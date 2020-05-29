import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Collection'
        self.tid = 'T1119'
        self.name = 'Automated Collection'
        self.description = '''Uses automated techniques for collecting internal data'''

    def run_rules(self, bundles):
        exe = [
            "date",
            "dir",
            "hostname",
            "ipconfig",
            "net",
            "nltest",
            "query",
            "reg",
            "systeminfo",
            "time",
            "type",
            "ver",
            "whoami"
        ]
        exe_ptn = r"({0})(\.exe)?".format("|".join(exe))
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line\s.+' + exe_ptn, entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False