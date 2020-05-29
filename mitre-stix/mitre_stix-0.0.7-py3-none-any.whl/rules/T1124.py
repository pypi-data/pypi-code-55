import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1124'
        self.name = 'System Time Discovery'
        self.description = '''Gathers the system time and/or time zone from a local or remote system'''

    def run_rules(self, bundles):
        cnt = 0
        command_ptn = [
            r"process:command_line\s.+net(\.exe)? +time .+",
            r"process:command_line\s.+w32tm(\.exe)? +\/tz.*",
            r"process:command_line\s.+powershell(\.exe)? +Get-Date.*",
            r"process:command_line\s.+(date|time)(\.exe)? *\/T.*"
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