import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1202'
        self.name = 'Indirect Command Execution'
        self.description = '''Uses various Windows utilities to execute commands, possibly without invoking cmd.'''
        
    def run_rules(self, bundles):
        indirect = [r"forfiles(\.exe)? /p (:\\)+.* /m .+\..+ /c .*",
                    r"pcalua(\.exe)? -a .+\..+"]
        indicator_ptn = "|".join(indirect)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*'+ indicator_ptn, entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False