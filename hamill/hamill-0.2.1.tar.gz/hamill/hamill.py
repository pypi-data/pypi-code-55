# -----------------------------------------------------------
# MIT Licence (Expat License Wording)
# -----------------------------------------------------------
# Copyright © 2020, Damien Gouteux
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For more information about the Hamill lightweight markup language see:
# https://xitog.github.io/dgx/informatique/hamill.html

"""
Hamill: a simple lightweight markup language derived from markdown

**bold**
--strikethrough-- (insted of ~~, too hard to type)
__underline__ (instead of using __ for bold)
''italic'' (instead of * or _, too difficult to parse)

[link_ref] or [link_name->link_ref]

|Table|
|-----|
|data |

* liste

[link_ref]: http://youradress

Created 2020-04-03 as a buggy Markdown processor
Evolved 2020-04-07 as yet another language

"""

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

import os # for walk
import os.path # test if it is a directory or a file
import shutil

from hamill.tokenizer import RECOGNIZED_LANGUAGES, tokenize
from hamill.log import success, fail, info, warn, error

#-------------------------------------------------------------------------------
# Tool functions
#-------------------------------------------------------------------------------

def multi_start(string, starts):
    for key in starts:
        if string.startswith(key):
            return key

def multi_find(string, finds):
    for key in finds:
        if string.find(key) != -1:
            return key

def contains_only(string, things):
    for t in things:
        if string.startswith(t) and len(string.strip()) == len(t):
            return True
    return False

def escape(line):
    # Escaping
    if line.find('\\') == -1:
        return line
    new_line = ''
    index_char = 0
    while index_char < len(line):
        char = line[index_char]
        if index_char < len(line) - 1:
            next_char = line[index_char + 1]
        else:
            next_char = None
        if char == '\\' and next_char in ['*', "'", '^', '-', '_', '[', '@', '%', '+', '$', '!', '|', '{']:
            new_line += next_char
            index_char += 2    
        else:
            new_line += char
            index_char += 1
    return new_line

def safe(line):
    # Do not escape !html line
    if line.startswith('!html'):
        return line
    # Replace special glyph
    line = line.replace('<==', '⇐')
    line = line.replace('==>', '⇒')
    # Replace HTML special char
    new_line = ''
    index_char = 0
    while index_char < len(line):
        # current, next, prev
        char = line[index_char]
        if index_char < len(line) - 1:
            next_char = line[index_char + 1]
        else:
            next_char = None
        if index_char > 0:
            prev_char = line[index_char -1 ]
        else:
            prev_char = None
        # replace
        if char == '&':
            new_line += '&amp;'
        elif char == '<':
            new_line += '&lt;'
        elif char == '>' and next_char == '>' and index_char == 0: # must not replace >>
            new_line += '>>'
            index_char += 1
        elif char == '>' and prev_char != '-': # must not replace ->
            new_line += '&gt;'
        else:
            new_line += char
        index_char += 1
    return new_line

def find_title(line):
    c = 0
    nb = 0
    while c < len(line):
        if line[c] == '#':
            nb += 1
        else:
            break
        c += 1
    if nb > 0:
        title = line.replace('#' * nb, '', 1).strip()
        id_title = make_id(title)
        return nb, title, id_title
    return 0, None, None

def make_id(string):
    """Translate : A simple Title -> a_simple_title"""
    return string.replace(' ', '-').lower()

def write_code(line, code_lang):
    tokens = tokenize(line, code_lang)
    tokens_by_index = {}
    next_stop = None
    string = ''
    for tok in tokens:
        tokens_by_index[tok.start] = tok
    for index_char, char in enumerate(line):
        if index_char in tokens_by_index:
            tok = tokens_by_index[index_char]
            string += f'<span class="{tok.typ}">{char}'
            next_stop = tok.stop
        elif next_stop is not None and index_char == next_stop:
            string += f'{char}</span>'
        else:
            string += safe(char)
    return string

#-------------------------------------------------------------------------------
# Processors
#-------------------------------------------------------------------------------

def prev_next(line, index):
    if index > 0:
        _prev = line[index - 1]
    else:
        _prev = None
    if index > 1:
        _prev_prev = line[index - 2]
    else:
        _prev_prev = None
    if index < len(line) - 1:
        _next = line[index + 1]
    else:
        _next = None
    return _prev, _next, _prev_prev


def find_unescaped(line, motif, start=0):
    "Used by super_strip and code handling"
    index = start
    while index < len(line):
        found = line.find(motif, index)
        if found == -1:
            break
        elif found == 0 or line[found - 1] != '\\':
            return found
        else:
            index = found + len(motif)
    return -1


def process_string(line, links=None, inner_links=None, DEFAULT_CODE='text', DEFAULT_FIND_IMAGE=None):
    links = {} if links is None else links
    inner_links = [] if inner_links is None else inner_links
    new_line = ''
    in_bold = False
    in_italic = False
    in_strikethrough = False
    in_underline = False
    in_power = False
    in_code = False
    code = ''
    char_index = -1
    res = Result()
    while char_index < len(line) - 1:
        char_index += 1
        char = line[char_index]
        prev_char, next_char, prev_prev_char = prev_next(line, char_index)
        # Paragraph et span class (div class are handled elsewhere)
        if char == '{' and next_char == '{' and prev_char != '\\':
            continue
        if char == '{' and prev_char == '{' and prev_prev_char != '\\':
            ending = line.find('}}', char_index)
            inside = line[char_index + 1:ending]
            cls = ''
            ids = ''
            txt = ''
            state = 'start'
            for c in inside:
                # state
                if c == '.':
                    state = 'cls'
                elif c == ' ':
                    state = 'start'
                elif c == '#':
                    state = 'ids'
                elif state == 'start':
                    state = 'txt'
                # save
                if state == 'cls':
                    cls += c
                elif state == 'ids':
                    ids += c
                elif state == 'txt':
                    txt += c
            if len(txt) > 0:
                if len(ids) > 0 and len(cls) > 0:
                    new_line += f'<span id="{ids[1:]}" class="{cls[1:]}">{txt}</span>'
                elif len(ids) > 0:
                    new_line += f'<span id="{ids[1:]}">{txt}</span>'
                elif len(cls) > 0:
                    new_line += f'<span class="{cls[1:]}">{txt}</span>'
                else:
                    new_line += f'<span>{txt}</span>'
            else:
                if len(ids) > 0:
                    res['PARAGRAPH_ID'] = ids[1:]
                if len(cls) > 0:
                    res['PARAGRAPH_CLASS'] = cls[1:]
            char_index = ending + 1
            continue
        # Links and images
        if char == '[' and next_char == '#' and prev_char != '\\': # [# ... ] creating inner link
            ending = line.find(']', char_index)
            if ending != -1:
                link_name = line[char_index + 2:ending]
                id_link = make_id(link_name)
                new_line += f'<span id="{id_link}">{link_name}</span>'
                char_index = ending
                continue
        elif char == '[' and next_char == '!' and prev_char != '\\': # [! ... ] image
            ending = line.find(']', char_index)
            if ending != -1:
                link = line[char_index + 2:ending]
                if DEFAULT_FIND_IMAGE is None:
                    new_line += f'<img src="{link}"></img>'
                else:
                    new_line += f'<img src="{DEFAULT_FIND_IMAGE}{link}"></img>'
                char_index = ending
                continue
        elif char == '[' and char_index < len(line) - 1 and prev_char != '\\':
            ending = line.find(']', char_index)
            if ending != -1:
                link = line[char_index + 1:ending]
                # Set the link_name and the link
                if link.find('->') != -1:
                    link_name, link = link.split('->', 1)
                else:
                    link_name = link
                if link == '#':
                    link = link_name
                # Check the link
                if multi_start(link, ('https://', 'http://')):
                    pass
                elif make_id(link) in inner_links:
                    link = '#' + make_id(link)
                elif link in inner_links:
                    link = '#' + link
                elif link in links:
                    link = links[link]
                else:
                    #print(link)
                    #print(make_id(link))
                    #print(inner_links)
                    warn('Undefined link:', link, 'in', line)
                link_name = process_string(link_name, links, inner_links,
                                           DEFAULT_CODE, DEFAULT_FIND_IMAGE).first()
                new_line += f'<a href="{link}">{link_name}</a>'
                char_index = ending
                continue
        # Italic
        if char == "'" and next_char == "'" and prev_char != '\\':
            continue
        if char == "'" and prev_char == "'" and prev_prev_char != '\\':
            if not in_italic:
                new_line += '<i>'
                in_italic = True
            else:
                new_line += '</i>'
                in_italic = False
            continue
        # Strong
        if char == '*' and next_char == '*' and prev_char != '\\':
            continue
        if char == '*' and prev_char == '*' and prev_prev_char != '\\':
            if not in_bold:
                new_line += '<b>'
                in_bold = True
            else:
                new_line += '</b>'
                in_bold = False
            continue
        # Strikethrough
        if char == '-' and next_char == '-' and prev_char != '\\':
            continue
        if char == '-' and prev_char == '-' and prev_prev_char != '\\':
            if not in_strikethrough:
                new_line += '<s>'
                in_strikethrough = True
            else:
                new_line += '</s>'
                in_strikethrough = False
            continue
        # Underline
        if char == '_' and next_char == '_' and prev_char != '\\':
            continue
        if char == '_' and prev_char == '_' and prev_prev_char != '\\':
            if not in_underline:
                new_line += '<u>'
                in_underline = True
            else:
                new_line += '</u>'
                in_underline = False
            continue
        # Power
        if char == '^' and next_char == '^' and prev_char != '\\':
            continue
        if char == '^' and prev_char == '^' and prev_prev_char != '\\':
            if not in_power:
                new_line += '<sup>'
                in_power = True
            else:
                new_line += '</sup>'
                in_power = False
            continue
        # Code
        if char == '@' and next_char == '@' and prev_char != '\\':
            continue
        if char == '@' and prev_char == '@' and prev_prev_char != '\\':
            ending = find_unescaped(line, '@@', char_index)
            code = line[char_index + 1:ending]
            length = len(code) + 2
            s = multi_start(code, RECOGNIZED_LANGUAGES)
            if s is not None:
                code = code.replace(s, '', 1) # delete
            else:
                s = DEFAULT_CODE
            new_line += '<code>' + write_code(code, s) + '</code>'
            char_index += length
            continue
        new_line += char
    res.append(new_line)
    return res


def get(line):
    if line.startswith('!const'):
        command, value = line.replace('!const ', '').split('=')
    elif line.startswith('!var'):
        command, value = line.replace('!var ', '').split('=')
    else:
        raise Exception('No variable or constant defined here: ' + line)
    command = command.strip()
    value = value.strip()
    return command, value

LIST_STARTERS = {'* ': 'ul', '% ': 'ol', '+ ' : 'ol', '- ': 'ol reversed'}

def count_list_level(line):
    """Return the level of the list, the kind of starter and if it is
       a continuity of a previous level."""
    starter = line[0]
    if starter + ' ' not in LIST_STARTERS:
        raise Exception('Unknown list starter: ' + line[0] + ' in ' + line)
    level = 0
    continuity = False
    while line.startswith(starter + ' '):
        level += 1
        line = line[2:]
    if line.startswith('| '):
        level += 1
        continuity = True
    return level, starter, continuity


class Result:

    def __init__(self, default_lang='en', default_encoding='utf-8'):
        self.constants = {}
        self.variables = {}
        self.lines = []
        self.header_links = []
        self.header_css = []
        # 6 HTML constants
        self.constants['TITLE'] = None
        self.constants['ENCODING'] = default_encoding
        self.constants['LANG'] = default_lang
        self.constants['ICON'] = None
        self.constants['BODY_CLASS'] = None
        self.constants['BODY_ID'] = None
        # 2 var from markup {{.cls}} or {{#id}}
        self.variables['PARAGRAPH_ID'] = None
        self.variables['PARAGRAPH_CLASS'] = None

    def first(self):
        return self.lines[0]

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self.constants:
                return self.constants[key]
            elif key in self.variables:
                return self.variables[key]
            else:
                raise Exception('Key not known: ' + str(key))

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if key in self.constants:
                self.constants[key] = value
            elif key in self.variables:
                self.variables[key] = value
            else:
                raise Exception('Key not known: ' + str(key))

    def append(self, line):
        self.lines.append(line)

    def __iter__(self):
        for line in self.lines:
            yield line

    def __str__(self):
        return ''.join(self.lines)


def process_file(input_name, output_name=None, default_lang=None, includes=None):
    info('Processing file:', input_name)
    if not os.path.isfile(input_name):
        raise Exception('Process_file: Invalid source file: ' + str(input_name))
    source = open(input_name, mode='r', encoding='utf8')
    content = source.readlines()
    source.close()

    result = process_lines(content, default_lang, includes)

    if output_name is None:
        if input_name.endswith('.hml'):
            output_name = input_name.replace('.hml', '.html')
        else:
            output_name = input_name + '.html'
    output = open(output_name, mode='w', encoding='utf8')

    # Header
    if result["LANG"] is not None:
        output.write(f'<html lang="{result["LANG"]}">\n')
    else:
        output.write(f'<html>\n')
    output.write('<head>\n')
    output.write(f'  <meta charset={result["ENCODING"]}>\n')
    output.write('  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n')
    output.write('  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
    if result["TITLE"] is not None:
        output.write(f'  <title>{result["TITLE"]}</title>\n')
    if result["ICON"] is not None:
        output.write(f'  <link rel="icon" href="{result["ICON"]}" type="image/x-icon" />\n')
        output.write(f'  <link rel="shortcut icon" href="{result["ICON"]}" type="image/x-icon" />\n')

    # Should I put script in head?
    for line in result.header_links:
        output.write(line)
    # Inline CSS
    for line in result.header_css:
        output.write('<style type="text/css">\n')
        output.write(line + '\n')
        output.write('</style>\n')

    output.write('</head>\n')

    if result["BODY_CLASS"] is None and result["BODY_ID"] is None:
        output.write('<body>\n')
    elif result["BODY_ID"] is None:
        output.write(f'<body class="{result["BODY_CLASS"]}">\n')
    elif result["BODY_CLASS"] is None:
        output.write(f'<body id="{result["BODY_ID"]}">\n')
    else:
        output.write(f'<body id="{result["BODY_ID"]}" class="{result["BODY_CLASS"]}">\n')

    for line in result:
        output.write(line)

    output.write('</body>')
    output.close()


def output_list(result, list_array):
    heap = []
    closed = False
    for index in range(len(list_array)):
        elem = list_array[index]
        level = elem['level']
        starter = LIST_STARTERS[elem['starter'] + ' ']
        ender = starter[:2]
        line = elem['line']
        cont = elem['cont']
        # Iterate
        if index > 0:
            prev_level = list_array[index - 1]['level']
        else:
            prev_level = None
        if index < len(list_array) - 1:
            next_level = list_array[index + 1]['level']
            next_cont = list_array[index + 1]['cont']
        else:
            next_level = None
            next_cont = None
        # Output
        if prev_level is None or level > prev_level:
            start = 0 if prev_level is None else prev_level
            for current in range(start, level):
                result.append('    ' * current + f'<{starter}>\n')
                heap.append(ender)
                if current < level - 1:
                    result.append('    ' * current + f'  <li>\n')
        elif prev_level == level:
            current = level - 1
            if not closed and not cont:
                    result.append('    ' * current + '  </li>\n')
        elif level < prev_level:
            start = prev_level
            for current in range(start, level, -1):
                ender = heap[-1]
                if current != start:
                    result.append('    ' * (current - 1) + '  </li>\n')
                result.append('    ' * (current - 1) + f'</{ender}>\n')
                heap.pop()
            current -= 2
            result.append('    ' * current + '  </li>\n')
        # Line
        s = '    ' * current + '  '
        if cont:
            s += '<br>'
        else:
            s += '<li>'
        s += line
        if (next_level is None or next_level <= level) and not (next_level == level and next_cont):
            s += '</li>\n'
            closed = True
        #elif next_cont is not None and not next_cont)
        else:
            s += '\n'
            closed = False
        result.append(s)
    if len(heap) > 0:
        while len(heap) > 0:
            ender = heap[-1]
            if not closed:
                result.append('    ' * (len(heap) - 1) + '  </li>\n')
            result.append('    ' * (len(heap) - 1) + f'</{ender}>\n')
            closed = False
            heap.pop()


COMMENT_STARTER = '§§'

def super_strip(line):
    """Remove any blanks at the start or the end of the string AND the comments §§"""
    line = line.strip()
    if len(line) == 0:
        return line
    index = find_unescaped(line, COMMENT_STARTER)
    if index != -1:
        return line[:index].strip()
    else:
        return line


def process_lines(lines, default_lang=None, includes=None):
    VAR_EXPORT_COMMENT=False
    VAR_DEFINITION_AS_PARAGRAPH=False
    VAR_DEFAULT_CODE='text'
    VAR_DEFAULT_PAR_CLASS=None
    VAR_DEFAULT_TAB_CLASS=None
    VAR_NEXT_PAR_CLASS=None
    VAR_NEXT_PAR_ID=None
    VAR_NEXT_TAB_CLASS=None
    VAR_DEFAULT_FIND_IMAGE=None
    # The 6 HTML constants are defined in Result class
    result = Result(default_lang)
    in_table = False
    links = {}
    inner_links = []
    in_definition_list = False
    in_code_free_block = False
    in_code_block = False
    in_pre_block = False
    code_lang = None
    
    # 1st Pass : prefetch links, replace special HTML char, skip comments
    # Empty line must be kept to separate lists!
    after = []
    for line in lines:
        # Constant must be read first, are defined once, anywhere in the doc
        if line.startswith('!const '):
            command, value = get(line)
            if command == 'TITLE':
                result["TITLE"] = value
            elif command == 'ENCODING':
                result["ENCODING"] = value
            elif command == 'ICON':
                result["ICON"] = value
            elif command == 'LANG':
                result["LANG"] = value
            elif command == 'BODY_CLASS':
                results["BODY_CLASS"] = value
            elif command == 'BODY_ID':
                result["BODY_ID"] = value
            else:
                raise Exception('Unknown constant: ' + command + 'with value= ' + value)
        elif line.startswith('!require ') and super_strip(line).endswith('.css'):
            required = super_strip(line.replace('!require ', '', 1))
            result.header_links.append(f'  <link href="{required}" rel="stylesheet">\n')
        # Inline CSS
        elif line.startswith('!css '):
            result.header_css.append(super_strip(line.replace('!css ', '', 1)))
        else:
            # Block of code
            if len(line) > 2 and line[0:3] == '@@@':
                if not in_code_free_block:
                    in_code_free_block = True
                else:
                    in_code_free_block = False
            if line.startswith('@@'):
                in_code_block = True
            else:
                in_code_block = False
            # Strip
            if not in_code_free_block and not in_code_block:
                line = super_strip(line)
            # Special chars
            line = safe(line)
            # Link library
            if len(line) > 0 and line[0] == '[' and (line.find(']: https://') != -1 or line.find(']: http://') != -1):
                name = line[1:line.find(']: ')]
                link = line[line.find(']: ') + len(']: '):]
                links[name] = link
                continue
            # Inner links
            if line.find('[#') != -1:
                char_index = 0
                while char_index < len(line):
                    char = line[char_index]
                    prev_char, next_char, prev_prev_char = prev_next(line, char_index)
                    if char == '[' and next_char == '#' and prev_char != '\\': # [# ... ] inner link
                        ending = line.find(']', char_index)
                        if ending != -1:
                            link_name = line[char_index + 2:ending]
                            id_link = make_id(link_name)
                            if id_link in inner_links:
                                log.warn("Multiple definitions of anchor: " + id_link)
                            inner_links.append(id_link)
                            char_index = ending
                            continue
                    char_index += 1
            # Inner links from Title
            nb, title, id_title = find_title(line)
            if nb > 0:
                inner_links.append(id_title)
            after.append(line)
    content = after
    
    # Start of output
    list_array = []
    
    # 2nd Pass
    index = -1
    while index < len(content) - 1:
        index += 1
        line = content[index]
        # Next line
        if index < len(content) - 2:
            next_line = content[index + 1]
        else:
            next_line = None
        # Variables
        if line.startswith('!var '):
            command, value = get(line)
            if command == 'EXPORT_COMMENT':
                if value == 'true':
                    VAR_EXPORT_COMMENT = True
                elif value == 'false':
                    VAR_EXPORT_COMMENT = False
            elif command == 'PARAGRAPH_DEFINITION':
                if value == 'true':
                    VAR_DEFINITION_AS_PARAGRAPH = True
                else:
                    VAR_DEFINITION_AS_PARAGRAPH = False
            elif command == 'DEFAULT_CODE':
                if value in RECOGNIZED_LANGUAGES:
                    VAR_DEFAULT_CODE = value
                else:
                    warn('Not recognized language in var VAR_DEFAULT_CODE:', value)
            elif command == 'NEXT_PAR_ID':
                VAR_NEXT_PAR_ID = value if value != 'reset' else None
            elif command == 'NEXT_PAR_CLASS':
                VAR_NEXT_PAR_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_PAR_CLASS':
                VAR_DEFAULT_PAR_CLASS = value if value != 'reset' else None
            elif command == 'NEXT_TAB_CLASS':
                VAR_NEXT_TAB_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_TAB_CLASS':
                VAR_DEFAULT_TAB_CLASS = value if value != 'reset' else None
            elif command == 'DEFAULT_FIND_IMAGE':
                VAR_DEFAULT_FIND_IMAGE = value if value != 'reset' else None
            else:
                raise Exception('Var unknown: ' + command + ' with value = ' + value)
            continue
        # Comment
        if line.startswith(COMMENT_STARTER):
            if VAR_EXPORT_COMMENT:
                line = line.replace(COMMENT_STARTER, '<!--', 1) + ' -->'
                result.append(line + '\n')
            continue
        # Require CSS or JS file
        if line.startswith('!require '):
            required = line.replace('!require ', '', 1)
            if required.endswith('.js'):
                result.append(f'  <script src="{required}"></script>\n')
            else:
                raise Exception("I don't known how to handle this file: " + required)
            continue
        # Include HTML file
        if line.startswith('!include '):
            included = line.replace('!include ', '', 1).strip()
            if includes is not None:
                filepath = None
                for file in includes:
                    if os.path.basename(file) == included:
                        filepath = file
                if filepath is not None:
                    file = open(filepath, mode='r', encoding='utf8')
                    file_content = file.read()
                    file.close()
                    result.append(file_content + '\n')
                else:
                    warn('Included file', included, 'not found in includes.')
            else:
                warn('No included files for generation.')
            continue
        # Inline HTML
        if line.startswith('!html '):
            result.append(line.replace('!html ', '', 1) + '\n')
            continue
        # HR
        if line.startswith('---'):
            if line.count('-') == len(line):
                result.append('<hr>\n')
                continue
        # BR
        if line.find(' !! ') != -1:
            line = line.replace(' !! ', '<br>')
        # Block of pre
        if line.startswith('>>'):
            if not in_pre_block:
                result.append('<pre>\n')
                in_pre_block = True
            line = escape(line[2:])
            result.append(line + '\n')
            continue
        elif in_pre_block:
            result.append('</pre>\n')
            in_pre_block = False
        # Block of code 1
        if len(line) > 2 and line[0:3] == '@@@':
            if not in_code_free_block:
                result.append('<pre class="code">\n')
                in_code_free_block = True
                code_lang = line.replace('@@@', '', 1).strip()
                if len(code_lang) == 0:
                    code_lang = VAR_DEFAULT_CODE
            else:
                result.append('</pre>\n')
                in_code_free_block = False
            continue 
        # Block of code 2
        if line.startswith('@@') and (len(super_strip(line)) == 2 or line[2] != '@'):
            if not in_code_block:
                result.append('<pre class="code">\n')
                in_code_block = True
                code_lang = super_strip(line.replace('@@', '', 1))
                if len(code_lang) == 0:
                    code_lang = VAR_DEFAULT_CODE
                continue
        elif in_code_block:
            result.append('</pre>\n')
            in_code_block = False
        if in_code_free_block or in_code_block:
            if in_code_block:
                line = line[2:] # remove starting @@
            result.append(write_code(line, code_lang))
            continue
        # Div {{#ids .cls}}
        if line.startswith('{{') and line.endswith('}}'):
            inside = line[2:-2]
            if inside == 'end':
                result.append('</div>\n')
            else:
                cls = ''
                ids = ''
                state = 'start'
                for c in inside:
                    # state
                    if c == '.':
                        state = 'cls'
                    elif c == ' ':
                        state = 'start'
                    elif c == '#':
                        state = 'ids'
                    # save
                    if state == 'cls':
                        cls += c
                    elif state == 'ids':
                        ids += c
                if len(cls) > 0 and len(ids) > 0:
                    result.append(f'<div id="{ids[1:]}" class="{cls[1:]}">\n')
                elif len(cls) > 0:
                    result.append(f'<div class="{cls[1:]}">\n')
                elif len(ids) > 0:
                    result.append(f'<div id="{ids[1:]}">\n')
                else:
                    result.append(f'<div id="{cls}">\n')
            continue
        # Bold & Italic & Strikethrough & Underline & Power
        if multi_find(line, ('**', '--', '__', '^^', "''", "[", '@@', '{{')) and \
           not line.startswith('|-'):
            res = process_string(line, links, inner_links, VAR_DEFAULT_CODE, VAR_DEFAULT_FIND_IMAGE)
            line = res.first()
            VAR_NEXT_PAR_CLASS = res['PARAGRAPH_CLASS']
            VAR_NEXT_PAR_ID = res['PARAGRAPH_ID']
        # Title
        nb, title, id_title = find_title(line)
        if nb > 0:
            line = f'<h{nb} id="{id_title}">{title}</h{nb}>\n'
            result.append(line)
            continue
        # Liste
        found = multi_start(line, LIST_STARTERS)
        if found:
            level, starter, cont = count_list_level(line)
            list_array.append({'level': level, 'starter': starter, 'line': escape(line[level * 2:]), 'cont': cont})
            continue
        elif len(list_array) > 0 and len(line) > 0 and line[0] == '|':
            level = list_array[-1]['level']
            starter = list_array[-1]['starter']
            list_array.append({'level': level, 'starter': starter, 'line': escape(line[2:]), 'cont': True})
            continue
        elif len(list_array) > 0:
            output_list(result, list_array)
            list_array = []
        # Table
        if len(line) > 0 and line[0] == '|':
            if not in_table:
                if VAR_DEFAULT_TAB_CLASS is not None:
                    result.append(f'<table class="{VAR_DEFAULT_TAB_CLASS}">\n')
                elif VAR_NEXT_TAB_CLASS is not None:
                    result.append(f'<table class="{VAR_NEXT_TAB_CLASS}">\n')
                    VAR_NEXT_TAB_CLASS = None
                else:
                    result.append('<table>\n')
                in_table = True
            if next_line is not None and next_line.startswith('|-'):
                element = 'th'
            else:
                element = 'td'
            columns = line.split('|')
            skip = True
            for col in columns:
                if len(col.replace('-', '').strip()) != 0:
                    skip = False
            if not skip:
                result.append('<tr>')
                for col in columns:
                    if col != '': # center or right-align
                        if col[0] == '>':
                            align = ' align="right"'
                            col = col[1:]
                        elif col[0] == '=':
                            align = ' align="center"'
                            col = col[1:]
                        else:
                            align = ''
                        res = process_string(escape(col), links, inner_links, VAR_DEFAULT_CODE, VAR_DEFAULT_FIND_IMAGE)
                        val = res.first()
                        result.append(f'<{element}{align}>{val}</{element}>')
                result.append('</tr>\n')
            continue
        elif in_table:
            result.append('</table>\n')
            in_table = False
        # Definition list
        if line.startswith('$ '):
            if not in_definition_list:
                in_definition_list = True
                result.append('<dl>\n')
            else:
                result.append('</dd>\n')
            result.append(f'<dt>{line.replace("$ ", "", 1)}</dt>\n<dd>\n')
            continue
        elif len(line) != 0 and in_definition_list:
            if not VAR_DEFINITION_AS_PARAGRAPH:
                result.append(escape(line) +'\n')
            else:
                result.append('<p>' + escape(line) +'</p>\n')
            continue
        # empty line
        elif len(line) == 0 and in_definition_list:
            in_definition_list = False
            result.append('</dl>\n')
            continue
        # Replace escaped char
        line = escape(line)
        # Paragraph
        if len(line) > 0:
            cls = f'class="{VAR_DEFAULT_PAR_CLASS}"' if VAR_DEFAULT_PAR_CLASS is not None else ''
            cls = f'class="{VAR_NEXT_PAR_CLASS}"' if VAR_NEXT_PAR_CLASS is not None else cls
            ids = f'id="{VAR_NEXT_PAR_ID}"' if VAR_NEXT_PAR_ID is not None else ''
            space1 = ' ' if len(cls) > 0 or len(ids) > 0 else ''
            space2 = ' ' if len(cls) > 0 and len(ids) > 0 else ''
            VAR_NEXT_PAR_CLASS = None
            result.append(f'<p{space1}{ids}{space2}{cls}>' + super_strip(line) + '</p>\n')
    # Are a definition list still open?
    if in_definition_list:
        result.append('</dl>\n')
    # Are some lists still open?
    if len(list_array) > 0:
        output_list(result, list_array)
    # Are a table still open?
    if in_table:
        result.append('</table>\n')
        in_table = False
    # Are we stil in in_pre_block?
    if in_pre_block:
        result.append('</pre>')
    # Are we still in in_code_block?
    if in_code_block:
        result.append('</pre>')
    return result


#-------------------------------------------------------------------------------
# Main functions
#-------------------------------------------------------------------------------


def process_dir(source, dest, default_lang=None, includes=None):
    """Process a directory:
            - If it is a .hml file, it is translated in HTML
            - Else the file is copied into the new directory
       The destination directory is systematically DELETED at each run.
    """
    info('Processing directory:', source)
    if not os.path.isdir(source):
        raise Exception('Process_dir: Invalid source directory: ' + str(source))
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    info('Making dir:', dest)
    os.mkdir(dest)
    for name_ext in os.listdir(source):
        path = os.path.join(source, name_ext)
        if os.path.isfile(path):
            name, ext = os.path.splitext(name_ext)
            if ext == '.hml':
                process_file(path, os.path.join(dest, name + '.html'), default_lang, includes)
            else:
                info('Copying file:', path)
                shutil.copy2(path, os.path.join(dest, name_ext))
        elif os.path.isdir(path):
            process_dir(path, os.path.join(dest, name_ext), default_lang, includes)


def process(source, dest, default_lang=None, includes=None):
    """Process a file or directory"""
    if os.path.isfile(source):
        process_file(source, dest, default_lang, includes)
    elif os.path.isdir(source):
        process_dir(source, dest, default_lang, includes)
    else:
        warn('Process:', source, 'not found.')
