import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Initial Access'
        self.tid = 'T1189'
        self.name = 'Drive-by Compromise'
        self.description = '''A drive-by compromise is when an adversary gains 
                            access to a system through a user visiting a 
                            website over the normal course of browsing. With 
                            this technique, the user's web browser is 
                            typically targeted for exploitation, but 
                            adversaries may also use compromised websites 
                            for non-exploitation behavior such as acquiring 
                            application access tokens.'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'attack-pattern':
                if re.search('HTTP\_[a-zA-Z]+_EK', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False