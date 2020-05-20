import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Exfiltration'
        self.tid = 'T1070'
        self.name = 'Indicator Removal on Host'
        self.description = '''Adversaries may delete or alter generated artifacts on a host system.'''
        
    def run_rules(self, bundles):
        wevtutil_ptn = [
            r".*wevtutil?.+ cl system",
            r".*wevtutil?.+ cl application",
            r".*wevtutil?.+ cl security"
        ]
        indicator_ptn = "|".join(wevtutil_ptn)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*'+ indicator_ptn, entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False