##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from index_calculation import generic_index as get_index
from index_calculation import get_reference
from result_accum import result_concat as concat


def iperf_index():
    iperf_dict = concat('results/iperf/')
    iperf_bm_ref = get_reference('network', 'iperf_bm', 'throughput received(b/s)')
    iperf_bm_index = get_index(iperf_dict, 'iperf_bm', iperf_bm_ref, 'details', 'bandwidth', 'received_throughput')
    iperf_vm_ref = get_reference('network', 'iperf_vm', 'throughput received(b/s)')
    iperf_vm_index = get_index(iperf_dict, 'iperf_vm', iperf_vm_ref, 'details', 'bandwidth', 'received_throughput')

    iperf_vm_2_ref = get_reference('network', 'iperf_vm_2', 'throughput received(b/s)')
    iperf_vm_2_index = get_index(iperf_dict, 'iperf_vm_2', iperf_vm_2_ref, 'details', 'bandwidth', 'received_throughput')
    iperf_index = float(iperf_bm_index + iperf_vm_index + iperf_vm_2_index) / 3
    print iperf_index
    iperf_dict_i = {}
    iperf_dict_i['index'] = iperf_index
    iperf_dict_i['results'] = iperf_dict
    return iperf_dict_i
