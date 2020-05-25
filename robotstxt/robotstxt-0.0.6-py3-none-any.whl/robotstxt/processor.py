import re
import operator
from .robots_processing import is_valid_url, robots_rule_to_regex, select_rule_block, get_url_path
from urllib.parse import unquote
import json
import hashlib
import datetime

def robots_file(content):
    return RobotsFile(content)

def hash_generator(value_to_hash):
    return hashlib.sha1(str(value_to_hash).encode('utf-8')).hexdigest()

class RobotsFile:
    def __init__(self, contents):
        self.contents = contents
        self.sitemaps = []
        self.byte_size = len(self.contents.encode('utf-8'))
        self.size_exceeded = True if self.byte_size > 512000 else False
        self.hash_raw = hash_generator(self.contents)
        self.generated_datetime = datetime.datetime.utcnow()

        # Process the file for rules
        lines = self.contents.splitlines()
        user_agent_tokens = []
        user_agent_discovery = False
        user_agent_blocks = {}

        for line in lines:
            sitemap = re.search(r'sitemap:\s*(.*?)($|\s)', line, re.IGNORECASE)
            if sitemap:
                self.sitemaps.append(Sitemap(sitemap[1]))

            else:
                user_agent = re.search(r'user-agent:\s*(.*?)($|\s)', line, re.IGNORECASE)

                if user_agent:
                    if user_agent_discovery == True:
                        user_agent_tokens.append(user_agent[1].lower())
                    if user_agent_discovery == False:
                        user_agent_tokens = [user_agent[1].lower()]
                        user_agent_discovery = True
                else:
                    user_agent_discovery = False

                    disallow_rule = re.search(r'disallow:\s*(.*?)(?:$|\s|#)', line, re.IGNORECASE)
                    if disallow_rule:
                        for token in user_agent_tokens:
                            if token in user_agent_blocks:
                                user_agent_blocks[token].append(['Disallow', -len(disallow_rule[1]), disallow_rule[1], robots_rule_to_regex(disallow_rule[1])])

                            else:
                                user_agent_blocks[token] = [['Disallow', -len(disallow_rule[1]), disallow_rule[1], robots_rule_to_regex(disallow_rule[1])]]

                    else:
                        allow_rule = re.search(r'allow:\s*(.*?)($|\s)', line, re.IGNORECASE)
                        if allow_rule:
                            for token in user_agent_tokens:
                                if token in user_agent_blocks:
                                    user_agent_blocks[token].append(['Allow', -len(allow_rule[1]), allow_rule[1], robots_rule_to_regex(allow_rule[1])])

                                else:
                                    user_agent_blocks[token] = [['Allow', -len(allow_rule[1]), allow_rule[1], robots_rule_to_regex(allow_rule[1])]]



        for user_agent_block in user_agent_blocks:

            user_agent_blocks[user_agent_block] = sorted(user_agent_blocks[user_agent_block],
                                                         key=operator.itemgetter(1, 0))


        self.rule_blocks = user_agent_blocks

        self.json = json.dumps(self.rule_blocks, sort_keys=True)
        self.hash_material = hash_generator(json.dumps(self.rule_blocks, sort_keys=True))

        # Generate a hash of the sitemaps
        sitemap_list = []
        for sitemap in self.sitemaps:
            sitemap_list.append(sitemap.url)
        sitemap_list.sort()
        self.hash_sitemaps = hash_generator(sitemap_list)

    def test_url(self, url, token):

        url_path_to_test = get_url_path(unquote(url))
        selected_block = select_rule_block(self.rule_blocks, token.lower())

        if selected_block:
            for rule in self.rule_blocks[selected_block]:
                if re.search(unquote(rule[3]), url_path_to_test):
                    if rule[0] == 'Disallow':
                        return {'disallowed': True, 'matching_rule': rule[2]}

                    else:
                            return {'disallowed': False, 'matching_rule': rule[2]}

            else:
                return {'disallowed': False, 'matching_rule': None}
        else:
            return {'disallowed': False, 'matching_rule': None}

class Sitemap:
    def __init__(self, url):
        self.url = url
        self.valid_url = True if is_valid_url(self.url) else False
