import yaml
import sys
from collections import defaultdict
import os
class Driver:
	def __init__(self):
		print "Class driver initialized\n"
        def drive_bench (self,benchmark,roles):
		result_dir = '$PWD/results'
		benchmark_name = benchmark+'.yaml'
		print roles
		for k,v in roles:
			print k
			run_play= 'ansible-playbook -s $PWD/benchmarks/playbooks/{0} --extra-vars "Dest_dir={1} role={2}" -v'.format(benchmark_name,result_dir,k)

			status = os.system(run_play)
