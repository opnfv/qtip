#!/bin/bash

if [[ ! -f ${QTIP_DIR}/openrc ]];then
    source ${REPOS_DIR}/releng/utils/fetch_os_creds.sh \
    -d ${QTIP_DIR}/openrc \
    -i ${INSTALLER_TYPE} \
    -a ${INSTALLER_IP}
fi

source ${QTIP_DIR}/openrc

cleanup_image()
{
    echo
    if ! glance image-list; then
        return
    fi

    echo "Deleting image QTIP_CentOS..."
    glance image-delete $(glance image-list | grep -e QTIP_CentOS | awk '{print $2}')

}

cleanup_image
