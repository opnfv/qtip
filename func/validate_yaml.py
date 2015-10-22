import yaml
import os




class Validate_Yaml():
	
	def __init__(self, doc):

		print 'Validating YAML CONFIG FILE'

		if not doc['Scenario']:
			print '\nScenario Field missing\n'
		if not doc['Scenario']['benchmark']:
			print '\nBenchmark field missing'
		if not doc['Scenario']['pointless']:
			print '\nBabyeating anumal'
		if not doc['Context']:
			print '\nEntire Context is missing'
		if not doc['Context']['Host_Machine']:
			print '\nNo Host Machine'
		if not doc['Context']['Host_Machine']['machine_1']
