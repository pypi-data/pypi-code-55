import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1218'
        self.name = 'Signed Binary Proxy Execution'
        self.description = '''Use of Microsoft Signed Binaries to execute malicious code'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*msiexec(\.exe)?.+.*((\.msi)|(\.dll))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                elif re.search('process:command_line (.*mavinject(\.exe)?.+|.*SyncAppvPublishingServer(\.exe)?.+|.*odbcconf(\.exe)?.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False