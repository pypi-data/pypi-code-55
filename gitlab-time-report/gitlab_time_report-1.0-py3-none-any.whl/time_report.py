import argparse
import sys

from gitlab_time_report import __version__ as module_version
from gitlab_time_report import gitlab_project, template_renderer

examples = """How to use gitlab_time_report:

  gitlab_time_report https://gitlab.com/user/project rVE63xwLymYpido9aV1t templates/temp.md.jinja2 report
  \t-> Connects to your GitLab project 'https://gitlab.com/user/project'
  \t   with the given personal access token 'rVE63xwLymYpido9aV1t'
  \t-> Renders the template file 'templates/temp.md.jinja2',
  \t   creates the requested charts from the template by fetching
  \t   the necessary data from the given project. The rendered
  \t   file is then created with the name 'report.md'"""


def main():
    """The main function. Is called first, when the application is run.

        Calls the :py:func:`parse_arguments` and passes the given arguments on.
        Creates a :py:class:`GitLabProject` object with given gitlab_url and access_token.
        Creates a :py:class:`TemplateRenderer` object with a given template and output_file.
        Calls the :py:func:`render` to render the template file.
    """
    args = parse_arguments(sys.argv[1:])
    gitlab_url = args.gitlab_url
    access_token = args.access_token
    template = args.template
    output_file = args.output_file

    project = gitlab_project.GitLabProject(gitlab_url, access_token)
    renderer = template_renderer.TemplateRenderer(template, output_file, project.issues)
    renderer.render()


def parse_arguments(sys_args):
    """Parses the user-given arguments.

        :param sys_args: A list of arguments.

        :returns: A :py:class:`ArgumentParser` object, parsed with the user-given arguments.

        Parses with argparse. See https://python.readthedocs.io/en/stable/library/argparse.html.
    """
    parser = argparse.ArgumentParser(
        description="""With access to the GitLab API, this tool fetches
time related data from project issues and creates
informative charts such as cake or bar charts which
then are saved in markdown report files.""",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=module_version)
    parser.add_argument("gitlab_url", type=str, help="The URL of your GitLab project")
    parser.add_argument("access_token", type=str, help="Your personal access token")
    parser.add_argument("template", type=str, help="A .md.jinja2 template file")
    parser.add_argument("output_file", type=str, help="Name of the report file")

    if len(sys_args) < 1:
        parser.print_help()
        parser.exit(0)

    return parser.parse_args(sys_args)


if __name__ == "__main__":
    main()
