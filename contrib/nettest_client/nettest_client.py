##############################################################################
# Copyright (c) 2018 Spirent Communications and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import os
import logging
import requests
import json
import time


class NettestClient(object):

    def __init__(self, rest_server_ip, port, version):
        self.logger = logging.getLogger(__name__)

        self.rest_server_ip = rest_server_ip
        self.port = port
        self.version = version
        self.base_url = "http://" + self.rest_server_ip + ":" + str(port) + "/api/" + "v" + self.version + "/"
        self.headers = {"Content-Type": "application/json"}

    def write_log(self, log):
        self.logger.info(log)
        print log

    def create_stack(self, name, stack_type, public_network_name, **kargs):
        stack_id = None

        try:
            payload = {
                "stack_name": name,
                "stack_type": stack_type,
                "public_network": public_network_name,
                "stack_params": {
                    "stcv_affinity": kargs.get("stcv_affinity"),
                    "stcv_image": kargs.get("stcv_image"),
                    "stcv_flavor": kargs.get("stcv_flavor"),
                    "lab_server_ip": kargs.get("lab_server_ip"),
                    "license_server_ip": kargs.get("license_server_ip")
                }
            }

            stack_url = self.base_url + "stack"
            response = requests.post(url=stack_url, headers=self.headers, json=payload)
            if requests.codes.ok != response.status_code:
                self.write_log("create stack fail, response_content = " + response.content)
                return None
            print response.content
            stack_id = json.loads(response.content)["stack_id"]
        except Exception as err:
            self.write_log("create stack fail, error = " + str(err))

        return stack_id

    def destroy_stack(self, stack_id):
        payload = {"id": stack_id}
        url = self.base_url + "stack"
        try:
            response = requests.delete(url, params=payload)
            if requests.codes.ok != response.status_code:
                self.write_log("delete stack fail, err: " + response.content)
        except Exception as err:
            self.write_log("delete stack fail, error = " + str(err))
            return

        self.write_log("delete stack success")

    def run_rfc2544_testcase(self, stack_id, tc_name, metric_type, framesizes):
        url = self.base_url + "testcase"
        payload = {
            "name": tc_name,
            "stack_id": stack_id,
            "category": "rfc2544",
            "params": {
                "metric": metric_type,
                "framesizes": framesizes
            }
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if requests.codes.ok != response.status_code:
                self.write_log("run rfc2544 testcase fail, err = " + response.content)
                return None
        except Exception as err:
            self.write_log("run rfc2544 testcase fail, err = " + str(err))
            return None

        self.write_log("run rfc2544 testcase success")

        tc_id = json.loads(response.content)["tc_id"]

        return tc_id

    def delete_testcase(self, tc_id):
        url = self.base_url + "testcase"
        params = {"tc_id": tc_id}
        try:
            response = requests.delete(url, params=params)
            if requests.codes.ok != response.status_code:
                self.write_log("delete testcase fail, err = " + response.content)
        except Exception as err:
            self.write_log("delete testcase fail, err = " + str(err))

    def write_result(self, result):
        pass

    def get_tc_result(self, tc_id):
        ret = False
        url = self.base_url + "testcase"
        status_params = {
            "id": tc_id,
            "type": "status"
        }
        while True:
            response = requests.get(url, params=status_params)
            if requests.codes.ok == response.status_code:
                status = json.loads(response.content)["status"]
                if status == "running":
                    time.sleep(2)
                    continue
                elif status == "finished":
                    url = "http://" + self.rest_server_ip + ":" + str(self.port) + "/tc_results/" + tc_id
                    response = requests.get(url)
                    if requests.codes.ok == response.status_code:
                        self.write_log("get tc result success")
                        with open(os.getcwd() + "/" + tc_id, "w") as fd:
                            fd.write(response.content)
                        break
                        ret = True
                    else:
                        self.write_log(response.content)
                        break
                else:
                    self.write_log(response.content)
                    break
            else:
                self.write_log(response.content)
                break

        return ret


if __name__ == "__main__":

    nc = NettestClient(rest_server_ip="127.0.0.1", port=5001, version="1.0")

    stack_params = {
        "name": 's1',
        "stack_type": "stcv",
        "public_network_name": "public",
        "stcv_affinity": True,
        "stcv_image": "STCv-4.80.2426",
        "stcv_flavor": "small.shared",
        "lab_server_ip": '10.61.67.53',
        "license_server_ip": '10.140.88.61',
    }

    stack_id = nc.create_stack(**stack_params)
    if stack_id is None:
        print "create stack fail"
        # exit(1)

    # wait stcv vm into stable status
    time.sleep(30)

    tc_params = {
        "stack_id": stack_id,
        "tc_name": "tc1",
        "metric_type": "throughput",
        "framesizes": [64, 128, 256, 512, 1024]
    }
    tc_id = nc.run_rfc2544_testcase(**tc_params)
    if tc_id is None:
        print "run testcase fail"
        nc.destroy_stack(stack_id)
        exit(1)

    result = nc.get_tc_result(tc_id)
    if result is False:
        print "get testcase result fail"

    nc.delete_testcase(tc_id)

    nc.destroy_stack(stack_id)
