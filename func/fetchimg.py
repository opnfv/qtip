import os
import sys
import time
class FetchImg:
	
	def __init__(self):
		print 'Fetching Image!'
		print 'Fetching QTIP_VM Image'
	def download(self):
		time.sleep(2)
		os.system('cd ./Temp_Img && wget http://artifacts.opnfv.org/qtip/QTIP_CentOS.qcow2')
		
	
		filepath = './Temp_Img/QTIP_CentOS.qcow2'
		while not  os.path.isfile(filepath):
			time.sleep(10)
		print 'Download Completed!'
 
	

