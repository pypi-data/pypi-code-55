import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Initial Access'
        self.tid = 'T1190'
        self.name = 'Exploit Public-Facing Application'
        self.description = 'The use of software, data, or commands to take advantage of a weakness in an '+\
                            'Internet-facing computer system or program in order to cause unintended or '+\
                            'unanticipated behavior. The weakness in the system can be a bug, a glitch, '+\
                            'or a design vulnerability. These applications are often websites, '+\
                            'but can include databases (like SQL), standard services (like SMB or SSH), '+\
                            'and any other applications with Internet accessible open sockets, such as web '+\
                            'servers and related services. Depending on the flaw being exploited this may '+\
                            'include Exploitation for Defense Evasion.'

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
##                                print s_id
                                break
                    else:
                        s_id = False
                    if s_id != False:
                        for o_r in bundles['objects']:
                            if o_r['type'] == 'identity':
                                if o_r['id'] == s_id:
                                    if re.search('(172\.([1][6-9]|2[0-9]|3[0-1])|10\.[0-9]+|192\.168)\.[0-9]+\.[0-9]+', o_r['name']):
                                        i = False
                                    else:
                                        self.oid.append(o_id)
                                        cnt += 1
                                    break
                                
##                        if i is True:
##                            for o_r in bundles['objects']:
##                                if o_r['type'] == 'relationship':
##                                    if o_r['source_ref'] == s_id:
##                                        t_id = o_r['target_ref']
##    ##                                    print t_id
##                                        break
##                            else:
##                                t_id = False
##                            if t_id != False:
##                                for o_r in bundles['objects']:
##                                    if o_r['id'] == t_id:
##                                        if o_r['type'] == 'indicator':
##                                            self.oid.append(o_id)
##                                            cnt += 1
##                                            break
                                

        if cnt != 0:
            return self
        else:
            return False
                            

            
