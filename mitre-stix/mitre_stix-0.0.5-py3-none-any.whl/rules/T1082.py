import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1082'
        self.name = 'System Information Discovery'
        self.description = '''Attempt to get detailed information about the operating system and hardware, including version, patches, hotfixes, service packs, and architecture.'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line (.*sysinfo.exe|reg.exe).*(query.*HKLM\\\\SYSTEM\\\\CurrentControlSet\\\\Services\\\\Disk\\\\Enum)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False