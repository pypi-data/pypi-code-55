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
			r'.*wscript(\.exe)?',
            r'.*cmd(\.exe)? (\/c)? .+',
			r'.*wscript(\.exe)? .+',
			r'.*powershell(\.exe)?',
			r'.*powershell(\.exe)? .+',
			r'.*cmd(\.exe)?(\')? (\/c)? .*\.bat',
			r'.*cmd(\.exe)? (\/c)?  .*\.lnk',
			r'.*cmd(\.exe)?(\')? (\/c)?  .*\.ps1',
			r'.*cmd(\.exe)? (\/c)?  .*\.vba',
			r'.*cmd(\.exe)? (\/c)?  .*\.js',
			r'.*cmd(\.exe)?(\')? (\/c)? .* -executionpolicy (bypass)?',
			r'.*cmd(\.exe)?(\')? (\/c)? .* -ep bypass .+',
			r'.*\.vbs(.*)?',
			r'.*\.js(.*)?',
			r'.*\.ps1(.*)?',
			r'.*\.bat(.*)?',
			r'.*\.lnk(.*)?',
			r'.*\.vbe(.*)?'
		]
        proc_list = '|'.join(proc)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('(process:command_line\s|process:name\s)' + proc_list, entry['pattern'], re.IGNORECASE):
                    if re.search('process:command_line .*((powershell(\.exe)?.+frombase64string|\-e(n(c(o(d(e(d(c(o(m(m(a(n(d)?)?)?)?)?)?)?)?)?)?)?)?)?)|(certutil(\.exe)?.+-decode))\s.+', entry['pattern'], re.IGNORECASE):
                        self.oid.append(entry['id'])
                        cnt += 1
        if cnt != 0:
            return self
        else:
            return False