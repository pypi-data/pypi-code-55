import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defensive Evasion'
        self.tid = 'T1064'
        self.name = 'Scripting'
        self.description = '''Use of scripts to aid operations and perform multiple instructions'''

    def run_rules(self, bundles):
        proc = [
			r'(process:command_line\s|process:name\s).*wscript(\.exe)?',
            r'(process:command_line\s|process:name\s).*cmd(\.exe)? (\/c)? .+',
			r'(process:command_line\s|process:name\s).*wscript(\.exe)? .+',
			r'(process:command_line\s|process:name\s).*powershell(\.exe)?',
			r'(process:command_line\s|process:name\s).*powershell(\.exe)? .+',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)?(\')? (\/c)? .*\.bat',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)? (\/c)?  .*\.lnk',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)?(\')? (\/c)?  .*\.ps1',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)? (\/c)?  .*\.vba',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)? (\/c)?  .*\.js',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)?(\')? (\/c)? .* -executionpolicy (bypass)?',
			r'(process:command_line\s|process:name\s).*cmd(\.exe)?(\')? (\/c)? .* -ep bypass .+',
			r'(process:command_line\s|process:name\s).*\.vbs(.*)?',
			r'(process:command_line\s|process:name\s).*\.js(.*)?',
			r'(process:command_line\s|process:name\s).*\.ps1(.*)?',
			r'(process:command_line\s|process:name\s).*\.bat(.*)?',
			r'(process:command_line\s|process:name\s).*\.lnk(.*)?',
			r'(process:command_line\s|process:name\s).*\.vbe(.*)?'
		]
        proc_list = '|'.join(proc)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search(proc_list, entry['pattern'], re.IGNORECASE):
                    if re.search('process:command_line .*((powershell(\.exe)?.+frombase64string|\-e(n(c(o(d(e(d(c(o(m(m(a(n(d)?)?)?)?)?)?)?)?)?)?)?)?)?)|(certutil(\.exe)?.+-decode))\s.+', entry['pattern'], re.IGNORECASE):
                        self.oid.append(entry['id'])
                        cnt += 1
                        break
        if cnt != 0:
            return self
        else:
            return False