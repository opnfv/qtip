import requests
import json
import os
TEST_DB = 'http://213.77.62.197'



def push_results_to_db(db_url=TEST_DB, case_name, logger=None, pod_name='dell-us-testing-bm-1', payload):
    url = db_url + "/results"
    installer = get_installer_type(logger)
    params = {"project_name": "functest", "case_name": case_name,
              "pod_name": os.environ[''], "installer": installer,
              "version": git_version, "details": payload}

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, data=json.dumps(params), headers=headers)
        logger.debug(r)
        return True
    except:
        print "Error:", sys.exc_info()[0]
        return False
        
