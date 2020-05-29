import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Lateral Movement'
        self.tid = 'T1184'
        self.name = 'SSH Hijacking'
        self.description = '''Connect to another system via an encrypted tunnel, 
                            commonly authenticating through a password, certificate 
                            or the use of an asymmetric encryption key pair.'''
                            
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*\_SSH\_', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False