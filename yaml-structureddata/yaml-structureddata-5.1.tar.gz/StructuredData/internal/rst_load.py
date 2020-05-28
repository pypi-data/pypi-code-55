"""class to load rst files.
"""

import re

__version__="5.1" #VERSION#

# pylint: disable=invalid-name

def read_file(filename):
    """read a file and return the lines."""
    f= open(filename,"r")
    lines= f.readlines()
    f.close()
    return lines

rx_star_remove= re.compile(r'\*([A-Za-z]\w*)\*')

rx_double_colon= re.compile(r'::\s*$')

rx_ref= re.compile(r':ref:`([^<]+?)\s+<[^>]+>`')

def transform(st):
    r"""transform some RST character sequences to a more readable form.

    Here are some examples:
    >>> transform(r"print\_")
    'print_'
    >>> transform(r"a star \*")
    'a star *'
    >>> transform("a double colon::")
    'a double colon:'
    >>> transform("see also :ref:`document 1 <ab>` "+\
    ...           "or :ref:`document 2 <xy>` for more information")
    'see also ->document 1 or ->document 2 for more information'
    >>> print(transform(".. a comment"))
    None
    """
    if st.startswith(".."):
        # a comment
        return None
    st= st.replace(r"\_","_")
    st= st.replace(r'\*', "*")
    st= st.replace("\\\\","\\")
    st= rx_double_colon.sub(":", st)
    st= rx_ref.sub(r"->\1",st) # handle sphinx references
    return rx_star_remove.sub(r"\1", st)

rx_heading= re.compile(r'^(?P<ch>[=:._#\+-])(?P=ch){2,}\s*$')

def is_heading(st):
    """match a RST heading.

    Here are some examples:
    >>> is_heading("=")
    False
    >>> is_heading("==")
    False
    >>> is_heading("===")
    True
    >>> is_heading("=== =")
    False
    >>> is_heading("=== ")
    True
    >>> is_heading("... ")
    True
    >>> is_heading("--- ")
    True
    """
    m= rx_heading.match(st)
    return m is not None

def scan_headings(lines):
    """find and mark headings.

    A heading is transformed into a tuple consisting of
    a heading character and the heading string itself.
    All other lines remain unchanged.

    Here is an example:
    >>> text='''
    ... This is a heading
    ... =================
    ...
    ... a text follows
    ... here
    ...
    ... here is another heading
    ... +++++++++++++++++++++++
    ...
    ... with some text'''
    >>> for x in scan_headings(text.splitlines()):
    ...   print(repr(x))
    ...
    ''
    ('=', 'This is a heading')
    ''
    'a text follows'
    'here'
    ''
    ('+', 'here is another heading')
    ''
    'with some text'
    """
    last= None
    for l in lines:
        if last is None:
            last= l
            continue
        if not is_heading(l):
            yield last
            last= l
            continue
        yield (l[0],last)
        last= None
        continue
    if last is not None:
        yield last

def count_headings(elements):
    """put a level to each heading.

    returns a dict mapping heading levels to heading chars.
    Here is an example:

    >>> import pprint
    >>> lst=[
    ...      ('=', 'This is a heading'),
    ...      '',
    ...      'a text follows',
    ...      'here',
    ...      '',
    ...      ('+', 'here is another heading'),
    ...      '',
    ...      'with some text'
    ...     ]
    >>> pprint.pprint(count_headings(lst))
    {'+': 2, '=': 1}
    """
    heading_chars= {}
    last_level= 1
    for l in elements:
        if isinstance(l, tuple):
            ch= l[0]
            level= heading_chars.get(ch)
            if level is None:
                heading_chars[ch]= last_level
                level= last_level
                last_level+=1
    return heading_chars

class Node():
    """implements a representation of RST text as nodes.

    A node is a chapter in a RST text. It has a name which is the chapter
    heading, optional lines of text and an optional list of sub-chapters.

    Here are some examples:
    >>> n= Node("heading",1)
    >>> n.add_line("some text")
    >>> n2= Node("sub-heading",2,n)
    >>> print(n)
    Heading: 'heading'
    level: 1
    parent: heading
    lines: ['some text']
    children:
        sub-heading
    >>> print(n2)
    Heading: 'sub-heading'
    level: 2
    parent: heading
    lines: []
    children:

    >>> n2.print_text()
    sub-heading
    +++++++++++
    >>> n.print_text()
    heading
    -------
    some text
    sub-heading
    +++++++++++
    """
    _chars="=-+:*^_~<>"
    def __init__(self, heading, level, parent=None):
        self._heading= transform(heading.strip())
        self._level  = level
        self._lines  = []
        self._parent= parent
        self._children= []
        if parent is not None:
            parent.add_child(self)
    def heading(self):
        """return the heading."""
        return self._heading
    def add_child(self, child):
        """add a child."""
        self._children.append(child)
    def add_line(self, line):
        """add a line."""
        transformed= transform(line.rstrip())
        if transformed is not None:
            self._lines.append(transform(line.rstrip()))
    def children(self):
        """return the children."""
        return self._children
    def level(self):
        """return the level."""
        return self._level
    def parent(self):
        """return the parent."""
        if self._parent is None:
            return self
        return self._parent
    def __str__(self):
        # pylint: disable= protected-access
        lines= ["Heading: %s" % repr(self._heading),
                "level: %d" % self._level,
                "parent: %s" % self.parent()._heading,
                "lines: %s" % repr(self._lines),
                "children:"]
        for c in self._children:
            lines.append("    %s" % c._heading)
        return "\n".join(lines)
    def _heading_text(self):
        # pylint: disable= protected-access
        ch= self.__class__._chars[self._level]
        return(self._heading,ch * len(self._heading))
    def to_text(self):
        """returns list of lines representing the chapter."""
        lines= []
        ht= self._heading_text()
        if ht[0]:
            # do not append if self._heading_text()[0]==""
            lines.extend(self._heading_text())
            lines.extend(self._lines)
        for c in self._children:
            #lines.append("")
            lines.extend(c.to_text())
        return lines
    def to_index(self, level=0):
        """returns a list of lines representing an index."""
        lines= []
        h= self._heading_text()[0]
        # do not append if self._heading_text()[0]==""
        if h:
            lines.append(("    "*level)+h)
        for c in self._children:
            lines.extend(c.to_index(level+1))
        return lines
    def print_index(self):
        """print as index."""
        print("\n".join(self.to_index()))
    def print_text(self):
        """print as text."""
        print("\n".join(self.to_text()))

class Rst():
    """scan RST text, provide query and print functions.
    Here are some examples:
    >>> text='''
    ... Reference
    ... =========
    ...
    ... StructuredData in general
    ... -------------------------
    ...
    ... StructuredData is the concept of organizing data in a special hierarchical data
    ... structure. First we have to define the terms used in the following chapters.
    ...
    ... Reference
    ... +++++++++
    ...
    ... The same item again.
    ... '''
    >>> r=Rst(text.splitlines())
    >>> r.print_index()
        Reference
            StructuredData in general
                Reference
    >>> r.print_text()
    Reference
    ---------
    <BLANKLINE>
    StructuredData in general
    +++++++++++++++++++++++++
    <BLANKLINE>
    StructuredData is the concept of organizing data in a special hierarchical data
    structure. First we have to define the terms used in the following chapters.
    <BLANKLINE>
    Reference
    :::::::::
    <BLANKLINE>
    The same item again.
    >>> r.print_text("StructuredData in general")
    StructuredData in general
    +++++++++++++++++++++++++
    <BLANKLINE>
    StructuredData is the concept of organizing data in a special hierarchical data
    structure. First we have to define the terms used in the following chapters.
    <BLANKLINE>
    Reference
    :::::::::
    <BLANKLINE>
    The same item again.
    >>> r.print_text("Reference")
    more than one item found:
    1 at top level
    3 below 'StructuredData in general'
    please call again with the matching number
    >>> r.print_text("Reference",1)
    Reference
    ---------
    <BLANKLINE>
    StructuredData in general
    +++++++++++++++++++++++++
    <BLANKLINE>
    StructuredData is the concept of organizing data in a special hierarchical data
    structure. First we have to define the terms used in the following chapters.
    <BLANKLINE>
    Reference
    :::::::::
    <BLANKLINE>
    The same item again.
    >>> r.print_text("Reference",2)
    not found with this index
    >>> r.print_text("Reference",3)
    Reference
    ---------
    <BLANKLINE>
    StructuredData in general
    +++++++++++++++++++++++++
    <BLANKLINE>
    StructuredData is the concept of organizing data in a special hierarchical data
    structure. First we have to define the terms used in the following chapters.
    <BLANKLINE>
    Reference
    :::::::::
    <BLANKLINE>
    The same item again.
    """
    @classmethod
    def from_file(cls, filename):
        """create object from a file."""
        return cls(read_file(filename))
    def __init__(self, lines):
        def build_tree(elements, heading_chars):
            """build the tree."""
            top= Node("",0)
            curr= top
            for l in elements:
                if not isinstance(l, tuple):
                    curr.add_line(l)
                    #print "ADD:",l
                    continue
                (char, heading)= l
                level= heading_chars[char]
                while level<=curr.level():
                    curr= curr.parent()
                new= Node(heading, level, curr)
                curr= new
            return top
        def node_dict(topnode):
            """create a dictionary of nodes."""
            def _add_node(dict_, node):
                l= dict_.get(node.heading())
                if l is None:
                    l= []
                    dict_[node.heading()]= l
                l.append(node)
                for c in node.children():
                    _add_node(dict_, c)
            dict_= {}
            _add_node(dict_, topnode)
            return dict_

        elements= list(scan_headings(lines))
        heading_chars= count_headings(elements)
        self._top= build_tree(elements, heading_chars)
        self._nodedict= node_dict(self._top)
    def _select(self, as_index= False, heading="", level=None):
        # pylint: disable=too-many-return-statements
        l= self._nodedict.get(heading)
        if l is None:
            return ["not found"]
        if level is None:
            if len(l)==1:
                # pylint: disable= no-else-return
                if as_index:
                    return l[0].to_index()
                else:
                    return l[0].to_text()
            lines= ["more than one item found:"]
            for it in l:
                if it.level()<=1:
                    lines.append("%d at top level" % it.level())
                else:
                    lines.append("%d below '%s'" %
                                 (it.level(), it.parent().heading()))
            lines.append("please call again with the matching number")
            return lines
        for it in l:
            if it.level()==level:
                # pylint: disable= no-else-return
                if as_index:
                    return l[0].to_index()
                else:
                    return l[0].to_text()
        lines= ["not found with this index"]
        return lines
    def text(self, heading="", level=None):
        """return as text."""
        return self._select(False, heading, level)
    def index(self, heading="", level=None):
        """return as index."""
        return self._select(True, heading, level)
    def print_text(self, heading="", level=None):
        """print as text."""
        print("\n".join(self.text(heading, level)))
    def print_index(self, heading="", level=None):
        """print as index."""
        print("\n".join(self.index(heading, level)))

#lines= read_file("TEST.rst")
#r= Rst(lines)
#r.print_text()

def _test():
    # pylint: disable= import-outside-toplevel
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
