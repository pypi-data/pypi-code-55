import re

class mitre_rules():
    def __init__(self):
        self.oid = []
        self.tactic = 'Defense Evasion'
        self.tid = 'T1102'
        self.name = 'Web Service'
        self.description = '''Uses an existing, legitimate external web service as a means for relaying commands to a compromised system.'''
        
    def run_rules(self, bundles):
        web_services = [
            "amazon",
            "wordpress",
            "twitter",
            "dropbox",
            "github",
            "tumblr",
            "blogspot",
            "pastebin",
            "evernote",
            "yandex",
            "mediafire",
            "pcloud"
        ]
        indicator_ptn = "|".join(web_services)
        cnt = 0
        for entry in bundles['objects']:
            if entry['type'] == 'indicator':
                if re.search('url:extensions\.domain \= \'.*'+ indicator_ptn, entry['pattern']):
                    self.oid.append(entry['id'])
                    cnt += 1
                    break
        if cnt != 0:
            return self
        else:
            return False