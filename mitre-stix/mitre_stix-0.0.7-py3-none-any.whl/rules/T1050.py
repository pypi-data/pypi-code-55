import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1050'
        self.name = 'New Service'
        self.description = '''Creates and/or starts a new service'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*((sc|net)(\.exe)?\s.*create.+)|(psexec(\.exe)?\s*-r.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False 