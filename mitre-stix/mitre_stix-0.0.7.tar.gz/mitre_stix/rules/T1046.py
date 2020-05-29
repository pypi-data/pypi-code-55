import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1046'
        self.name = 'Network Service Scanning'
        self.description = '''Acquires a list of services running on remote hosts, 
                            including those that may be vulnerable to exploitation'''
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*\_VULNERABILITY\_SCANNER\_', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False