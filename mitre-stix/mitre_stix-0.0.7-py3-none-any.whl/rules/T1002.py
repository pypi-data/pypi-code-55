import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Exfiltration'
        self.tid = 'T1002'
        self.name = 'Data Compressed'
        self.description = '''Compress data that is collected prior to exfiltration in order to make it portable and minimize the amount of data sent over the network.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*(powershell(\.exe)? .*(-Recursive|Compress-Archive)|(rar|7z|7za)(\.exe)? .*a .*)', entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False