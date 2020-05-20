import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Execution'
        self.tid = 'T1086'
        self.name = 'PowerShell'
        self.description = '''PowerShell is a powerful interactive command-line interface and 
                            scripting environment included in the Windows operating system. 
                            Adversaries can use PowerShell to perform a number of actions, 
                            including discovery of information and execution of code. Examples 
                            include the Start-Process cmdlet which can be used to run an 
                            executable and the Invoke-Command cmdlet which runs a command 
                            locally or on a remote computer.'''

    def run_rules(self, bundles):
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('process:command_line .+ \'(powershell\.exe)\'', entry['pattern'], re.IGNORECASE):
                    self.oid.append(entry['id'])
                    cnt += 1
        if cnt != 0:
            return self
        else:
            return False
