import os
import sys
from collections import defaultdict
import yaml

class Env_setup:
	roles_ip_list = []			#ROLE and its corresponding IP address list
	ip_pw_list = []				#IP and password, this will be used to ssh			
	roles_dict = defaultdict(list)
	ip_pw_dict = defaultdict(list)			

	def __init__(self):
		print 'class initated'
	def writeTofile(self,role):
		fname2= open('/etc/ansible/hosts', 'w')
		for k in role:					#reading the roles and getting to their ips
			fname2.write('['+k+']\n')		#writing the role into the file
			num = len(role[k])
			for x in range(num):			#writing all the values for that role into the file
				fname2.write(role[k][x]+'\n')
		fname2.close
	def sshping(self, lister):
		pingFlag = 0
		#print lister
               	for k,v in lister:
			#print k+ '\t' +v
			ipvar= k
			pwvar= v
			ssh_cmd= 'expect ./data/ssh_exch.exp {0} {1}'.format(ipvar, pwvar)
			print ssh_cmd
			res = os.system(ssh_cmd)
  			while pingFlag !=1:
				ping_cmd = 'ping -c1 {0}'.format(ipvar)
				result = os.system(ping_cmd)
				if result == 0:
					pingFlag = 1
					print 'Machine is UP'
				else:
					print 'Waiting for machine'

	def GetHostMachineinfo(self,Hosttag):
		num = len(Hosttag)
		offset = len(self.roles_ip_list)
		print 'Offset: ', offset
		for x in range(num):
			hostlabel = 'machine_'+str(x+1)
			
			self.roles_ip_list.insert(offset,(Hosttag[hostlabel]['role'],Hosttag[hostlabel]['ip']))
			self.ip_pw_list.insert(offset,(Hosttag[hostlabel]['ip'],Hosttag[hostlabel]['pw']))

	def parse(self,configfilepath):
		try:
			fname = open(configfilepath,'r+')
			doc = yaml.load(fname)
			fname.close()

			for scenario in doc:
				benchmark = doc['scenario']['benchmark']
			self.GetHostMachineinfo(doc['Context']['Host_Machines'])

			#num = len(doc['Context']['Vir_Machines'])
			#for x in range(num): 		
			#	lab = 'host_machine'+ str(x+1)
			#	self.roles_ip_list.insert(x,(doc[lab]['role'],doc[lab]['ip']))
			#	self.ip_pw_list.insert(x,(doc[lab]['ip'],doc[lab]['pw']))
			for k,v in self.roles_ip_list:
				self.roles_dict[k].append(v)
			for k,v in self.ip_pw_list:
				self.ip_pw_dict[k].append(v)
			return (benchmark, self.roles_dict.items())
		except KeyboardInterrupt:
			fname.close()
			print 'ConfigFile Closed: exiting!'
			sys.exit(0)
	def updateAnsible(self):
		self.writeTofile(self.roles_dict)
	def pingsshtest(self):
		self.sshping(self.ip_pw_list)
