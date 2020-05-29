import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Command And Control'
        self.tid = 'T1102'
        self.name = 'Web Service'
        self.description = '''Uses an existing, legitimate external web service as a means for relaying commands to a compromised system.'''
        
    def run_rules(self, bundles):
        web_services = [
            "url:extensions\.domain \= \'.*amazon",
            "url:extensions\.domain \= \'.*wordpress",
            "url:extensions\.domain \= \'.*twitter",
            "url:extensions\.domain \= \'.*dropbox",
            "url:extensions\.domain \= \'.*github",
            "url:extensions\.domain \= \'.*tumblr",
            "url:extensions\.domain \= \'.*blogspot",
            "url:extensions\.domain \= \'.*pastebin",
            "url:extensions\.domain \= \'.*evernote",
            "url:extensions\.domain \= \'.*yandex",
            "url:extensions\.domain \= \'.*mediafire",
            "url:extensions\.domain \= \'.*pcloud"
        ]
        indicator_ptn = '|'.join(web_services)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search(indicator_ptn, entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False