import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1007'
        self.name = 'System Service Discovery'
        self.description = '''Gets information about registered services'''

    def run_rules(self, bundles):
        cnt = 0
        command_ptn = [
            r"process:command_line\s(.+\\sc\.exe|(.+sc(\.exe)?)) +query.*",
            r"process:command_line\s.+tasklist(\.exe)? +\/svc.*",
            r"process:command_line\s.+net(\.exe)? +start( *>>.+)?$",
            r"process:command_line\s.+wmic(\.exe)? + service.*"
        ]
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('|'.join(command_ptn), entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False