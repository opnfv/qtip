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
from collections import defaultdict


class create_zones:

    def __init__(self):
        print 'Creating Zones'
        self._keystone_client = None
        self._nova_client = None

    def _get_keystone_client(self):
        '''returns a keystone client instance'''

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

        return sess

    def _get_nova_client(self):
        if self._nova_client is None:
            keystone = self._get_keystone_client()
            self._nova_client = client.Client('2', session=keystone)
        return self._nova_client

    def check_aggregate(self, nova, agg_name):
        list1 = nova.aggregates.list()

        agg_name_exist = False
        for x in list1:
            
            if x.name == agg_name:
                agg_name_exist = True
        return agg_name_exist

    def get_aggregate_id(self, nova, agg_name):
        list1 = nova.aggregates.list()
        agg_id = 0
        agg_name_exist = False
        for x in list1:
            if x.name == agg_name:
                agg_id = x.id
                return agg_id

    def check_host_added_to_aggregate(self, nova, agg_id, hostname):
        host_added = False
        list1 = nova.aggregates.get_details(agg_id)

        nme = str(list1.hosts)
        if(hostname in nme):
            host_added = True
        return host_added

    def del_agg(self, nova, id, host):

        nova.aggregates.remove_host(id, host)
        nova.aggregates.delete(id)

    def create_agg(self, D):
        nova = self._get_nova_client()
        hyper_list = nova.hypervisors.list()
        hostnA = []
        zone_machine = defaultdict(list)

        x = 0
        for x in range(len(hyper_list)):

            hostnA.append(hyper_list[x].service['host'])
            hostnA[x] = str(hostnA[x])

        hostnA.sort()
        for k in D:

            zone_machine[k].append(' ')

        for x in range(len(zone_machine)):
            if not self.check_aggregate(nova, hostnA[x]):
                agg_idA = nova.aggregates.create(hostnA[x], D[x])
                nova.aggregates.add_host(aggregate=agg_idA, host=hostnA[x])

            else:

                id1 = self.get_aggregate_id(nova, hostnA[x])
                self.del_agg(nova, id1, hostnA[x])
                agg_idA = nova.aggregates.create(hostnA[x], D[x])
                id1 = self.get_aggregate_id(nova, hostnA[x])

                if not self.check_host_added_to_aggregate(
                        nova, id1, hostnA[x]):

                    nova.aggregates.add_host(aggregate=id1, host=hostnA[x])
