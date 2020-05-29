import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1482'
        self.name = 'Domain Trust Discovery'
        self.description = '''Gathers information on domain trust relationships'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(nltest(\.exe)?\s+\/domain_trusts)|(dsquery(\.exe)?\s+\*\s+-filter\s+\"\(objectClass=trustedDomain\)\"\s+-attr\s+\*)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False