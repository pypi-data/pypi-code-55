import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1063'
        self.name = 'Security Software Discovery'
        self.description = '''Attempts to identify installed AV products by installation directory'''

    def run_rules(self, bundles):
        softwaredisc_ptn = [
            r'process:command_line\s.+wmic(\.exe)?.+(SELECT * FROM (AntiVirusProduct|AntiSpywareProduct|FirewallProduct))|(\\\\root\\SecurityCenter2\sPath\sAntiVirusProduct.+)',
            r'process:command_line\s.+((netsh\sadvfirewall\sfirewall\sshow\s.+)|(.+get-netfirewallrule\s.+))',
        ]
        indicator_ptn = '|'.join(softwaredisc_ptn)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search(indicator_ptn, entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False