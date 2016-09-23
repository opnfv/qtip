#!/bin/bash
IMGNAME='QTIP_CentOS.qcow2'
IMGPATH='/home/opnfv/imgstore'
IMGURL='http://build.opnfv.org/artifacts.opnfv.org/qtip/QTIP_CentOS.qcow2'

load_image()
{
    if [[ -n $( glance image-list | grep -e QTIP_CentOS) ]]; then
        return
    fi

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

rm -rf ${QTIP_DIR}/openrc

${REPOS_DIR}/releng/utils/fetch_os_creds.sh \
-d ${QTIP_DIR}/openrc \
-i ${INSTALLER_TYPE} \
-a ${INSTALLER_IP}

source ${QTIP_DIR}/openrc

load_image
