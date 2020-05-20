import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1033'
        self.name = 'System Owner/User Discovery'
        self.description = '''Identifies the primary user, currently logged in user, 
                                or set of users that commonly uses a system'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .+ \'(whoami|systeminfo)(\.exe)?|(query(\.exe)?\s+user|net(\.exe)?\s+config\s+workstation)\'', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False