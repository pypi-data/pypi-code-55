"""
Deprecated or unused code.
"""


def _is_df_like(df):
    """Check if an object is a 2D Pandas object (ie. a DataFrame).

    This cannot be accomplished just by checking `isinstance(df, DataFrame)`
    because of the use of utility classes like BlockManager.
    """
    if not isinstance(df, PandasObject):
        return False
    try:
        return df.ndim == 2
    except AttributeError:
        return False


def parse_df_from_html(html_df):
    parser = HTMLDFParser(html_df)
    return DataFrame(parser.rows, columns=parser.colnames)


class HTMLDFParser(HTMLParser):
    def __init__(self, html_df, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._section = None
        self._current_tag = None
        
        self.colnames = []
        self.rows = []
        
        self.feed(html_df)
    
    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        if tag in ("thead", "tbody"):
            self._section = tag
        elif tag == "tr" and self._section == "tbody":
            self.rows.append([])
    
    def handle_data(self, data):
        if self._section == "thead" and self._current_tag == "th":
            # Index column will be ignored if not named.
            self.colnames.append(data)
        elif self._section == "tbody" and self._current_tag == "td":
            # Ignores index column (which uses 'th')
            self.rows[-1].append(data)
            
    def handle_endtag(self, tag):
        # Only capture data inside the innermost tags.
        self._current_tag = None


def run_in_notebook(func_name, *args):
    """Call a function in a Jupyter notebook code cell and capture the output.

    This can be used for testing code that interacts with the notebook
    environment, eg. rich output formatting. For clarity and consistency with
    `pytest` philosophy, the code to be run should be encapsulated in a single
    function defined in this module which accepts simple args (see below).

    Parameters
    ----------
    func_name : str
        The name of the function to run. It must be importable from this module.
    args: str
        Arguments to pass to the function. These must be either Python literal
        strings or names of symbols defined in this module. If a symbol is
        callable, it will be replaced with its return value prior to calling
        the function.

    Returns
    -------
    dict
        The dict representing the cell output in the Jupyter notebook format.
    """
    ## Symbols that need to be imported in order to run the notebook.
    to_import = [func_name]
    ## String representations of the args to pass to the function.
    call_args = []
    for a in args:
        try:
            ## Is the arg a valid string literal?
            ast.literal_eval(a)
        except ValueError:
            ## Arg is not a literal.
            ## Interpret as a symbol name.
            if a not in globals():
                err_msg = "Notebook test runner can only handle function" + \
                          " args that are either literal or defined symbol" + \
                          " names"
                raise ValueError(err_msg.format(a))
            to_import.append(a)
            if callable(globals()[a]):
                ## The arg represents a function.
                ## Make sure to evaluate it first.
                a += "()"
        finally:
            call_args.append(a)

    to_import_str = ",".join(to_import)
    call_args_str = ",".join(call_args)
    source = "from {module} import {symb}".format(module=__name__,
                                                  symb=to_import_str)
    source += "\n{func}({args})".format(func=func_name,
                                        args=call_args_str)

    ## Create a notebook with a single code cell that calls the function.
    code_cell = new_code_cell(source)
    nb = new_notebook()
    nb.cells.append(code_cell)
    ## Run the notebook to capture the output.
    ep = ExecutePreprocessor()
    ep.preprocess(nb, {})

    return code_cell.outputs

