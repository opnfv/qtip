#! /bin/bash
run_test_suite()
{
    if [ "$TEST_CASE" == "compute" ]; then
        cd ${QTIP_DIR}  && python qtip.py -l default -f compute
        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py compute
    elif [ "$TEST_CASE" == "storage" ]; then
        cd ${QTIP_DIR}  && python qtip.py -l default -f storage
        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py storage
    elif [ "$TEST_CASE" == "network" ]; then
        cd ${QTIP_DIR}  && python qtip.py -l default -f network
        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py network
    elif [ "$TEST_CASE" == "all" ]; then
        cd ${QTIP_DIR}  && python qtip.py -l default -f compute
        cd ${QTIP_DIR}  && python qtip.py -l default -f storage
        cd ${QTIP_DIR}  && python qtip.py -l default -f network

        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py compute
        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py storage
        cd ${QTIP_DIR} && python scripts/ref_results/suite_result.py network
    fi
}

source ${QTIP_DIR}/docker/prepare_qtip_image.sh

run_test_suite

source ${QTIP_DIR}/docker/cleanup_qtip_image.sh
