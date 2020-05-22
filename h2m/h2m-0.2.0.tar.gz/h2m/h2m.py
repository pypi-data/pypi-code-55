"""Main module."""

import re
import logging
from html import unescape
from html.parser import HTMLParser
from html.entities import name2codepoint
from inspect import isfunction


class TableParser:
    # 表格相关开始

    def __init__(self):
        self.reset_table()

    def reset_table(self):
        self.is_handle_thead_char = False
        self.is_tr = False
        self.is_th = False
        self.tr_count = 0
        self.th_count = 0
        self.table_level = 1

    def get_thead_char(self):
        thead_char = '|'
        i = self.th_count
        while i > 0:
            thead_char = f"{thead_char}--------|"
            i = i - 1
        return thead_char

    def convert_table(self, node):
        thead_char = ""
        if not self.is_handle_thead_char:
            thead_char = f"{self.get_thead_char()}\n"
        if not self.is_th:
            self.reset_table()
            return ""
        self.reset_table()

        return f"\n{node.get('md')}\n{thead_char}"

    def convert_th(self, node):
        self.is_th = True
        self.th_count = self.th_count + 1
        return f"{node.get('md')}|"

    def convert_tr(self, node):
        tr_str = ''
        self.tr_count = self.tr_count + 1

        tr_str = f"\n|{node.get('md')}"

        if not self.is_handle_thead_char and self.tr_count == 2:
            thead_char = self.get_thead_char()
            self.is_handle_thead_char = True
            return f"\n{thead_char}{tr_str}"
        else:
            return f"{tr_str}"

    def convert_td(self, node):
        self.is_th = True
        if self.tr_count == 0:
            self.th_count = self.th_count + 1
        md = node.get('md')
        if node['table_level'] != 13:
            r = re.compile('(<br>)|(<br/>)|(</br>)|(\n)|(\r\n)')
            md = re.sub(r, '', md)
        return f'{md}|'
    # 表格相关结束


class ConvertClass:
    def __init__(self):
        self.li_header = 'H2M_LI_HEADER'
        self.table_parser = TableParser()
        self.converters = {
            "a": self.convert_a,
            "b": self.convert_b_strong,
            "p": "\n{}\n",
            "i": self.convert_i_em,
            "em": self.convert_i_em,
            "h1": "\n# {}\n",
            "h2": "\n## {}\n",
            "h3": "\n### {}\n",
            "h4": "\n#### {}\n",
            "h5": "\n##### {}\n",
            "h6": "\n###### {}\n",

            "ul": self.convert_ul,
            "ol": self.convert_ol,
            "li": self.li_header + " {}\n",

            "table": self.table_parser.convert_table,
            "tr": self.table_parser.convert_tr,
            "th": self.table_parser.convert_th,
            "td": self.table_parser.convert_td,

            "hr": "\n---\n",
            "br": "\n",

            "div": "\n{}\n",
            "img": self.convert_img,
            "pre": self.convert_pre,
            "code": self.convert_code,
            "strong": self.convert_b_strong,

            "script": "",
            "style": "",

            "blockquote": self.convert_blockquote,

            "default": "{}"
        }

    def convert_a(self, node):
        text = node.get('md', node.get('attrs', {'href': ''}).get('href'))
        text = text.replace('\n', '')
        href = node.get('attrs', {'href': text}).get('href')
        return f"[{text}]({href})"

    def convert_b_strong(self, node):
        if node['raw_text_flag']:
            return f"{node.get('md')}"
        else:
            return f"**{node.get('md')}**"

    def convert_i_em(self, node):
        if node['raw_text_flag']:
            return f"{node.get('md')}"
        else:
            return f"_{node.get('md')}_"

    def convert_img(self, node):
        attrs = node.get('attrs', {'title': '', 'alt': '', 'src': ''})
        title = attrs.get('title', attrs.get('alt', ''))
        src = attrs.get('src', '')

        if title == '' and src == '':
            return ''

        return f"![{title}]({src})"

    def convert_ul(self, node):
        return f"\n{str(node['md']).replace(self.li_header, '-')}"

    def convert_ol(self, node):
        i = 1
        count = node['md'].count(self.li_header)
        while i <= count:
            node['md'] = str(node['md']).replace(self.li_header, f"{i}.", 1)
            i = i + 1

        return f"\n{node['md']}"

    def convert_pre(self, node):
        md = node.get('md', None)
        if md:
            return ''.join(map(lambda line: f'    {line}\n', md.split('\n')))
        return f"\n{md}\n"

    def convert_code(self, node):
        md = node['md']
        if node.get('is_in_pre_node', False):
            return md
        return f'`{md}`'

    def convert_blockquote(self, node):
        r_str = '(^(\n+))|((\n+)$)'
        r = re.compile(r_str)
        md = node.get('md')
        # md = re.sub(r, '', md)
        if node['table_level'] > 10:
            return md
        md = ''.join(
            map(lambda line: f"> {re.sub(r, '', line)}\n", md.split('\n')))
        return f'\n{md}\n'

    def convert(self, node):
        if node.get('md', None) is not None:
            node['md'] = node['md'] and ''.join(node['md'])
            if node['md'] == 'None' :
                print('hi None')
        else:
            node['md'] = ""

        converter = self.converters.get(
            node.get('tag'), self.converters.get('default'))

        if isinstance(converter, str):
            node['md'] = converter.format(node['md'])
        else:
            node['md'] = converter(node)

        return node['md']

    ###################


class HTMLParserToMarkDown(HTMLParser):
    converter = ConvertClass()
    node_buffer = []
    results = []
    is_in_pre_node = False
    table_level = 1
    raw_text_flag = False
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)

    def set_debug_level(self, level):
        self.logger.setLevel(level)

    def feed(self, data):
        r_table = re.compile('<table[\S\s\w]*<table[\S\s\w]*</table>')
        if re.search(r_table, data):
            self.table_level = 12

        super().feed(data)
        # 只接收完整的html
        self.close()


    def handle_starttag(self, tag, attrs):
        node = {
            'tag': tag,
            'attrs': dict(attrs),
            'is_in_pre_node': self.is_in_pre_node,
            'table_level': self.table_level,
            'raw_text_flag': self.raw_text_flag
        }

        if tag == 'table':
            self.table_level = self.table_level + 1

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
        node_buffer_length = len(self.node_buffer)
        if tag == 'table':
            self.table_level = self.table_level - 1

        if tag == "br":
            self.node_buffer[node_buffer_length - 1].get('md', []).append('\n')
            return
        if node_buffer_length != 0:
            last = self.node_buffer.pop()
            node_buffer_length = len(self.node_buffer)
            md = self.converter.convert(last)
        else:
            md = ""

        if tag is "pre":
            is_in_pre_node = False

        if node_buffer_length == 0:
            return self.results.append(md)

        tail = self.node_buffer[node_buffer_length - 1]
        tail['md'] = tail.get('md', [])
        tail['md'].append(md)

        self.logger.debug("End tag  :" + tag)

    def handle_data(self, data):
        if re.search(r'^\s+$', data):
            return
        # data = self.unescape(data)
        data = unescape(data)
        last = {}
        node_buffer_length = len(self.node_buffer)
        if node_buffer_length >= 1:
            last = self.node_buffer[node_buffer_length - 1]
            self.logger.debug(last)

            last['md'] = last.get('md', [])
            last['md'].append(data)
        else:
            self.results.append(data)
        self.logger.debug("Data     :" + data)

    def handle_comment(self, data):
        self.logger.debug("Comment  :" + data)

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
        if len(self.results) == 0 and len(self.node_buffer) != 0:
            while len(self.node_buffer) != 0:
                last = self.node_buffer.pop()
                md = self.converter.convert(last)
                self.results.append(md)

        r_head_n = re.compile('^\n+|\n+$')
        r_3n_2n = re.compile('\n{3,}')

        clean_md = "".join(self.results)
        clean_md = re.sub(r_head_n, '', clean_md)
        clean_md = re.sub(r_3n_2n, '\n\n', clean_md)

        self.reset_parser()

        return clean_md


h2m = HTMLParserToMarkDown()

if __name__ == "__main__":
    # h2m.set_debug_level(logging.DEBUG)

    # # h2m.feed('<test_xhtml /><error></error><h1>&amp;Python</h1><ol><li>first</li><li>secend</li></ol><ul><li>first</li><li>secend</li></ul>')
    # h2m.feed('''    <blockquote>
    #   <p>This is the first level of quoting.</p>
    #   <p>This is a paragraph in a nested blockquote.</p>
    #   <blockquote>
    #     <p>This is a paragraph in a nested blockquote.</p>
    #     <p>This is a paragraph in a nested blockquote.</p>
    #     <p>This is a paragraph in a nested blockquote.</p>
    #   </blockquote>
    #     <p>This is a paragraph in a nested blockquote.</p>
    #   <p>Back to the first level.</p>
    # </blockquote>''')

    import pathlib
    h2m.raw_text_flag = True
    test_html = pathlib.Path("tests\\html\\raw_text.html")
    with test_html.open('rt', encoding='utf-8') as th:
        html = th.readlines()
        h2m.feed("".join(html))
    print(h2m.md())
