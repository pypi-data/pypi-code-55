import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1117'
        self.name = 'Regsvr32'
        self.description = '''Register and unregister object linking and embedding controls'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:name\s.+\'regsvr32(\.exe)?\'', entry['pattern'], re.IGNORECASE):
                    if 'object' in entry['labels']:
                        self.oid.append(entry['id'])
                        cnt += 1
        if cnt != 0:
            return self
        else:
            return False