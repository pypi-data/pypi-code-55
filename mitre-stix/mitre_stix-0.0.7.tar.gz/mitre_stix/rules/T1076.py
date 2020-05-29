import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Lateral Movement'
        self.tid = 'T1076'
        self.name = 'Remote Desktop Protocol'
        self.description = '''Connect to a remote system over RDP/RDS'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(tscon|mstsc)(\.exe)?\s', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False