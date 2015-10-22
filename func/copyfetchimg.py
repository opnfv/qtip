import os
import sys

class FetchImg:
	
	def __init__(self):
		print 'Fetching Image!'
	
	def DownloadImg(self):
		os.system('mkdir ./Temp_Img')
		filepath = './Temp_Img/QTIP_CentOS.qcow2'
	#filepath = './Temp_Img/cirros-0.3.3-x86_64-disk.img'
	#	filepath = './Temp_Img/CentosLive.iso'
		if os.path.isfile(filepath):
			print 'Image Already Downloaded'
			os.system('glance image-create --name "QTIP_CentOS" --is-public true --disk-format qcow2 \
			          --container-format bare \
          			  --file $PWD/Temp_Img/QTIP_CentOS.qcow2')
#			os.system('glance image-create --name "Cirros" --is-public true --disk-format qcow2 \
##			          --container-format bare \
#          			  --file $PWD/Temp_Img/cirros-0.3.3-x86_64-disk.img')
		#	os.system('glance image-create --name "CentosLive" --is-public true --disk-format iso \
	#		          --container-format bare \
        #  			  --file $PWD/Temp_Img/CentosLive.iso')


	

		else:
			print 'Fetching QTIP_VM Image'
			os.system('cd ./Temp_Img && wget http://artifacts.opnfv.org/qtip/QTIP_CentOS.qcow2')
#			os.system('wget http://download.cirros-cloud.net/0.3.3/cirros-0.3.3-x86_64-disk.img')
			print 'Uploading image to glance'
			os.system('glance image-create --name "QTIP_CentOS" --is-public true --disk-format qcow2 \
			          --container-format bare \
          			  --file $PWD/Temp_Img/QTIP_CentOS.qcow2')
		os.system('cd ..')
