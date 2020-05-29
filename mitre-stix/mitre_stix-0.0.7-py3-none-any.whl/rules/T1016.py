import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1016'
        self.name = 'System Network Configuration Discovery'
        self.description = '''Acquires details about network configuration and settings of systems it accesses'''


    def run_rules(self, bundles):
        configdisc_ptn = [
            r'(process:command_line\s.+(nbtstat(\.exe)?\s+(-a|-e|-c|-n|-r)|route(\.exe)?)\s+command\s+PRINT|arp(\.exe)?\s+(-a|-g)|ipconfig(\.exe)?\s+(\/all|\/displaydns))',
            r'(process:command_line\s.+(wmic(\.exe)?\s+nic\s+get.+|Get-WmiObject\s+-Class\s+Win32_NetworkAdapterConfiguration.*|Get-WmiObject.+\.domain))',
        ]
        indicator_ptn = '|'.join(configdisc_ptn)
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