import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1064'
        self.name = 'Service Execution'
        self.description = '''Executes a binary, command, or script via a method that interacts with Windows services'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*((sc|net)(\.exe)?\s.*start.+)|(psexec(\.exe)?\s*-r.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False