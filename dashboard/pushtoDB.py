import requests
import json
import datetime
import os
import sys
TEST_DB = 'http://testresults.opnfv.org/test/api/v1'

suite_list = [('compute_result.json', 'compute_test_suite'),
              ('network_result.json', 'network_test_suite'),
              ('storage_result.json', 'storage_test_suite')]
payload_list = {}


def push_results_to_db(db_url, case_name, payload, logger=None, pod_name="dell-pod1"):

    url = db_url + "/results"
    creation_date = str(datetime.datetime.utcnow().isoformat())
    installer = os.environ['INSTALLER_TYPE']
    pod_name = os.environ['NODE_NAME']

    params = {"project_name": "qtip", "case_name": case_name,
              "pod_name": pod_name, "installer": installer, "start_date": creation_date,
              "version": "test", "details": payload}

    headers = {'Content-Type': 'application/json'}
    print pod_name
    print installer
    print creation_date

    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        print r
        return True
    except:
        print "Error:", sys.exc_info()[0]
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
        print payload_list
        for suite, case in payload_list.items():
            with open('results/' + suite, 'r') as result_file:
                j = json.load(result_file)
            push_results_to_db(TEST_DB, case, j)
    elif not payload_list:
        print 'Results not found'


if __name__ == "__main__":
    main()
