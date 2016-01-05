#! /bin/bash

cp ${REPOS_DIR}/releng/utils/fetch_os_creds.sh ${QTIP_DIR}/data/
cd ${QTIP_DIR}/data  &&  source get_env_info.sh -n ${INSTALLER_TYPE} -i ${INSTALLER_IP}
source ${QTIP_DIR}/data/opnfv-creds.sh
cd ${QTIP_DIR}  && python qtip.py -l ${LAB} -f compute.txt
cd ${QTIP_DIR}  && python qtip.py -l ${LAB} -f storage.txt
cd ${QTIP_DIR}  && python qtip.py -l ${LAB} -f network.txt

cd ${QTIP_DIR}/data/ref_results/ $$ python compute_suite.py
cd ${QTIP_DIR}/data/ref_results/ $$ python storage_suite.py
cd ${QTIP_DIR}/data/ref_results/ $$ python network_suite.py





