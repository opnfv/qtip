#! /bin/bash

usage() {
    echo "usage $0  -n <installer_type> -i <installer_ip>"
}



while getopts ":n:i:" optchar; do
    case "${optchar}" in
        n)
         export INSTALLER_TYPE=${OPTARG};; 

        i)
         export  INSTALLER_IP=${OPTARG};;

        *)
           echo "Incorrect usage"
           usage ;;
    esac
done
