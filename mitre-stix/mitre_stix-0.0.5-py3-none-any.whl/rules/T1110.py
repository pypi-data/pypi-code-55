import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Credential Access'
        self.tid = 'T1110'
        self.name = 'Brute Force'
        self.description = '''Use brute force techniques to attempt access to accounts when
                        passwords are unknown or when password hashes are obtained.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*\_BRUTEFORCE\_', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False 