import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Lateral Movement'
        self.tid = 'T1210'
        self.name = 'Exploitation of Remote Services'
        self.description = 'Exploitation of a software vulnerability occurs when ' + \
                            'an adversary takes advantage of a programming error' + \
                            'in a program, service, or within the operating system' +\
                            'software or kernel itself to execute adversary-controlled' +\
                            'code. A common goal for post-compromise exploitation of' +\
                            'remote services is for lateral movement to enable access' +\
                            'to a remote system.'

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'malware':
                if re.search('.*SMB\_.*EXPLOIT', entry['name']):
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