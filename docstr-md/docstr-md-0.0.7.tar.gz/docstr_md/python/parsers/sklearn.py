import ast
import re


class Sklearn():
    """
    Parses sklearn-style docstrings.

    Parameters
    ----------
    raw_sections : iterable of strings, default=('Notes','Examples')
        List of section names whose content will be treated as raw markdown. 
        Other sections are treated as fields.

    Attributes
    ----------
    raw_sections : iterable of strings
        From `raw_sections` parameter.

    Notes
    -----
    `'\\'` functions as an escape character when added to the beginning of a 
    line. Whitespace to its left will be stripped. All text to its right will 
    be treated as raw markdown.

    Examples
    --------
    ```python
    from docstr_md.python import parsers

    docstr_txt = '''
    Description.

    Field0
    \------
    \item0 : short description
    \    Long description.

    \item1 : short description
    \   Long description.

    Field1
    \------
    \item0 : short description
    \   Long description

    Notes
    \-----
    \Here is a note.

    Examples
    \--------
    \Here is an example.
    '''

    parser = parsers.Sklearn()
    parser(docstr_txt)
    ```

    Out:

    ```
    {
    \    'description': 'Description.', 
    \    'sections': [
    \        ('Notes', 'Here is a note.'), 
    \        ('Examples', 'Here is an example.')
    \    ], 
    \    'fields': [
    \        {
    \            'name': 'Field0', 
    \            'items': [
    \                {
    \                    'name': 'item0', 
    \                    'short_desc': 'short description', 
    \                    'long_desc': 'Long description.'
    \                }, 
    \                {
    \                    'name': 'item1', 
    \                    'short_desc': 'short description', 
    \                    'long_desc': 'Long description.'
    \                }
    \            ]
    \        }, 
    \        {
    \            'name': 'Field1', 
    \            'items': [
    \                {
    \                    'name': 'item0', 
    \                    'short_desc': 'short description', 
    \                    'long_desc': 'Long description'
    \                }
    \            ]
    \        }
    \    ]
    }
    ```
    """
    def __init__(self, raw_sections=('Notes', 'Examples')):
        self.raw_sections = raw_sections

    def __call__(self, obj):
        """
        Parses the docstring.

        Parameters
        ----------
        obj : str or docstr_md.python.soup_objects.Expr
            Raw docstring to be parsed.

        Returns
        -------
        docstr : dict
            Parsed docstring dictionary. A dictionary contains a description 
            (str), raw markdown sections (list), and fields (list). Each 
            section is a (name, markdown) tuple. Each field contains a name 
            (str) and items (list). Each item contains a name (str), a short 
            description (usually the data type, str), and a long description 
            (str).
        """
        if isinstance(obj, str):
            return self._parse(obj)
        try:
            if bool(obj.value.s):
                return self._parse(obj.value.s)
        except:
            pass
        return {'description': '', 'sections': [], 'fields': []}
        
    def _parse(self, docstr_txt):
        """
        Parse a raw docstring.

        Parameters
        ----------
        docstr_txt : str
            Raw docstring.
        """
        docstr = {'description': '', 'sections': [], 'fields': []}
        section_names, sections = self._get_sections(docstr_txt)
        docstr['description'] = self._parse_lines(sections.pop(0))
        docstr['sections'] = [
            self._parse_section(name, section_names, sections)
            for name in self.raw_sections if name in section_names
        ]
        docstr['fields'] = [
            self._parse_field(name, section) 
            for name, section in zip(section_names, sections) 
        ]
        return docstr

    def _get_sections(self, docstr_txt):
        """
        Get section names and sections.

        Sections are delimited by a line of dashes. e.g.

        Section name
        ------------
        Content
        """
        sections = re.split(r'\n\s*?-+\n', docstr_txt)
        sections = [section.splitlines() for section in sections]
        sections = [
            [self._clean_line(line) for line in section] 
            for section in sections
        ]
        section_names = [sections[i-1].pop() for i in range(1, len(sections))]
        return section_names, sections 

    def _clean_line(self, line):
        """
        Clean a line of a section.

        Use '\' as a escape character at the beginning of a line. e.g.

        \----------

        is interpreted as '----------'
        """
        line = line.strip()
        return line[1:] if re.match(r'\\', line) else line
        
    def _parse_lines(self, lines):
        """
        Parse the lines of a section.

        Parameters
        ----------
        lines : list
            List of strings.
        """
        return ''.join(['\n'+line for line in lines]).strip()

    def _parse_section(self, name, section_names, sections):
        """
        Parse a raw markdown section.

        Parameters
        ----------
        name : str
            Section name.

        section_names : list of str
            All section names in the docstring.

        sections : list of lists of section lines
        """
        idx = section_names.index(name)
        section_names.pop(idx)
        content = self._parse_lines(sections.pop(idx))
        return (name, content)   

    def _parse_field(self, name, lines):
        """
        Parse a field (i.e. a section not designated as raw markdown).

        Parameters
        ----------
        name : str
            Field name.

        lines : list of str
            Lines of field text.
        """
        field = {'name': name}
        while lines and lines[-1] == '':
            lines.pop()
        idx_list = [idx for idx, val in enumerate(lines) if val == '']
        idx_list.append(len(lines))
        idx_list = zip([-1]+idx_list[:-1], idx_list)
        field['items'] = [
            self._parse_item(name, lines[i+1:j]) for i, j in idx_list
        ]
        return field

    def _parse_item(self, name, lines):
        """
        Parse an item.

        Parameters
        ----------
        name : str
            Item name.

        lines : list of str
            List of item lines (text).
        """
        item = {}
        head = lines.pop(0).split(':', maxsplit=2)
        name, short_desc = head if len(head) == 2 else (head[0], '')
        item['name'], item['short_desc'] = name.strip(), short_desc.strip()
        item['long_desc'] = ' '.join(lines)
        return item