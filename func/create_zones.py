##############################################################################
# Copyright (c) 2015 Dell Inc  and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client
import os
import re
from collections import defaultdict


class create_zones:

    def __init__(self):
        print 'Creating Zones'
        self._keystone_client = None
        self._nova_client = None

    def _get_keystone_client(self):
        """returns a keystone client instance"""

        if self._keystone_client is None:
            '''
            self._keystone_client = keystoneclient.v2_0.client.Client(
            auth_url=os.environ.get('OS_AUTH_URL'),
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'),
            tenant_name=os.environ.get('OS_TENANT_NAME'))
            '''
            auth = v2.Password(auth_url=os.environ.get('OS_AUTH_URL'),
                               username=os.environ.get('OS_USERNAME'),
                               password=os.environ.get('OS_PASSWORD'),
                               tenant_name=os.environ.get('OS_TENANT_NAME'))

            sess = session.Session(auth=auth)
        else:
            return self._keystone_client

        return sess

    def _get_nova_client(self):
        if self._nova_client is None:
            keystone = self._get_keystone_client()
            self._nova_client = client.Client('2', session=keystone)
        return self._nova_client

    @staticmethod
    def check_aggregate(nova, agg_name):
        list1 = nova.aggregates.list()
        agg_name_exist = False
        for x in list1:
            if x.name == agg_name:
                agg_name_exist = True
        return agg_name_exist

    @staticmethod
    def get_aggregate_id(nova, agg_name):
        list1 = nova.aggregates.list()
        for x in list1:
            if x.name == agg_name:
                agg_id = x.id
                return agg_id

    @staticmethod
    def check_host_added_to_aggregate(nova, agg_id, hostname):
        host_added = False
        list1 = nova.aggregates.get_details(agg_id)

        nme = str(list1.hosts)
        if hostname in nme:
            host_added = True
        return host_added

    @staticmethod
    def del_agg(nova, id, host):

        nova.aggregates.remove_host(id, host)
        nova.aggregates.delete(id)

    @staticmethod
    def get_compute_num(compute_name):

        num = re.findall(r'\d+', compute_name)
        return int(num[0]) - 1

    def test(self):
        nova = self._get_nova_client()
        hyper_list = nova.hypervisors.list()
        return hyper_list

    def create_agg(self, d):
        nova = self._get_nova_client()
        hyper_list = nova.hypervisors.list()
        host_a = []
        zone_machine = defaultdict(list)

        for x in range(len(hyper_list)):

            host_a.append(hyper_list[x].service['host'])
            host_a[x] = str(host_a[x])

        host_a.sort()
        for k in d:

            zone_machine[k].append(' ')

        for x in range(len(zone_machine)):
            compute_index = self.get_compute_num(d[x])
            if compute_index > len(hyper_list):
                print '\n The specified compute node doesnt exist. using compute 1'
                compute_index = 1
            if not self.check_aggregate(nova, host_a[compute_index]):
                agg_id_a = nova.aggregates.create(host_a[compute_index], d[x])
                nova.aggregates.add_host(aggregate=agg_id_a, host=host_a[compute_index])

            else:
                id1 = self.get_aggregate_id(nova, host_a[compute_index])
                self.del_agg(nova, id1, host_a[compute_index])
                nova.aggregates.create(host_a[compute_index], d[x])
                id1 = self.get_aggregate_id(nova, host_a[compute_index])

                if not self.check_host_added_to_aggregate(
                        nova, id1, host_a[compute_index]):

                    nova.aggregates.add_host(aggregate=id1, host=host_a[compute_index])
