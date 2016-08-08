from func.ansible_api import AnsibleApi


class TestClass:
    def test_call_ansible_api_success(self):
        ansible_api = AnsibleApi()
        ret = ansible_api.execut_playbook('tests/data/hosts', 'tests/data/test.yml', 'data/QtipKey', {'keys': 'test'})
        assert ret == 3
