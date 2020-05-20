import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Credential Access'
        self.tid = 'T1187'
        self.name = 'Forced Authentication'
        self.description = '''The Server Message Block (SMB) protocol is commonly used in Windows
                            networks for authentication and communication between systems for access 
                            to resources and file sharing. When a Windows system attempts to connect 
                            to an SMB resource it will automatically attempt to authenticate and send 
                            credential information for the current user to the remote system.'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*_SMB\_', entry['name']):
                    o_id = entry['id']
                    for o in bundles['objects']:
                        if o['type'] == 'relationship':
                            if o['source_ref'] == o_id and o['relationship_type'] == 'target':
                                s_id = o['target_ref']
                                break
                    else:
                        s_id = False
                    if s_id != False:
                        for o_r in bundles['objects']:
                            if o_r['type'] == 'identity':
                                if o_r['id'] == s_id:
                                    if re.search('(172\.([1][6-9]|2[0-9]|3[0-1])|10\.[0-9]+|192\.168)\.[0-9]+\.[0-9]+', o_r['name']):
                                         self.oid.append(o_id)
                                         cnt += 1

        if cnt != 0:
            return self
        else:
            return False