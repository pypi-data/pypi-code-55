import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1216'
        self.name = 'Signed Script Proxy Execution'
        self.description = '''Scripts signed with trusted certificates can be used to proxy execution of malicious files'''

    def run_rules(self, bundles):
        proc = [ 
            r".*Windows\\System32\\.*\\pubprn\.vbs .+", 
            r".*pubprn\.vbs .+",
            r".*Windows\\System32\\SyncAppvPublishingServer\.vbs .+" 
            r".*cscript\.exe .+"
        ]
        proc_list = "|".join(proc)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line' + proc_list, entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False