import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1053'
        self.name = 'Scheduled Task'
        self.description = '''Schedule programs or scripts to be executed at a date and time'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+(schtasks(\.exe)?.+\/create.+\/sc\s+.+|(.*at(\.exe)?.*(([0-1][0-9])|(2[0-3]))\:[0-5][0-9]))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False