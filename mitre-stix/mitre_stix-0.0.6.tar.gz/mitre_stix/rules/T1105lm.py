import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Lateral Movement'
        self.tid = 'T1105'
        self.name = 'Remote File Copy'
        self.description = '''Copies files from external sources'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('(process:command_line .*certutil(\.exe)?\s+(?=.*-urlcache)(?=.*-split)(?=.*-f).+)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break

            if entry['type'] == 'malware':
                if re.search('.*\_DOWNLOAD\_', entry['name']):
                    o_id = entry['id']
                    s_ref = None
                    for o in bundles['objects']:
                        if o['type'] == 'relationship':
                            if o['target_ref'] == o_id and o['relationship_type'] == 'uses':
                                s_ref = o['source_ref']
                                break
                    if s_ref:
                        for o_rto in bundles['objects']:
                            if o_rto['type'] == 'relationship':
                                if o_rto['target_ref'] == s_ref and o_rto['relationship_type'] == 'related-to':
                                    is_ref = o_rto['source_ref']
                                    for indicator in bundles['objects']:
                                        if indicator['type'] == 'indicator':
                                            if re.search('http|https', indicator['name']):
                                                self.oid.append(o_id)
                                                cnt += 1
                                                break
                                            if re.search('(172\.([1][6-9]|2[0-9]|3[0-1])|10\.[0-9]+|192\.168)\.[0-9]+\.[0-9]+', indicator['name']):
                                                cnt = 0
                                                break
                                            else:
                                                self.oid.append(o_id)
                                                cnt += 1
                                                break

        if cnt != 0:
            return self
        else:
            return False 