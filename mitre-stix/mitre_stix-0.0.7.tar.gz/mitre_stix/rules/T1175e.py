import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1175'
        self.name = 'Component Object Model and Distributed COM'
        self.description = '''DCOM can also execute macros in existing documents and 
                            may also invoke (DDE) execution directly through a COM 
                            created instance of a Microsoft Office application'''

    def run_rules(self, bundles):
        cnt = 0
        office_ptn = [
            r"process:name\s.+\'winword\.exe\'",
            r"process:name\s.+\'excel\.exe\'",
            r"process:name\s.+\'outlook\.exe\'",
        ]
        is_office = False
        is_DCOM = False
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('|'.join(office_ptn), entry['pattern'], re.IGNORECASE):
                    is_office = True
                if re.search('process:command_line\s.+DcomLaunch', entry['pattern']):
                    is_DCOM = True
                    dcom_id = entry['id']
                if is_office and is_DCOM:
                    for o in bundles['objects']:
                        if o['type'] == 'relationship':
                            #get the id of indicator that Dcom created process
                            if o['target_ref'] == dcom_id and o['relationship_type'] == 'derived-from':
                                s_id = o['source_ref']
                                break
                    else:
                        s_id = False
                    if s_id != False:
                        for o_r in bundles['objects']:
                            if o_r['type'] == 'indicator':
                                if o_r['id'] == s_id:
                                    if re.search('process:command_line\s.+\-(embedding)', o_r['pattern'], re.IGNORECASE):
                                        self.oid.append(o_r['id'])
                                        cnt +=1
                                        break
        if cnt != 0:
            return self
        else:
            return False