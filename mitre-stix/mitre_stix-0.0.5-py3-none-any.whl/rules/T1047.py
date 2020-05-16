import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1047'
        self.name = 'Windows Management Instrumentation'
        self.description = '''Uses WMI to execute malicious behavior'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .+ \'.*wmic.+.*\'', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False