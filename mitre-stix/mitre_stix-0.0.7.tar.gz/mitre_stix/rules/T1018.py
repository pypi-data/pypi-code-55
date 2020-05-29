import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1018'
        self.name = 'Remote System Discovery'
        self.description = '''Attempts to get a listing of other systems by IP address, hostname, or other logical identifier on a network'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+(?=.*ping(\.exe)?\s+)(?!.*(localhost|127\.0\.0\.1))|(net(\.exe)?\s+view)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False