import os
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor


class AnsibleApi:

    def __init__(self):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = {}
        self.pbex = None

    def _check_path(self, file_path):
        if not os.path.exists(file_path):
            print '[INFO] The playbook %s does not exist' % file_path
            return False
        else:
            return True

    def execut_playbook(self, hosts_file, playbook_path, pub_key_file, vars):
        if not self._check_path(hosts_file):
            return False

        inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=hosts_file)
        Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='root', private_key_file=pub_key_file, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)
        self.variable_manager.extra_vars = vars

        self.pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=self.variable_manager, loader=self.loader, options=options, passwords=self.passwords)

        return self.pbex.run()

    def get_detail_playbook_stats(self):
        if self.pbex:
            stats = self.pbex._tqm._stats
            return map(lambda x: (x, stats.summarize(x)), stats.processed.keys())
        else:
            return None
