import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence'
        self.tid = 'T1100'
        self.name = 'Web Shell'
        self.description = '''A Web shell may provide a set of functions to 
                            execute or a command-line interface on the system 
                            that hosts the Web server.'''
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*\_WEBSHELL\_', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False