#!/usr/bin/env bash

# detect installer_ip
case ${INSTALLER_TYPE} in
    apex)
        export INSTALLER_IP=$(sudo virsh domifaddr undercloud | grep ipv4 | awk '{print $4}' | cut -d/ -f1)
        ;;
esac

export ENV_FILE="${ENV_FILE:-$(pwd)/env_file}"
cat << EOF > $ENV_FILE
INSTALLER_TYPE=${INSTALLER_TYPE}
INSTALLER_IP=${INSTALLER_IP}
TEST_SUITE=${TEST_SUITE}
NODE_NAME=${NODE_NAME:-opnfv-pod}
SCENARIO=${DEPLOY_SCENARIO:-generic}
TESTAPI_URL=${TESTAPI_URL:-}
OPNFV_RELEASE=${OPNFV_RELEASE:-}
EOF

export SSH_CREDENTIALS=${SSH_CREDENTIALS:-/root/.ssh}
export IMAGE_DIR=${IMAGE_DIR:-$HOME/tmp}

TMPFILE=`mktemp /tmp/qtip.XXXXXX` || exit 1
curl https://git.opnfv.org/releng/plain/utils/fetch_os_creds.sh | bash -s -- \
    -i ${INSTALLER_TYPE} -a ${INSTALLER_IP} -d ${TMPFILE}
grep "export" ${TMPFILE} | sed "s/export //" >> $ENV_FILE
# eliminate warning message "Invalid -W option ignored: invalid action: '"ignore'"
sed -i '/^PYTHONWARNINGS=/d' $ENV_FILE

# In CI job, it still uses fuel to represent MCP.
if [[ "${BRANCH}" =~ "master" && "${INSTALLER_TYPE}" =~ "fuel" ]];then
   sed -i 's/^INSTALLER_TYPE=fuel/INSTALLER_TYPE=mcp/g' $ENV_FILE
fi

docker-compose -f $script_dir/${TEST_SUITE}/docker-compose.yaml pull
docker-compose -f $script_dir/${TEST_SUITE}/docker-compose.yaml up -d
