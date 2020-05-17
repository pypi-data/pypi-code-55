import argparse
from io import StringIO
import math
import sys

from bs4 import BeautifulSoup, PageElement, Tag, NavigableString

from .compat import stream_configure


def digitlize(n):
    if n == 0:
        return 1
    else:
        return int(math.log10(abs(n))) + 1


class HtmlNode(object):
    TEXT_REPR_LEN = 20
    FMT_MINIMUM   = '{indent}-{name}{cls}{id}'
    
    def __init__(self, bsObj, level):
        self.name    = bsObj.name
        self.class_  = bsObj.attrs['class'] if 'class' in bsObj.attrs else ''
        self.id_     = bsObj.attrs['id']    if 'id'    in bsObj.attrs else ''
        self.srcline = bsObj.sourceline
        self.srcpos  = bsObj.sourcepos
        self.level   = level
        self.text    = self.__get_own_text(bsObj)
    
    def __get_own_text(self, bsObj):
        for c in bsObj.children:
            if isinstance(c, NavigableString):
                return c.string
        return ''
    
    def pprint(self, source, srcdigit, treedigit=0, *, file=sys.stdout):
        name    = self.name
        indent  = '| ' * max(self.level, 0)
        clsrepr = '.' + ' '.join(self.class_) if self.class_ else ''
        idrepr  = '#' + self.id_              if self.id_    else ''
        
        treerepr = self.FMT_MINIMUM.format(indent=indent, name=name,
                                           cls=clsrepr, id=idrepr)
        if source:
            srcrepr  = str(self.srcline).rjust(srcdigit[0]) + ',' + str(self.srcpos).rjust(srcdigit[1])
            treerepr = srcrepr + '  ' + treerepr
        
        if treedigit:
            textrepr = self.text.strip().replace('\n', '')[:self.TEXT_REPR_LEN]
            treerepr = treerepr.ljust(treedigit) + '  ' + textrepr
        
        print(treerepr, file=file)


class HtmlTree(object):
    def __init__(self):
        self.nodelist = []
    
    def parse(self, bsObj, filter, selector):
        tree(bsObj,
             selector=selector,
             filter=lambda x: x in filter,
             nodelist=self.nodelist)
        return self
    
    def pprint(self, source=False, text=False, *, file=sys.stdout):
        treedigit = 0
        srcdigit  = (3, 3)
        
        if text:
            with StringIO() as buf:
                self.pprint(source=source, text=False, file=buf)
                treedigit = max([len(s) for s in buf.getvalue().split('\n')])
        
        if source:
            srcdigit = digitlize(max([node.srcline for node in self.nodelist])), digitlize(max([node.srcpos for node in self.nodelist]))
        
        for node in self.nodelist:
            node.pprint(source, srcdigit, treedigit=treedigit, file=file)


def select_one_strict(bsObj, selector):
    assert isinstance(bsObj, PageElement), type(bsObj)
    assert isinstance(selector, str), type(selector)
    
    bsObjSub = bsObj.select(selector)
    assert len(bsObjSub) == 1, 'css selector must correspond to 1 unique element. ()' % len(bsObjSub)
    return bsObjSub[0]


def tree(bsObj, level=-1, selector='',
         filter=lambda x: False,
         nodelist=None):
    assert isinstance(bsObj, PageElement), type(bsObj)
    
    if selector:
        bsObjCur = select_one_strict(bsObj, selector)
        
        while BeautifulSoup.ROOT_TAG_NAME != bsObjCur.name:
            for sibling in list(bsObjCur.next_siblings) + list(bsObjCur.previous_siblings):
                if isinstance(sibling, Tag):
                    sibling.decompose()
            bsObjCur = bsObjCur.parent
    
    if not isinstance(bsObj, Tag) or filter(bsObj.name):
        return
    
    if BeautifulSoup.ROOT_TAG_NAME != bsObj.name:
        nodelist.append(HtmlNode(bsObj, level))
    
    for c in bsObj.children:
        tree(c, level=level+1, filter=filter, nodelist=nodelist)


def __parser():
    PARSER_DESC0 = 'html tree view pprint'
    PARSER_HELP0 = 'stdin or .html filename'
    PARSER_HELP1 = 'filtered tag names (default: %(default)s)'
    PARSER_HELP2 = 'HTML parser name (default: %(default)s)'
    PARSER_HELP3 = 'add "sourceline, pos" of corresponding start-tags'
    PARSER_HELP4 = 'css selector string, must be quoted'
    PARSER_HELP5 = 'add HTML below tree view, in the scope specified with selector'
    PARSER_HELP6 = 'text encoding of stdin/stdout'
    PARSER_HELP7 = 'add "text value" of corresponding tags'
    
    parser = argparse.ArgumentParser(description=PARSER_DESC0)
    parser.add_argument('html', nargs='?', type=argparse.FileType('r', encoding='utf-8'),
                        default=sys.stdin,
                        help=PARSER_HELP0)
    parser.add_argument('--filter', nargs='*', default=['p', 'br', 'span'],
                        help=PARSER_HELP1)
    parser.add_argument('--parser', default='html.parser',
                        help=PARSER_HELP2)
    parser.add_argument('--source', default=False, action='store_true',
                        help=PARSER_HELP3)
    parser.add_argument('--select',
                        help=PARSER_HELP4)
    parser.add_argument('--raw', default=False, action='store_true',
                        help=PARSER_HELP5)
    parser.add_argument('--encoding', default='utf-8',
                        help=PARSER_HELP6)
    parser.add_argument('--text', default=False, action='store_true',
                        help=PARSER_HELP7)
    
    return parser


def main():
    # set ahead of parser creation
    parser1 = argparse.ArgumentParser(add_help=False)
    parser1.add_argument('--encoding', default='utf-8')
    args, _ = parser1.parse_known_args()
    
    sys.stdin  = stream_configure(args.encoding, sys.stdin)
    sys.stdout = stream_configure(args.encoding, sys.stdout)
    sys.stderr = stream_configure(args.encoding, sys.stderr)
    
    parser = __parser()
    args = parser.parse_args()
    
    # prohibit inputmode
    if sys.stdin.isatty() and '<stdin>' == args.html.name:
        parser.print_help(); return
    
    # souplize
    html = args.html.read()
    bsObj = BeautifulSoup(html, features=args.parser)
    
    # destructive!
    HtmlTree().parse(bsObj, filter=args.filter, selector=args.select).pprint(source=args.source, text=args.text, file=sys.stdout)
    
    if args.raw and args.select:
        print('')  # blank line
        print(select_one_strict(bsObj, args.select))
