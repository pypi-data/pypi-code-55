import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Persistence" Movement'
        self.tid = 'T1084'
        self.name = 'Windows Management Instrumentation Event Subscription'
        self.description = '''Uses WMI to subscribe to an event and 
                                execute arbitrary code when that event occurs, 
                                providing persistence on a system'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*wmic(\.exe)?\s+(\/|-)NAMESPACE:.\\\\root\\subscription.\s+PATH\s+', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
                elif re.search('process:command_line .*mofcomp(\.exe)?.*\.mof.*', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break

        if cnt != 0:
            return self
        else:
            return False 