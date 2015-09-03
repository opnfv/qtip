#! /bin/bash
echo cleaning Ip

sed -i -e '/demo1/{ n;N;N;d;}' /etc/ansible/hosts
neutron floatingip-delete $(neutron floatingip-list| grep "17" | awk '{print $2;}')
heat stack-delete exp2
