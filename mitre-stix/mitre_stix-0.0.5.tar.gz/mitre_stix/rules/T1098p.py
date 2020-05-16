import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1098'
        self.name = 'Account Manipulation'
        self.description = '''Manipulates accounts to gain/maintain credential access'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+((net +user.+\/add.*)|(net +user.+\/del.*)|(net +user.+[a-z0-9]+.[a-z0-9]+)|(.*net localgroup.+[a-z0-9]+.[a-z0-9]+.*\/add.*))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False