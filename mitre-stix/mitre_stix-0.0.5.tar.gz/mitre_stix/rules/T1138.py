import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1138'
        self.name = 'Application Shimming'
        self.description = '''Uses application shims to perform malicious routine'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+sdbinst(\.exe)?.+(\.sdb)|process:name.+\'sdbinst\.exe\'', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False