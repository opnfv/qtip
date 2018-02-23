##############################################################################
# Copyright (c) 2018 Spirent Communications and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import base64
import copy
import logging
import os
import shutil
import threading
from time import sleep
import uuid

import requests
from stcrestclient import stchttp


class Stcv2Net1Stack(object):
    ADMIN_NETWORK_NAME = "admin"
    ADMIN_SUBNET_ADDR = "50.50.50.0/24"
    ADMIN_GW_IP = "50.50.50.1"
    TST_NETWORK_NAME = "tst"
    TST_SUBNET_ADDR = "192.168.0.0/24"
    TST_GW_IP = "192.168.0.1"
    ROUTER_NAME = "router"
    WEST_STCV_NAME = "west_stcv"
    EAST_STCV_NAME = "east_stcv"
    AFFINITY_SG_NAME = "affinity"
    STCV_USER_DATA = '''#cloud-config
spirent:
    ntp: '''

    def __init__(self, name, conn, ext_network_name, params):
        self.logger = logging.getLogger(__name__)

        self.name = name
        self.conn = conn
        self.ext_network_name = ext_network_name
        self.image_name = params['stcv_image']
        self.flavor_name = params['stcv_flavor']
        self.ntp_server_ip = params['license_server_ip']
        self.affinity = params['stcv_affinity']

        self.stack_id = str(uuid.uuid4())
        self.admin_network = None
        self.admin_subnet = None
        self.tst_network = None
        self.tst_subnet = None
        self.ext_network = None
        self.router = None
        self.affinity_sg = None

        self.west_stcv = None
        self.west_stcv_ip = ''
        self.east_stcv = None
        self.east_stcv_ip = ''

    def _deploy_test_network(self):

        # create tst network and subnet
        self.tst_network = self.conn.network.create_network(
            name=self.TST_NETWORK_NAME)
        self.tst_subnet = self.conn.network.create_subnet(
            name=self.TST_NETWORK_NAME + '_subnet',
            network_id=self.tst_network.id,
            ip_version='4',
            cidr=self.TST_SUBNET_ADDR,
            gateway_ip=self.TST_GW_IP,
            is_dhcp_enabled=True)

        # create admin network and subnet
        self.admin_network = self.conn.network.create_network(
            name=self.ADMIN_NETWORK_NAME)
        self.admin_subnet = self.conn.network.create_subnet(
            name=self.ADMIN_NETWORK_NAME + '_subnet',
            network_id=self.admin_network.id,
            ip_version='4',
            cidr=self.ADMIN_SUBNET_ADDR,
            gateway_ip=self.ADMIN_GW_IP,
            is_dhcp_enabled=True)

        # create external gateway and connect admin subnet to router
        self.ext_network = self.conn.network.find_network(self.ext_network_name)
        self.router = self.conn.network.create_router(name=self.ROUTER_NAME,
                                                      external_gateway_info={"network_id": self.ext_network.id},
                                                      is_admin_state_up=True)
        self.conn.network.add_interface_to_router(self.router, subnet_id=self.admin_subnet.id)

    def _depoly_stcv(self, name, image_id, flavor_id, scheduler_hints, user_data):

        stcv = self.conn.compute.create_server(
            name=name, image_id=image_id, flavor_id=flavor_id,
            networks=[{"uuid": self.admin_network.id}, {"uuid": self.tst_network.id}],
            config_drive=True,
            user_data=base64.encodestring(user_data)
        )
        stcv = self.conn.compute.wait_for_server(stcv)

        stcv_fixed_ip = stcv.addresses[self.admin_network.name][0]['addr']
        stcv_floating_ip = self.conn.network.create_ip(floating_network_id=self.ext_network.id)
        self.conn.compute.add_floating_ip_to_server(server=stcv, address=stcv_floating_ip.floating_ip_address,
                                                    fixed_address=stcv_fixed_ip)

        return {'stcv': stcv, 'fixed_ip': stcv_fixed_ip, 'floating_ip': stcv_floating_ip}

    def create_stack(self):

        image = self.conn.compute.find_image(self.image_name)
        flavor = self.conn.compute.find_flavor(self.flavor_name)

        if self.affinity:
            self.affinity_sg = \
                self.conn.compute.create_server_group(name=self.AFFINITY_SG_NAME,
                                                      policies=["affinity"])
        else:
            self.affinity_sg = \
                self.conn.compute.create_server_group(name=self.AFFINITY_SG_NAME,
                                                      policies=["anti-affinity"])
        self._deploy_test_network()

        user_data = self.STCV_USER_DATA + self.ntp_server_ip

        stcv = self._depoly_stcv(name=self.WEST_STCV_NAME,
                                 image_id=image.id,
                                 flavor_id=flavor.id,
                                 scheduler_hints=self.affinity_sg,
                                 user_data=user_data)
        self.west_stcv = stcv['stcv']
        self.west_stcv_ip = stcv['floating_ip']

        stcv = self._depoly_stcv(name=self.EAST_STCV_NAME,
                                 image_id=image.id,
                                 flavor_id=flavor.id,
                                 scheduler_hints=self.affinity_sg,
                                 user_data=user_data)
        self.east_stcv = stcv['stcv']
        self.east_stcv_ip = stcv['floating_ip']

    def delete_stack(self):

        self.conn.compute.delete_server(self.west_stcv, ignore_missing=True)
        self.conn.compute.delete_server(self.east_stcv, ignore_missing=True)

        self.conn.compute.delete_server_group(server_group=self.affinity_sg,
                                              ignore_missing=True)

        # delete external gateway
        self.conn.network.delete_router(self.router, ignore_missing=True)

        # delete tst network
        self.conn.network.delete_subnet(self.tst_subnet, ignore_missing=True)
        self.conn.network.delete_network(self.tst_network, ignore_missing=True)

        # delete admin network
        self.conn.network.delete_subnet(self.admin_subnet, ignore_missing=True)
        self.conn.network.delete_network(self.admin_network, ignore_missing=True)


class StcSession:
    """ wrapper class for stc session"""

    def __init__(self, labserver_addr, user_name, session_name):
        self.logger = logging.getLogger(__name__)

        # create connection obj
        self.stc = stchttp.StcHttp(labserver_addr)
        self.user_name = user_name
        self.session_name = session_name

        # create session on labserver
        self.session_id = self.stc.new_session(self.user_name, self.session_name)
        self.stc.join_session(self.session_id)
        return

    def __del__(self):
        # destroy resource on labserver
        self.stc.end_session()

    def clean_all_session(self):
        session_urls = self.stc.session_urls()
        for session in session_urls:
            resp = requests.delete(session)
            self.logger.info("delete session resp: %s", str(resp))
        return


class StcRfc2544Test:
    """ RFC2544 test class"""

    RESULT_PATH_PREFIX = './tc_results/rfc2544/'
    TC_STATUS_INIT = 'init'
    TC_STATUS_RUNNING = 'running'
    TC_STATUS_FINISHED = 'finished'
    TC_STATUS_ERROR = 'error'

    default_additional_params = {
        "AcceptableFrameLoss": 0.0,
        "Duration": 60,
        "FrameSizeList": 64,
        "LearningMode": 'AUTO',
        "NumOfTrials": 1,
        "RateInitial": 99.0,
        "RateLowerLimit": 99.0,
        "RateStep": 10.0,
        "RateUpperLimit": 99.0,
        "Resolution": 1.0,
        "SearchMode": 'BINARY',
        "TrafficPattern": 'PAIR'
    }

    def __init__(self, name, lab_server_ip, license_server_ip,
                 west_stcv_admin_ip, west_stcv_tst_ip,
                 east_stcv_admin_ip, east_stcv_tst_ip,
                 stack_id=None, **kwargs):
        self.logger = logging.getLogger(__name__)

        self.name = name
        self.lab_server_ip = lab_server_ip
        self.license_server_ip = license_server_ip
        self.west_stcv_ip = west_stcv_admin_ip
        self.west_stcv_tst_ip = west_stcv_tst_ip
        self.east_stcv_ip = east_stcv_admin_ip
        self.east_stcv_tst_ip = east_stcv_tst_ip
        self.stack_id = stack_id
        self.metric = kwargs.get('metric')
        self.additional_params = copy.copy(self.default_additional_params)
        self.additional_params['FrameSizeList'] = kwargs.get('framesizes')

        self.tc_id = str(uuid.uuid4())

        self.stc = None
        self.sess = None
        self.executor = None
        self.status = 'init'
        self.err_reason = ''

    def config_license(self, license_server_addr):
        license_mgr = self.stc.get("system1", "children-licenseservermanager")
        self.stc.create("LicenseServer",
                        under=license_mgr,
                        attributes={"server": license_server_addr})
        return

    def create_project(self, traffic_custom=None):
        self.project = self.stc.get("System1", "children-Project")
        # Configure any custom traffic parameters
        if traffic_custom == "cont":
            self.stc.create("ContinuousTestConfig", under=self.project)
        return

    def config_test_port(self, chassis_addr, slot_no, port_no, intf_addr, gateway_addr):
        # create test port
        port_loc = "//%s/%s/%s" % (chassis_addr, slot_no, port_no)
        chassis_port = self.stc.create('port', self.project)
        self.stc.config(chassis_port, {'location': port_loc})

        # Create emulated genparam for east port
        device_gen_params = self.stc.create("EmulatedDeviceGenParams",
                                            under=self.project,
                                            attributes={"Port": chassis_port})
        # Create the DeviceGenEthIIIfParams object
        self.stc.create("DeviceGenEthIIIfParams",
                        under=device_gen_params,
                        attributes={"UseDefaultPhyMac": "True"})

        # Configuring Ipv4 interfaces
        self.stc.create("DeviceGenIpv4IfParams",
                        under=device_gen_params,
                        attributes={"Addr": intf_addr, "Gateway": gateway_addr})

        # Create Devices using the Device Wizard
        self.stc.perform("DeviceGenConfigExpand",
                         params={"DeleteExisting": "No", "GenParams": device_gen_params})

        return

    def do_test(self):
        if self.metric == "throughput":
            self.stc.perform("Rfc2544SetupThroughputTestCommand", self.additional_params)
        elif self.metric == "backtoback":
            self.stc.perform("Rfc2544SetupBackToBackTestCommand", self.additional_params)
        elif self.metric == "frameloss":
            self.stc.perform("Rfc2544SetupFrameLossTestCommand", self.additional_params)
        elif self.metric == "latency":
            self.stc.perform("Rfc2544SetupLatencyTestCommand", self.additional_params)
        else:
            raise Exception("invalid rfc2544 test metric.")

        # Save the configuration
        self.stc.perform("SaveToTcc", params={"Filename": "2544.tcc"})

        # Connect to the hardware...
        self.stc.perform("AttachPorts",
                         params={"portList": self.stc.get("system1.project", "children-port"),
                                 "autoConnect": "TRUE"})

        # Apply configuration.
        self.stc.apply()
        self.stc.perform("SequencerStart")
        self.stc.wait_until_complete()

        return

    def write_query_results_to_csv(self, results_path, csv_results_file_prefix, query_results):
        filec = os.path.join(results_path, csv_results_file_prefix + ".csv")
        with open(filec, "wb") as result_file:
            result_file.write(query_results["Columns"].replace(" ", ",") + "\n")
            for row in (query_results["Output"].replace("} {", ",").replace("{", "").replace("}", "").split(",")):
                result_file.write(row.replace(" ", ",") + "\n")

    def format_result(self, metric, original_result_dict):
        result = {}
        if metric == 'throughput':
            columns = original_result_dict["Columns"].split(' ')
            index_framesize = columns.index("ConfiguredFrameSize")
            index_result = columns.index("Result")
            index_throughput = columns.index("Throughput(%)")
            index_ForwardingRate = columns.index("ForwardingRate(fps)")
            outputs = \
                original_result_dict["Output"].replace('} {', ',').replace("{", "").replace("}", "").split(",")

            for row in outputs:
                output = row.split(' ')
                result[output[index_framesize]] = {'Result': output[index_result],
                                                   "Throughput(%)": output[index_throughput],
                                                   "ForwardingRate(fps)": output[index_ForwardingRate]}

        elif self.metric == "latency":
            pass

        elif self.metric == "frameloss":
            pass

        elif self.metric == "backtoback":
            pass

        return result

    def collect_result(self, local_dir):
        # Determine what the results database filename is...
        lab_server_resultsdb = self.stc.get(
            "system1.project.TestResultSetting", "CurrentResultFileName")
        self.stc.perform("CSSynchronizeFiles",
                         params={"DefaultDownloadDir": local_dir})

        resultsdb = local_dir + lab_server_resultsdb.split("/Results")[1]

        if not os.path.exists(resultsdb):
            resultsdb = lab_server_resultsdb
            self.logger.info("Failed to create the local summary DB File, using"
                             " the remote DB file instead.")
        else:
            self.logger.info(
                "The local summary DB file has been saved to %s", resultsdb)

        if self.metric == "throughput":
            resultsdict = self.stc.perform("QueryResult",
                                           params={
                                               "DatabaseConnectionString": lab_server_resultsdb,
                                               "ResultPath": "RFC2544ThroughputTestResultDetailedSummaryView"})
        elif self.metric == "backtoback":
            resultsdict = self.stc.perform("QueryResult",
                                           params={
                                               "DatabaseConnectionString": lab_server_resultsdb,
                                               "ResultPath": "RFC2544Back2BackTestResultDetailedSummaryView"})
        elif self.metric == "frameloss":
            resultsdict = self.stc.perform("QueryResult",
                                           params={
                                               "DatabaseConnectionString": lab_server_resultsdb,
                                               "ResultPath": "RFC2544LatencyTestResultDetailedSummaryView"})
        elif self.metric == "latency":
            resultsdict = self.stc.perform("QueryResult",
                                           params={
                                               "DatabaseConnectionString": lab_server_resultsdb,
                                               "ResultPath": "RFC2544FrameLossTestResultDetailedSummaryView"})
        else:
            raise Exception("invalid rfc2544 test metric.")

        self.write_query_results_to_csv(self.results_dir, self.metric, resultsdict)

        self.result = self.format_result(self.metric, resultsdict)

        return

    def thread_entry(self):
        self.status = self.TC_STATUS_RUNNING
        try:
            # create session on lab server
            self.sess = StcSession(self.lab_server_ip, session_name=self.name, user_name=self.name)
            self.stc = self.sess.stc

            # create test result directory
            self.results_dir = self.RESULT_PATH_PREFIX + self.tc_id + '/'
            os.makedirs(self.results_dir)

            # Bring up license server
            self.config_license(self.license_server_ip)

            self.logger.info("config license success, license_server_addr = %s.", self.license_server_ip)

            # Create the root project object and Configure any custom traffic parameters
            self.create_project()

            self.logger.info("create project success.")

            # configure test port
            self.config_test_port(self.west_stcv_ip, 1, 1, self.west_stcv_tst_ip, self.east_stcv_tst_ip)
            self.config_test_port(self.east_stcv_ip, 1, 1, self.east_stcv_tst_ip, self.west_stcv_tst_ip)

            self.logger.info("config test port success, west_chassis_addr = %s, east_chassis_addr = %s.",
                             self.west_stcv_ip, self.east_stcv_ip)

            # execute test
            self.do_test()

            self.logger.info("execute test success.")

            # collect test result
            self.collect_result(self.results_dir)

            self.logger.info("collect result file success, results_dir = %s.", self.results_dir)

            self.status = self.TC_STATUS_FINISHED

        except Exception as err:
            self.logger.error("Failed to execute Rfc2544 testcase, err: %s", str(err))
            self.err_reason = str(err)
            self.status = self.TC_STATUS_ERROR

        finally:
            if self.sess is not None:
                self.sess.clean_all_session()

    def execute(self):

        self.executor = threading.Thread(name='rfc2544', target=self.thread_entry())
        self.executor.start()

    def get_result(self):
        if self.status != self.TC_STATUS_FINISHED:
            return {'name': self.name,
                    'tc_id': self.tc_id,
                    'status': self.status
                    }

        return {'name': self.name,
                'category': 'rfc2544',
                'id': self.tc_id,
                'params': {
                    'metric': self.metric,
                    'framesizes': self.additional_params.get('FrameSizeList')},
                'result': self.result}

    def get_status(self):
        return self.status

    def delete_result(self):
        shutil.rmtree(self.results_dir)
        pass

    def cancel_run(self):
        pass

    def get_err_reason(self):
        return self.err_reason


if __name__ == '__main__':

    lab_server_ip = '192.168.37.122'
    license_server_ip = '192.168.37.251'
    west_stcv_admin_ip = '192.168.37.202'
    west_stcv_tst_ip = '192.168.1.20'
    east_stcv_admin_ip = '192.168.37.212'
    east_stcv_tst_ip = '192.168.1.17'

    tc = StcRfc2544Test(name='tc1',
                        lab_server_ip=lab_server_ip,
                        license_server_ip=license_server_ip,
                        west_stcv_admin_ip=west_stcv_admin_ip,
                        west_stcv_tst_ip=west_stcv_tst_ip,
                        east_stcv_admin_ip=east_stcv_admin_ip,
                        east_stcv_tst_ip=east_stcv_tst_ip,
                        metric="throughput",
                        framesizes=[64, 128, 256, 512, 1024])
    tc.execute()
    status = tc.get_status()
    while(status != tc.TC_STATUS_FINISHED):
        if status == tc.TC_STATUS_ERROR:
            print "tc exectue fail, reason %s" % tc.get_err_reason()
            break
        sleep(2)
    if status == tc.TC_STATUS_FINISHED:
        print tc.get_result()
'''
    tc = StcRfc2544Test(name='tc2',
                        lab_server_ip=lab_server_ip,
                        license_server_ip=license_server_ip,
                        west_stcv_admin_ip=west_stcv_admin_ip,
                        west_stcv_tst_ip=west_stcv_tst_ip,
                        east_stcv_admin_ip=east_stcv_admin_ip,
                        east_stcv_tst_ip=east_stcv_tst_ip,
                        metric="latency",
                        framesizes=[64, 128, 256, 512, 1024])
    tc.execute()
    status = tc.get_status()
    while(status != tc.TC_STATUS_FINISHED):
        if status == tc.TC_STATUS_ERROR:
            print "tc exectue fail, reason %s" % tc.get_err_reason()
            break
        sleep(2)
    if status == tc.TC_STATUS_FINISHED:
        print tc.get_result()

    tc = StcRfc2544Test(name='tc3',
                        lab_server_ip=lab_server_ip,
                        license_server_ip=license_server_ip,
                        west_stcv_admin_ip=west_stcv_admin_ip,
                        west_stcv_tst_ip=west_stcv_tst_ip,
                        east_stcv_admin_ip=east_stcv_admin_ip,
                        east_stcv_tst_ip=east_stcv_tst_ip,
                        metric="backtoback",
                        framesizes=[64, 128, 256, 512, 1024])
    tc.execute()
    status = tc.get_status()
    while(status != tc.TC_STATUS_FINISHED):
        if status == tc.TC_STATUS_ERROR:
            print "tc exectue fail, reason %s" % tc.get_err_reason()
            break
        sleep(2)
    if status == tc.TC_STATUS_FINISHED:
        print tc.get_result()

    tc = StcRfc2544Test(name='tc4',
                        lab_server_ip=lab_server_ip,
                        license_server_ip=license_server_ip,
                        west_stcv_admin_ip=west_stcv_admin_ip,
                        west_stcv_tst_ip=west_stcv_tst_ip,
                        east_stcv_admin_ip=east_stcv_admin_ip,
                        east_stcv_tst_ip=east_stcv_tst_ip,
                        metric="frameloss",
                        framesizes=[64, 128, 256, 512, 1024])
    tc.execute()
    status = tc.get_status()
    while(status != tc.TC_STATUS_FINISHED):
        if status == tc.TC_STATUS_ERROR:
            print "tc exectue fail, reason %s" % tc.get_err_reason()
            break
        sleep(2)
    if status == tc.TC_STATUS_FINISHED:
        print tc.get_result()
'''

'''
class Testcase(object):

    def __init__(self, stack):
        self.stack = stack

    def execute(self):
        pass

class TestcaseFactory(object):

    def __init__(self):

    def create_tc(self, tc_metadata):
        self.tc_name = tc_metadata['tc_name']
        self.tc_id = str(uuid.uuid4())
        if
'''
