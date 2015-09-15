import yaml
import sys
from collections import defaultdict
import os
from func.env_setup import Env_setup
from func.driver import Driver

testcase = {'BMBM' : './Test-cases/Bare_vs_Bare/config.yaml',
	   'BMVM' : './Test-cases/Bare_vs_VM/config.yaml'
}


class cli:
	def __init__(self,input_args):
		if input_args[1] == '-h' or input_args[1]== '--help':
			print 'Enter python qtip.py dhrystone_parallel.yaml'
		elif len(input_args) == 2:
			
			obj = Env_setup()
			[benchmark,roles] = obj.parse('/home/opnfv/qtip/test_cases/'+input_args[1]) 
			for k , v in roles:
				print k
			obj.pingsshtest()
			obj.updateAnsible()
			dvr = Driver()
#			dvr.drive_bench('/home/opnfv/qtip/test_case/'+input_args[1],input_args[2])
			dvr.drive_bench(benchmark,roles)
		elif len(input_args) >3 or len(input_args) <2:
			print 'Use test.py -h for usage'

def main():
	ObjCli = cli(sys.argv)


if __name__ == "__main__":
	main()
