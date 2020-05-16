import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1222'
        self.name = 'File Permissions Modification'
        self.description = '''Modifies file permissions/attributes'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*(attrib|cacls|icacls|taskown(\.exe)?)|(powershell(\.exe)?.+Set-Acl).+', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False