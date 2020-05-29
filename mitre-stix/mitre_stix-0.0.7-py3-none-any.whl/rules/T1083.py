import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1083'
        self.name = 'File and Directory Discovery'
        self.description = '''Search in specific locations of a host or network share for certain information within a file system'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:name\s.+\'cmd.exe\'.+process:command_line\s.+(dir|tree)(\s)?', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False