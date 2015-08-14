#! /bin/bash

#DIR1= $PWD



function Call_Test {

	case "$1" in
        	 dhrystone)
                 mkdir $PWD/results/dhrystone
        	 ansible-playbook -s $PWD/benchmarks/playbooks/dhrystone.yaml --extra-vars "Dest_dir=$PWD/results" -v
         	 
          	 ;;

            	 ramspeed)
                 mkdir $PWD/results/ramspeed
     	     	 ansible-playbook -s $PWD/benchmarks/playbooks/ramspeedbench.yaml --extra-vars "Dest_dir=$PWD/results" -v 
         	 ;;

                 cachebench)
                 mkdir $PWD/results/cachebench
         	 ansible-playbook -s $PWD/benchmarks/playbooks/cachebench.yaml   --extra-vars "Dest_dir=$PWD/results" -v
          	 ;;

         	 whetstone)
                 mkdir $PWD/results/whetstone
         	 ansible-playbook -s $PWD/benchmarks/playbooks/whetstone.yaml  --extra-vars "Dest_dir=$PWD/results"  -v
          	 ;;

          	 *)
         	 echo "Please pass a correct  argument to test. use -h for more details"
         	 ;;
       esac

} 

mkdir $PWD/results
case "$1" in
          -h)
           printf "To run test.sh, 2 arguments are required\n"
           printf "First argument: The Test case to run\nOptions:\nFirst: For a comparison between a baremetal machine and a VM\nSecond: For a comparison between two baremetal machines\n\nSecond argument: The Benchmark to run\nOptions:\ndhrystone\nwhetstone\nramspeed\ncachebench\n"
           ;;
          First)
             
             echo "Enter the IP of the machine to be teststed for comparison to the VM"
             read ipvar
             echo "Enter the password of this machine"
             read -s  passwordvar
             expect  $PWD/data/ssh_exch.exp $ipvar $passwordvarp
             heat stack-create exp2 -f $PWD/Test-cases/SampleHeat.yaml
            
             VAR1=$( heat stack-show exp2 | grep "stack_status_reason" | awk '{print $6;}')
             echo $VAR1
             while [  "$VAR1" != completed ]
             do
             echo VM is coming up
             VAR1=$( heat stack-show exp2 | grep "stack_status_reason" | awk '{print $6;}')
            #echo $VAR1
             done
             echo VM Created

            if [ "$VAR1" == "completed" ]; then
              VAR=$( heat stack-show exp2 | grep "output_value" | awk '{print $4;}'| cut -d '"' -f2)
   
              echo IP of VM is:
              echo $VAR

              sed -i '/demo1/a '$VAR'' /etc/ansible/hosts
              sed -i '/demo1/a '$ipvar'' /etc/ansible/hosts
              

             
              echo Waiting for ping
              while !  ping -c1  $VAR &> /dev/null; do
             	 echo Waiting for ping
              done   
     
              echo Ping detected
              expect $PWD/data/ssh_exch.exp $VAR 
              Call_Test $2

              echo cleaning environment
              sleep 10
              $PWD/clean.sh
            

               fi	      

             ;;
             Second)
             echo Second test to be written below
             echo "Enter the IP of the first machine to be benchmarked for comparison"
             read ipvar
             echo "Enter the password of this machine"
             read -s  passwordvar
             expect  $PWD/data/ssh_exch.exp $ipvar $passwordvar
             sed -i '/demo1/a '$ipvar'' /etc/ansible/hosts
             echo "Enter the IP of the second machine to be benchmarked for comparison"
             read ipvar
             echo "Enter the password of this machine"
             read -s  passwordvar
             expect  $PWD/data/ssh_exch.exp $ipvar $passwordvar
             sed -i '/demo1/a '$ipvar'' /etc/ansible/hosts
             Call_Test $2
             echo cleaning environment
             sleep 10
             $PWD/clean.sh
             ;;
            
             *)
             echo Incorrect Arguments passed to the script. Run script with -h for more helo
              
esac


