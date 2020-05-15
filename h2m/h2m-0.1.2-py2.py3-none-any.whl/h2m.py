"""Main module."""

import re
import logging
from html.parser import HTMLParser
from html.entities import name2codepoint
from inspect import isfunction

ESCAPE_MAP = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": "\"",
    "&#x27;": "'",
    "&#x60;": "`",
    "&nbsp;": " ",
    "&#8202;": " "
}


def unescape(html_string):
    r_str = f'({"|".join(ESCAPE_MAP.keys())})'
    r = re.compile(r_str)
    return re.sub(r, lambda m: ESCAPE_MAP[m.group()], html_string)


LI_HEADER = 'H2M_LI_HEADER'


def convert_a(node):
    text = node.get('md', node.get('attrs', {'href': ''}).get('href'))
    text = text.replace('\n', '')
    href = node.get('attrs', {'href': text}).get('href')
    return f"[{text}]({href})"


def convert_img(node):
    attrs = node.get('attrs', {'title': '', 'alt': '', 'src': ''})
    title = attrs.get('title', attrs.get('alt', ''))
    src = attrs.get('src', '')

    if title == '' and src == '':
        return ''

    return f"![{title}]({src})"


def convert_ul(node):
    return f"\n{str(node['md']).replace(LI_HEADER, '-')}"


def convert_ol(node):
    i = 1
    count = node['md'].count(LI_HEADER)
    while i <= count:
        node['md'] = str(node['md']).replace(LI_HEADER, f"{i}.", 1)
        i = i + 1

    return f"\n{node['md']}"


def convert_pre(node):
    md = node.get('md', None)
    if md:
        return ''.join(map(lambda line: f'    {line}\n', md.split('\n')))
    return f"\n{md}\n"


def convert_code(node):
    md = node['md']
    if node.get('is_in_pre_node', False):
        return md
    return f'`{md}`'


def convert_blockquote(node):
    r_str = '(^(\n+))|((\n+)$)'
    r = re.compile(r_str)
    md = node.get('md')
    # md = re.sub(r, '', md)
    md = ''.join(map(lambda line: f"> {re.sub(r, '', line)}\n", md.split('\n')))
    return f'\n{md}\n'


# 表格相关开始
is_handle_thead_char = False
is_th = False
is_tr = False
tr_count = 0
th_count = 0


def reset_table():
    is_handle_thead_char = False
    is_tr = False
    is_th = False
    tr_count = 0
    th_count = 0


def get_thead_char():
    thead_char = '|'
    i = th_count
    while i > 0:
        thead_char = f"{thead_char}--------|"
        i = i - 1


def convert_table(node):
    thead_char = ""
    if not is_handle_thead_char:
        thead_char = f"{get_thead_char()}\n"
    if not is_th:
        reset_table()
        return ""
    reset_table()

    return f"\n{node.get('md')}\n{thead_char}"


def convert_th(node):
    is_th = True
    th_count = th_count + 1
    return f"{node.get('md')}|"


def convert_tr(node):
    tr_str = ''
    tr_count = tr_count + 1

    tr_str = f"\n|{node.get('md')}"

    is_handle_thead_char = is_handle_thead_char    # vsc bug

    if not is_handle_thead_char and tr_count == 2:
        thead_char = get_thead_char()
        is_handle_thead_char = True
        return f"\n{thead_char}{tr_str}"
    else:
        return f"{tr_str}"


def convert_td(node):
    is_th = True
    if tr_count == 0:
        th_count = th_count + 1
    md = node.get('md')
    r = re.compile('(<br>)|(<br/>)|(\n)|(\r\n)')
    md = re.sub(r, '', md)
    return f'{md}|'
# 表格相关结束


converters = {
    "a": convert_a,  # TODO: line 32 list has no get()
    "b": "**{}**",
    "p": "\n{}\n",
    "i": "_{}_",
    "em": "_{}_",
    "h1": "\n# {}\n",
    "h2": "\n## {}\n",
    "h3": "\n### {}\n",
    "h4": "\n#### {}\n",
    "h5": "\n##### {}\n",
    "h6": "\n###### {}\n",

    "ul": convert_ul,
    "ol": convert_ol,
    "li": LI_HEADER + " {}\n",

    "table": convert_table,
    "tr": convert_tr,
    "th": convert_th,
    "td": convert_td,

    "hr": "\n---\n",
    "br": "\n",

    "div": "\n{}\n",
    "img": convert_img,
    "pre": convert_pre,
    "code": convert_code,
    "strong": "**{}**",

    "script": "",

    "blockquote": convert_blockquote,

    "default": "{}"
}


def convert(node):
    if node.get('md', None) is not None:
        node['md'] = node['md'] and ''.join(node['md'])
    else:
        node['md'] = ""

    converter = converters.get(node.get('tag'), converters.get('default'))

    if isinstance(converter, str):
        node['md'] = converter.format(node['md'])

    if isfunction(converter):
        node['md'] = converter(node)

    return node['md']


class HTMLParserToMarkDown(HTMLParser):
    node_buffer = []
    results = []
    is_in_pre_node = False
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)

    def set_debug_level(self, level):
        self.logger.setLevel(level)

    def handle_starttag(self, tag, attrs):
        node = {
            'tag': tag,
            'attrs': dict(attrs),
            'is_in_pre_node': self.is_in_pre_node
        }

        if tag == "pre":
            self.is_in_pre_node = True

        if tag == "br":
            self.logger.debug("is br tag")
            return

        self.node_buffer.append(node)
        self.logger.debug("Start tag:" + tag)
        for attr in attrs:
            self.logger.debug("     attr:" + str(attr))

    def handle_endtag(self, tag):
        if tag == "br":
            self.node_buffer[len(self.node_buffer) - 1].get('md').append('\n')
            return
        last = self.node_buffer.pop()
        md = convert(last)

        if tag is "pre":
            is_in_pre_node = False

        if len(self.node_buffer) == 0:
            return self.results.append(md)

        tail = self.node_buffer[len(self.node_buffer) - 1]
        tail['md'] = tail.get('md', [])
        tail['md'].append(md)

        self.logger.debug("End tag  :" + tag)

    def handle_data(self, data):
        if re.search(r'^\s+$', data):
            return
        data = unescape(data)
        last = {}
        last = self.node_buffer[len(self.node_buffer) - 1]
        self.logger.debug(last)
        if last is not None:
            last['md'] = last.get('md', [])
            last['md'].append(data)
        else:
            self.results.append(data)
        self.logger.debug("Data     :" + data)

    def handle_comment(self, data):
        print("Comment  :" + data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        self.logger.debug("Named ent:" + c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.logger.debug("Num ent  :" + c)

    def handle_decl(self, data):
        self.logger.debug("Decl     :" + data)

    def reset_parser(self):
        self.results = []
        self.node_buffer = []
        self.is_in_pre_node = False

    def md(self):
        r_head_n = re.compile('^\n+|\n+$')
        r_3n_2n = re.compile('\n{3,}')

        clean_md = "".join(self.results)
        clean_md = re.sub(r_head_n, '', clean_md)
        clean_md = re.sub(r_3n_2n, '\n\n', clean_md)

        self.reset_parser()

        return clean_md


h2m = HTMLParserToMarkDown()

if __name__ == "__main__":
    h2m.set_debug_level(logging.DEBUG)

    # h2m.feed('<test_xhtml /><error></error><h1>&amp;Python</h1><ol><li>first</li><li>secend</li></ol><ul><li>first</li><li>secend</li></ul>')
    h2m.feed('''    <blockquote>
      <p>This is the first level of quoting.</p>
      <p>This is a paragraph in a nested blockquote.</p>
      <blockquote>
        <p>This is a paragraph in a nested blockquote.</p>
        <p>This is a paragraph in a nested blockquote.</p>
        <p>This is a paragraph in a nested blockquote.</p>
      </blockquote>
        <p>This is a paragraph in a nested blockquote.</p>
      <p>Back to the first level.</p>
    </blockquote>''')
    print(h2m.md())
