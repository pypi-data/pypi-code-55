import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Lateral Movement'
        self.tid = 'T1077'
        self.name = 'Windows Admin Shares'
        self.description = '''Use of network shares to propagate'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(net\s+use\s.+|net\sshare\s.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False