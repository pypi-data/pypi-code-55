"""Main controller module."""

from importlib import resources
from markdown import markdown
from weasyprint import HTML
from . import pkgname

class DocumentError(Exception):
    """Basic exception raised by the program."""


class Document(object):

    """Controler class."""

    def __init__(self, config_file=None):

        """
        :param config_file: If given, the path to the configuration file
        """

        self.config_file = config_file
        self._config = None

    @property
    def config(self):

        """Load configuration from file"""

        try:
            if not self._config:
                self._config = yaml.safe_load(open(self.config_file, 'r'))

        except FileNotFoundError:
            raise DocumentError(f'No config file found at {self.config_file}')

        except yaml.YAMLError as e:
            logger.debug(e)
            raise DocumentError(f'Error loading configuration from {self.config_file}')

    @config.setter
    def config(self, value):

        """Set a dict has current configuration."""

        self._config = value

    @property
    def templates(self):

        """Return the list of available templates."""

        with resources.path(pkgname, 'samples') as _dir:
            return _dir.rglob('*.md')

    @property
    def styles(self):

        """Return the list of available styles."""

        with resources.path(pkgname, 'styles') as _dir:
            return _dir.rglob('*.css')

    def create(self, path, template):

        """Create a new document from a template."""

        if not path:
            raise DocumentError('No document name to create')

        try:
            # find template path
            template_path = next(elt for elt in self.templates if elt.name == template)
        except StopIteration:
            raise DocumentError(f'Template "{template}" not found.')

        # write document
        path.write_text(template_path.read_text())

    def convert(self, style, input, output):

        """Convert markdown to PDF"""

        try:
            # load style
            css = next(elt for elt in self.styles if elt.name == style)
        except StopIteration:
            raise DocumentError(f'Style "{style}" not found.')

        # convert to HTML
        html_text = markdown(input.read(), extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.attr_list',
                'markdown.extensions.fenced_code'
            ], output_format='html5')

        # convert to PDF
        HTML(string=html_text).write_pdf(output, stylesheets=[css])
