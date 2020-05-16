import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1059'
        self.name = 'Command-Line Interface'
        self.description = '''Interacts with the system via command line'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*cmd.exe\s+\/c', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False