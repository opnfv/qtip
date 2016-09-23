#! /bin/bash
run_test_suite()
{
if [ "$TEST_CASE" == "compute" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f compute
    cd ${QTIP_DIR}/data/ref_results/ && python compute_suite.py
elif [ "$TEST_CASE" == "storage" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f storage
    cd ${QTIP_DIR}/data/ref_results/ && python storage_suite.py
elif [ "$TEST_CASE" == "network" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f network
    cd ${QTIP_DIR}/data/ref_results/ && python network_suite.py
elif [ "$TEST_CASE" == "all" ]; then
    cd ${QTIP_DIR}  && python qtip.py -l default -f compute
    cd ${QTIP_DIR}  && python qtip.py -l default -f storage
    cd ${QTIP_DIR}  && python qtip.py -l default -f network

    cd ${QTIP_DIR}/data/ref_results/ && python compute_suite.py
    cd ${QTIP_DIR}/data/ref_results/ && python storage_suite.py
    cd ${QTIP_DIR}/data/ref_results/ && python network_suite.py
fi
}

source ${QTIP_DIR}/docker/prepare_qtip_image.sh

run_test_suite

source ${QTIP_DIR}/docker/cleanup_qtip_image.sh

