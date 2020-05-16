import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defensive Evasion'
        self.tid = 'T1108'
        self.name = 'Redundant Access'
        self.description = '''Use more than one remote access tool with varying command
                            and control protocols or credentialed access to remote 
                            services so they can maintain access if an access mechanism 
                            is detected or mitigated.'''
                            
    def run_rules(self, bundles):
        cnt = 0
        redundant_score = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*\_WEBSHELL\_', entry['name']) and redundant_score == 0:
                    redundant_score += 1
                    continue
                elif re.search('.*\_WEBSHELL\_', entry['name']) and redundant_score >= 1:     
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False