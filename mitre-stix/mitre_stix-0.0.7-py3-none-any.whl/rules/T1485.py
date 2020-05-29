import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Impact'
        self.tid = 'T1485'
        self.name = 'Data Destruction'
        self.description = '''Destroy data and files on specific systems 
                            or in large numbers on a network to interrupt 
                            availability to systems, services, and network 
                            resources'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+sdelete(\.exe)?\s.+\-(p|s|c|r|z)\s.+', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False