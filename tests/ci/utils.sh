#!/usr/bin/env bash

function detect_installer_ip {
    case ${INSTALLER_TYPE} in
        apex)
            sudo virsh domifaddr undercloud | grep ipv4 | awk '{print $4}' | cut -d/ -f1
            ;;
    esac
}

function start_services {
    export ENV_FILE="${ENV_FILE:-env_file}"
cat << EOF > $ENV_FILE
INSTALLER_TYPE=${INSTALLER_TYPE}
INSTALLER_IP=${INSTALLER_IP:-$(detect_installer_ip)}
NODE_NAME=${NODE_NAME:-opnfv-pod}
SCENARIO=${DEPLOY_SCENARIO:-generic}
TESTAPI_URL=${TESTAPI_URL:-}
EOF

    TMPFILE=`mktemp /tmp/qtip.XXXXXX` || exit 1
    curl https://git.opnfv.org/releng/plain/utils/fetch_os_creds.sh | bash -s -- \
        -i ${INSTALLER_TYPE} -a ${INSTALLER_IP} -d ${TMPFILE}
    grep "export" ${TMPFILE} | sed "s/export //" >> $ENV_FILE
    # eliminate warning message "Invalid -W option ignored: invalid action: '"ignore'"
    echo "export PYTHONWARNINGS=default" >> $ENV_FILE

    docker-compose -f $script_dir/${TEST_SUITE}/docker-compose.yaml up -d
}
