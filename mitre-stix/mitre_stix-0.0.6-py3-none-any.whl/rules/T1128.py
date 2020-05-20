import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1128'
        self.name = 'Netsh Helper DLL'
        self.description = '''Uses netsh.exe with helper DLLs to proxy execution of arbitrary code'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*netsh(\.exe)?\s+add\s+helper\s.+\.dll.*', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False 