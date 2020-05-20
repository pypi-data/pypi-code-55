import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Discovery'
        self.tid = 'T1069'
        self.name = 'Permission Groups Discovery'
        self.description = '''Find local system or domain-level groups and permissions settings.'''
        

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line ((.*net(\.exe)? +user.*)|(.*net(\.exe)? +localgroup.*)|(.*net(\.exe)? +group.*)|(.*get\-localgroup.*)|(.*get\-ADPrinicipalGroupMembership.*))', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False 