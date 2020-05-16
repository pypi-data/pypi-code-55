import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1136'
        self.name = 'Create Account'
        self.description = '''Creates an account for persistence'''
        

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line ((.*net +user.+\/add.*)|(.*net localgroup.+[a-z0-9]+.[a-z0-9]+.*\/add.*))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False 