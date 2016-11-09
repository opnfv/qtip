##############################################################################
# Copyright (c) 2016 Dell Inc, ZTE and others.
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
import random
import logger_utils

logger = logger_utils.QtipLogger('create_zones').get


class AvailabilityZone:

    def __init__(self):
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

    def clean_all_aggregates(self):
        logger.info("clean all aggregates")
        nova = self._get_nova_client()
        agg_list = nova.aggregates.list()

        for agg in agg_list:
            agg_info = nova.aggregates.get_details(agg.id)
            agg_hosts = agg_info.hosts
            if len(agg_hosts):
                for host in agg_hosts:
                    nova.aggregates.remove_host(agg.id, host)
            nova.aggregates.delete(agg.id)

    def create_aggs(self, args):
        azone_list = list(set(args))
        azone_list.sort()

        nova = self._get_nova_client()
        hyper_list = nova.hypervisors.list()

        if len(azone_list) > len(hyper_list):
            logger.error("required available zones > compute nodes")
            return None

        compute_nodes = map(lambda x: x.service['host'], hyper_list)
        sample_nodes = random.sample(compute_nodes, len(azone_list))
        sample_nodes.sort()

        for index, item in enumerate(azone_list):
            logger.info("create aggregates: %s" % str(item))
            agg_id = nova.aggregates.create(item, item)

            logger.info("add host: %s" % sample_nodes[index])
            nova.aggregates.add_host(aggregate=agg_id, host=sample_nodes[index])
