import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1054'
        self.name = 'Indicator Blocking'
        self.description = '''Block indicators or events captured by sensors to avoid detection.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*(netsh(\.exe)?\s*advfirewall set (allprofiles|currentprofile|domainprofile|privateprofile|publicprofile) state off)|(netsh(\.exe)?\s*firewall set opmode mode=disable)', entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False