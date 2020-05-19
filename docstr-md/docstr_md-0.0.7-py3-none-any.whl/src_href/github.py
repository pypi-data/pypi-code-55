class Github():
    """
    Compiles a hyperlink for source code stored in a Github repository.

    Parameters
    ----------
    root : str
        Path to the root directory of the source code. e.g. `'https://github.com/<username>/blob/master'`.

    Attributes
    ----------
    root : str
        Set from the `root` parameter.

    Examples
    --------
    ```python
    from docstr_md.python import PySoup, compile_md
    from docstr_md.src_href import Github

    src_href = Github('https://github.com/my-username/my-package/blob/master')
    soup = PySoup(path='path/to/file.py', src_href=src_href)
    md = compile_md(soup)
    ```

    `md` is a string of compiled markdown with source code links in the class 
    and function headers.
    """
    def __init__(self, root):
        if not root.endswith('/'):
            root += '/'
        self.root = root

    def __call__(self, obj):
        """
        Compile the hyperlink for the source code of the input object.

        Parameters
        ----------
        obj : docstr_md.soup_objects.FunctionDef or ClassDef
            Soup object to whose souce code we are linking.
        
        Returns
        -------
        href : str
            Hyperlink of the form `'<root>/<src_path>#L<lineno>'`.
        """
        return '{root}{src_path}#L{lineno}'.format(
            root=self.root,
            src_path=obj.src_path,
            lineno=obj.lineno,
        )