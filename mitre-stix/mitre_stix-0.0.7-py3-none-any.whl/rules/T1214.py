import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Credential Access'
        self.tid = 'T1214'
        self.name = 'Credentials in Registry'
        self.description = '''Queries the registry for credentials and passwords.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+(reg.+query.+(HKLM|HKCU).+\/f.+password.+\/t.+REG_SZ.+\/s|Get\-UnattendedInstallFile|Get\-Webconfig|Get\-ApplicationHost|Get\-SiteListPassword|Get\-CachedGPPPassword|Get\-RegistryAutoLogon)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False