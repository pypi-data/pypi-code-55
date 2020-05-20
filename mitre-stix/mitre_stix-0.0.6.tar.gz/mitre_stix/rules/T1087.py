import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1087'
        self.name = 'Account Discovery'
        self.description = '''Acquire listing of local system or domain accounts'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+((query\s+user|whoami|dsquery\s+(user|\*)|net\s+(view.+|user|group|localgroup))\s|cmdkey\s\/list)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
                elif re.search('process:name\s.+\'powershell(\.exe)?\'',entry['pattern'], re.IGNORECASE):
                    if re.search('process:command_line\s.+(get\-localuser|get\-localgroupmembers|get\-aduser).+',entry['entry'], re.IGNORECASE):
                        self.oid.append(entry['id'])
                        cnt += 1
                        break
        if cnt != 0:
            return self
        else:
            return False