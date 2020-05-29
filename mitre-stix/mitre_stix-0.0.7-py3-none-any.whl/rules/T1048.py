import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Exfiltration'
        self.tid = 'T1048'
        self.name = 'Exfiltration Over Alternative Protocol'
        self.description = '''Data exfiltration is performed with a different
                            protocol from the main C2C protocol or channel'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(net use .*\&\&xcopy\s|echo PUT\s.+|\sftp\s.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False
