import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1118'
        self.name = 'InstallUtil'
        self.description = '''Modifies or uninstalls resources using InstallUtil.exe'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process\:command_line .*installutil(\.exe)?\s(\/u|\/logfile\=|\/LogToConsole\=)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False