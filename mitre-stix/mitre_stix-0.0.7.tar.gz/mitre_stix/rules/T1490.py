import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Impact'
        self.tid = 'T1490'
        self.name = 'Inhibit System Recovery'
        self.description = '''Delete or remove built-in operating system data  
                            and turn off services designed to aid in the recovery 
                            of a corrupted system to prevent recovery'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+(vssadmin(\.exe)?\sdelete\sshadows\s|wmic(\.exe)?\sshadowcopy\sdelete|bcdedit(\.exe)?\s\/set\s.+(bootstatuspolicy\signoreallfailures|recoveryenabled\sno)|wbadmin(\.exe)?\sdelete\s)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False