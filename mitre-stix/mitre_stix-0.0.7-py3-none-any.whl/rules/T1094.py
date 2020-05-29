import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Command And Control'
        self.tid = 'T1094'
        self.name = 'Custom Command and Control Protocol'
        self.description = '''Communicate using a custom command and control protocol 
                            instead of encapsulating commands/data in an existing 
                            Standard Application Layer Protocol'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'attack-pattern':
                if re.search('.*(\_CARBANAK\_|RAT\_|\_COBALT|EMOTET|\_PLUGX\_|\_URSNIF\_).*', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False