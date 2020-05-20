import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1121'
        self.name = 'Regsvcs/Regasm'
        self.description = '''Uses Regsvcs.exe/regasm.exe to execute malicious behavior'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('(process:command_line|process:name)\s.*\'(.*regsvcs(\.exe)?.+|.*regasm(\.exe)?.+)\'', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False