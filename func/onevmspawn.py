import os
import sys
from collections import defaultdict
from func.env_setup import Env_setup
import yaml
class SpawnVM(Env_setup):
#	vm_params = defaultdict(list)
	def __init__(self):
		#vm_params = vm_info
		print 'spawing!'

	def spawn_vm(self,vm_params):
		#with open ('/home/opnfv/qtip/heat/SampleHeat.yaml', 'r+') as H_temp:
        	#	Heat_Dic=yaml.load(H_temp)
		Heat_Dic = """
heat_template_version: 2013-05-23
 
description: Simple template to deploy a single compute instance
 
parameters:
  image:
    type: string
    label: Image name or ID
    description: Image to be used for compute instance
    default: QTIP_CentOS
  flavor:
    type: string
    label: Flavor
    description: Type of instance (flavor) to be used
    default: m1.large

  private_network:
    type: string
    label: Private network name or ID
    description: Network to attach instance to.
    default: provider_network
 
resources:
  my_instance:
    type: OS::Nova::Server
    properties:
      image: { get_param: image }
      flavor: { get_param: flavor }
      networks:
        - network: { get_param: private_network }
      user_data: |
        #!/bin/sh
        echo "Hello, World!"
      user_data_format: RAW
 
outputs:
  instance_name:
    description: Name of the instance
    value: { get_attr: [my_instance, name] }
"""
#		print len(vm_params['availability_zone'])
		heatfin = yaml.load(Heat_Dic)
		with open ('/home/opnfv/qtip/HeatTemplate.yaml', 'w') as Output_file:
		        yaml.dump(heatfin,Output_file,default_flow_style = False)
