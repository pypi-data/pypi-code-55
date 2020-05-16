import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Credential Access'
        self.tid = 'T1081'
        self.name = 'Credentials in Files'
        self.description = '''Queries the files for credentials and passwords.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+(findstr.+\s\/si\spass|select\-string\s\-pattern\spass|list\svdir.+\/test\:password.+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False