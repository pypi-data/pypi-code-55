import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1003'
        self.name = 'Credential Dumping'
        self.description = '''Obtaining sensitive login information of users normally 
                            in the form of a hash or a clear text password, from the 
                            operating system and software.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('(process:name.+\'reg.exe\'.+process:command_line.+(save.+HKLM\\\\sam.+|save.+HKLM\\\\system.+)|process:command_line.+(Invoke\s\-Mimikatz\s\-DumpCreds|gsecdump\s\-a|wce\s\-o|procdump\s\-ma\slsass(\.exe)?|ntdsutil.+ac\si\sntds.+ifm.+create full))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False