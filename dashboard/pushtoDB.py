import requests
import json
import datetime
import os
import sys
from utils import logger_utils

logger = logger_utils.QtipLogger('push_db').get

TEST_DB = 'http://testresults.opnfv.org/test/api/v1'

suite_list = [('compute_result.json', 'compute_test_suite'),
              ('network_result.json', 'network_test_suite'),
              ('storage_result.json', 'storage_test_suite')]
payload_list = {}


def push_results_to_db(db_url, case_name, payload, installer, pod_name):

    url = db_url + "/results"
    creation_date = str(datetime.datetime.utcnow().isoformat())

    params = {"project_name": "qtip", "case_name": case_name,
              "pod_name": pod_name, "installer": installer, "start_date": creation_date,
              "version": "test", "details": payload}

    headers = {'Content-Type': 'application/json'}
    logger.info('pod_name:{0},installer:{1},creation_data:{2}'.format(pod_name,
                                                                      installer,
                                                                      creation_date))
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        logger.info(r)
        return True
    except:
        logger.info("Error:{0}".format(sys.exc_info()[0]))
        return False


def populate_payload(suite_list):

    global payload_list
    for k, v in suite_list:

        if os.path.isfile('results/' + str(k)):
            payload_list[k] = v


def main():

    global payload_list
    populate_payload(suite_list)
    if payload_list:
        logger.info(payload_list)
        for suite, case in payload_list.items():
            with open('results/' + suite, 'r') as result_file:
                j = json.load(result_file)
            push_results_to_db(TEST_DB, case, j,
                               os.environ['INSTALLER_TYPE'],
                               os.environ['NODE_NAME'])
    elif not payload_list:
        logger.info('Results not found')


if __name__ == "__main__":
    main()
