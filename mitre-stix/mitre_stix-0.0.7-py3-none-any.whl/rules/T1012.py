import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1012'
        self.name = 'Query Registry'
        self.description = '''Interacts with the Windows Registry to gather information
                            about the system, configuration, and installed software'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+reg(\.exe)?\s+query\s.+', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False