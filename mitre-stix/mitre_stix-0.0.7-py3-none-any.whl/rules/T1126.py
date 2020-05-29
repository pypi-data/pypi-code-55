import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defence Evasion'
        self.tid = 'T1126'
        self.name = 'Network Share Connection Removal'
        self.description = '''Adversaries may remove share connections that are no 
                        longer useful in order to clean up traces of their operation'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*net +use +\\\\system\\\\share +\/delete', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False