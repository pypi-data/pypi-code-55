import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1135'
        self.name = 'Network Share Discovery'
        self.description = '''Check shared network drives and folders'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:name\s.+\'net.exe\'.+process:command_line\s.+net\s+(share|view\s+\\remotesystem|get\-smbshare\s\-Name)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False