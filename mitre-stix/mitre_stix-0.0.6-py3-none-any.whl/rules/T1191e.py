import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1191'
        self.name = 'CMSTP'
        self.description = '''Uses cmstp.exe to execute malicious behavior'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('(process:command_line\s.*cmstp(\.exe)?\s.+|process:name\s.+\'cmstp\.exe\')', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False