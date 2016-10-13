#! /bin/bash

usage() {
    echo "usage $0  -n <installer_type> -i <installer_ip> -k <key incase of apex>"
}



while getopts ":n:i:k:" optchar; do
    case "${optchar}" in
        n)
         export INSTALLER_TYPE=${OPTARG};;

        i)
         export  INSTALLER_IP=${OPTARG};;

        k)
         export APEX_KEY=${OPTARG};;

        *)
           echo "Incorrect usage"
           usage ;;
    esac
done

if [ $INSTALLER_TYPE == "apex" ]
   then
       if [ -z $APEX_KEY ]
          then
              echo "Please provide the  the key to access the APEX Instack VM"
              usage
              exit 1
       fi
fi


${REPOS_DIR}/releng/utils/fetch_os_creds.sh -d ${QTIP_DIR}/opnfv-creds.sh
