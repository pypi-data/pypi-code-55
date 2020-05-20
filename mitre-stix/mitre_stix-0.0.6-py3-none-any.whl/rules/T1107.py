import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1107'
        self.name = 'File Deletion'
        self.description = '''Deletes files and directories.'''
        
    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .*(remove\-item|vssadmin*Delete Shadows \/All \/Q|wmic.*shadowcopy delete|wbdadmin.* delete catalog \-q.*|bcdedit.*bootstatuspolicy ignoreallfailures.*|bcdedit.*recoveryenabled no.*)', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False