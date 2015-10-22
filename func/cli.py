import yaml
import sys
from collections import defaultdict
import os
from func.env_setup import Env_setup
from func.driver import Driver
from func.fetchimg import FetchImg
from func.spawn_vm import SpawnVM
import argparse

class cli():
	def __init__(self):

		parser = argparse.ArgumentParser()
#		parser.add_argument('-h', '--help', help = 'welcome to QTIP')
		parser.add_argument('-s ','--suite', help = 'compute network storage ')
		parser.add_argument('-b', '--benchmark',
					 help = '''COMPUTE:
						dhrystone_serial.yaml \n
						dhrystone_paralle.yaml \n
						whetstone_serial.yaml \n
						whetstone_parllel.yaml \n
						dpi_serial.yaml \n
						dpi_paralle.yaml \n
						ssl_serial.yaml \n
						ssl_parallel.yaml ''')
		args = parser.parse_args()
		if not (args.suite or args.benchmark):
		        parser.error('Not enough arguments, -h, --help ')
			sys.exit(0)
		if ( args.suite and args.benchmark ):	
			obj = Env_setup()
			if os.path.isfile('./test_cases/'+args.suite+'/'+args.benchmark):

				[benchmark,roles,vm_info] = obj.parse('./test_cases/'+args.suite+'/'+args.benchmark) 

				if len(vm_info) !=0:
					vmObj = SpawnVM(vm_info)

				obj.callpingtest()
				obj.callsshtest()	
				obj.updateAnsible()
				dvr = Driver()
				dvr.drive_bench(benchmark,obj.roles_dict.items())
			else:
				print (args.benchmark, ' is not a Template in the Directory -  Enter a Valid file name. or use qtip.py -h for list')

