import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1049'
        self.name = 'System Network Connections Discovery'
        self.description = '''Acquire listing of network connections to or from compromised system'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(netstat|arp\s+-a|net\s+(use|file|session)|Get-NetTCPConnection)\s', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False