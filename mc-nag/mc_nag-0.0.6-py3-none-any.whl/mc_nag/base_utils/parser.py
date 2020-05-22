"""BaseParser class."""

import re
from json.decoder import JSONDecodeError
import jstyleson
from yaml import safe_load
from yaml.scanner import ScannerError as YamlScannerError
from yaml.parser import ParserError as YamlParserError
from mc_nag.base_utils.exceptions import InvalidTemplate


class BaseParser:
    """Parser class to interpret raw templates."""

    def __init__(self, template_string, parameter_file=None):
        """Init parser object with template and parsed template."""
        self.template_string = template_string
        self.parsed_template = self.parse_raw_file(self.template_string)
        self.validate_file(file_type='Template', parsed_contents=self.parsed_template)
        self.file_lines = template_string.split('\n')
        self.parameter_file = parameter_file
        self.parsed_parameter_file = self.parse_raw_file(self.parameter_file)
        self.validate_file(file_type='Parameter', parsed_contents=self.parsed_parameter_file)

    @staticmethod
    def parse_raw_file(file_contents=None):
        """Return parsed dictionary."""
        if file_contents is not None:
            try:
                return safe_load(file_contents)
            except (YamlParserError, YamlScannerError):
                try:
                    return jstyleson.loads(file_contents)
                except JSONDecodeError:
                    raise InvalidTemplate('Invalid YAML or JSON syntax!')
        else:
            return None

    @staticmethod
    def validate_file(file_type=None, parsed_contents=None, required_keys=None,
                      exception_class=InvalidTemplate):
        """Check template string for basic requirements."""
        if required_keys and not all(key in parsed_contents
                                     for key in required_keys):
            missing_keys = ', '.join([key for key in required_keys
                                      if key not in parsed_contents])
            message = f'{file_type} file is missing the {missing_keys} key(s)!'
            raise exception_class(message)

    def find_line_number(self, search_pattern: str) -> int:
        """Return line number from original template from search pattern."""
        regex_pattern = re.compile(re.escape(search_pattern))
        matched_lines = list(filter(regex_pattern.search,
                                    self.file_lines))
        try:
            return self.file_lines.index(matched_lines[0]) + 1
        except IndexError:
            return -1

    @property
    def resources(self):
        """Return parsed resources dict."""
        return self.parsed_template['resources']

    @property
    def parameters(self):
        """Return parsed parameters dict."""
        return self.parsed_template.get('parameters', {})

    @property
    def variables(self):
        """Return parsed variables dict."""
        return self.parsed_template.get('variables', {})

    @property
    def functions(self):
        """Return parsed functions dict."""
        return self.parsed_template.get('functions', {})

    @property
    def outputs(self):
        """Return parsed outputs dict."""
        return self.parsed_template.get('outputs', {})
