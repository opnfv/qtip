#! /bin/bash

IMGNAME='QTIP_CentOS.qcow2'
IMGPATH='/home/opnfv/imgstore'
IMGURL='http://build.opnfv.org/artifacts.opnfv.org/qtip/QTIP_CentOS.qcow2'

load_image()
{
    test -d $IMGPATH || mkdir -p $IMGPATH
    if [[ ! -f "$IMGPATH/$IMGNAME" ]];then
        echo
        echo "========== Downloading QTIP_CentOS image =========="
        cd $IMGPATH
        wget -c --progress=dot:giga $IMGURL
    fi

    echo
    echo "========== Loading QTIP_CentOS image =========="
    output=$(glance image-create \
        --name QTIP_CentOS \
        --visibility public \
        --disk-format qcow2 \
        --container-format bare \
        --file $IMGPATH/$IMGNAME )
    echo "$output"

    IMAGE_ID=$(echo "$output" | grep " id " | awk '{print $(NF-1)}')

    if [ -z "$IMAGE_ID" ]; then
        echo 'Failed uploading QTIP_CentOS image to cloud'.
        exit 1
    fi

    echo "QTIP_CentOS image id: $IMAGE_ID"
}

cleanup_image()
{
    echo

    if ! glance image-list; then
        return
    fi

    echo "Deleting image QTIP_CentOS..."
    glance image-delete $(glance image-list | grep -e QTIP_CentOS | awk '{print $2}')

}

cp ${REPOS_DIR}/releng/utils/fetch_os_creds.sh ${QTIP_DIR}/data/
cd ${QTIP_DIR}  &&  source get_env_info.sh \
-n ${INSTALLER_TYPE} \
-i ${INSTALLER_IP}

source ${QTIP_DIR}/opnfv-creds.sh

load_image

if [ "$TEST_CASE" == "compute" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f compute
    cd ${QTIP_DIR}/data/ref_results/ && python compute_suite.py
fi

if [ "$TEST_CASE" == "storage" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f storage
    cd ${QTIP_DIR}/data/ref_results/ && python storage_suite.py
fi

if [ "$TEST_CASE" == "network" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f network
    cd ${QTIP_DIR}/data/ref_results/ && python network_suite.py
fi


if [ "$TEST_CASE" == "all" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f compute
    cd ${QTIP_DIR}  && python qtip.py -l default -f storage
    cd ${QTIP_DIR}  && python qtip.py -l default -f network

    cd ${QTIP_DIR}/data/ref_results/ && python compute_suite.py
    cd ${QTIP_DIR}/data/ref_results/ && python storage_suite.py
    cd ${QTIP_DIR}/data/ref_results/ && python network_suite.py
fi

cleanup_image
