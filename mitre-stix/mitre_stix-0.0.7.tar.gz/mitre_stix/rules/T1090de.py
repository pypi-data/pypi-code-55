import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1090'
        self.name = 'Connection Proxy'
        self.description = '''Use a connection proxy to direct network traffic 
                            between systems or act as an intermediary for network 
                            communications to a command and control server to 
                            avoid direct connections to their infrastructure'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'attack-pattern':
                if re.search('HTTP\_PROXY', entry['name']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False