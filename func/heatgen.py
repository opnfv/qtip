import yaml

with open('config.yaml','r') as doc_r:
	doc=yaml.load(doc_r)


with open ('SampleHeat.yaml', 'r+') as H_temp:
        Heat_Dic=yaml.load(H_temp)

alist=[];

print"Printing the heat dictionary\n"

print Heat_Dic

for x in range (1, len(doc['Context']['Virtual_Machines'])+1):
        a_z=doc['Context']['Virtual_Machines']['vm_'+str(x)]['a_zone']
	img=doc['Context']['Virtual_Machines']['vm_'+str(x)]['image']
        Heat_Dic['resources']['public_port_'+str(x)]= {'type': 'OS::Neutron::Port', 'properties': {'network': {'get_resource': 'private_network'}, 'security_groups': [{'get_resource': 'demo1_security_Group'}]}}
        Heat_Dic['resources']['floating_ip_'+str(x)]=  {'type': 'OS::Neutron::FloatingIP', 'properties': {'floating_network': {'get_param': 'public_network'}}}
        Heat_Dic['resources']['floating_ip_assoc_'+str(x)]= {'type': 'OS::Neutron::FloatingIPAssociation','properties': {'floatingip_id': {'get_resource': 'floating_ip_'+str(x)}, 'port_id': {'get_resource': 'public_port_'+str(x)}}}
        print a_z
        Heat_Dic['resources']['my_instance_'+str(x)]={'type': 'OS::Nova::Server', 
							'properties': 
							{'image': img, 
							'networks': [{'port': {'get_resource': 'public_port_'+str(x)}}],
							 'flavor': 'm1.large', 	
							'availability_zone': a_z }}
       
        Heat_Dic['outputs']['instance_ip_'+str(x)]={'description': 'IP address of the instance', 'value': {'get_attr': ['floating_ip_'+str(x), 'floating_ip_address']}}
        print x


print Heat_Dic
#	if (doc['Context']['Virtual_Machines']['vm_'+str(x)]['role'] not in alist):

#		alist.append( doc['Context']['Virtual_Machines']['vm_'+str(x)]['role'])
        
#ifor y in range (0,len(alist)):
#        print "["+alist[y]+"]"
#	for x in range (1, len(doc['Context']['Virtual_Machines'])+1):
#		if (  doc['Context']['Virtual_Machines']['vm_'+str(x)]['role'] == alist[y]):

#	        	print doc['Context']['Virtual_Machines']['vm_'+str(x)]['ip']
                
			
with open ('Meh.yaml', 'w') as Output_file:
        Output_file.write(yaml.dump(Heat_Dic))
