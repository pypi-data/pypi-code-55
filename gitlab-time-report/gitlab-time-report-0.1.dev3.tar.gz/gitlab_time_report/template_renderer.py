from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from gitlab_time_report import bar_chart, cake_chart


def load_template(template):
    """Loads a jinja2 template file. Shows error-message and exits if not found.

        :param template: Path to a template file.

        :return: A loaded template.
    """
    env = Environment(loader=FileSystemLoader(searchpath="./"))

    try:
        return env.get_template(template)
    except TemplateNotFound:
        print(f"Template '{template}' does not exist")
        exit(1)


class TemplateRenderer:
    """Reads and renders a jinja2 template."""

    def __init__(self, template, output_file, issues):
        """
            :param template: Path to a template file.
            :param output_file: Name of the output file.
            :param issues: A list of GitLab issues.

            Calls the :py:func:`load_template` to receive a loaded template.
        """
        self.template = load_template(template)
        self.output_file = Path(output_file)
        if self.output_file.exists():
            print(f"The file '{self.output_file}' already exists")
            exit(1)
        self.issues = issues

    def render(self):
        """Renders a jinja2 template. Creates requested :py:class:`CakeChart` and :py:class:`BarChart` objects.
        Creates a report with :py:attr:`output_file` as its name.
        """
        try:
            with open(self.output_file, "w") as report:
                report.write(
                    self.template.render(
                        CakeChart=cake_chart.CakeChart(self.issues),
                        BarChart=bar_chart.BarChart(self.issues),
                    )
                )
        except PermissionError:
            print(f"Cannot create '{self.output_file}': Permission denied")
            exit(1)
