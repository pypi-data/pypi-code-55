import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Credential Access'
        self.tid = 'T1208'
        self.name = 'Kerberoasting'
        self.description = '''Attempt to acquire Kerberos tickets'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line.+(setspn\s+-T\s.+-Q\s+\*\/\*|servicePrincipalName|Where\s+\{\^\$_.servicePrincipalName}|KerberosRequestorSecurityToken|Invoke-Kerberoast)\s', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False