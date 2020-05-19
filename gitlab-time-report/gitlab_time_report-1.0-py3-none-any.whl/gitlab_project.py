import gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabParsingError
from requests.exceptions import ConnectionError


class GitLabProject:
    """Builds a connection to a GitLab project and enables access to its issues."""

    def __init__(self, gitlab_url, access_token):
        """
            :param gitlab_url: An URL to a GitLab project.
            :param access_token: A personal access token that provides access to the project.

            Calls the :py:func:`get_project_issues` to receive a list of issues from the project.
        """
        self.gitlab_url = gitlab_url
        self.access_token = access_token
        self.issues = self.get_project_issues()

    def get_project_issues(self):
        """Connects to a GitLab project through the GitLab REST API and gets the project issues.

            :return: A list of :py:class:`ProjectIssue` objects.

            Receives GitLab data with help from python-gitlab. See https://python-gitlab.readthedocs.io/en/stable/.
        """
        dom1, dom2, dom3, project_url = self.gitlab_url.split("/", 3)
        gitlab_domain = f"{dom1}/{dom2}/{dom3}"

        gl = gitlab.Gitlab(gitlab_domain, private_token=self.access_token)
        project = None
        try:
            project = gl.projects.get(project_url)
        except ConnectionError:
            print("GitLab-Domain could not be found or does not exist")
        except GitlabAuthenticationError:
            print("You are not authorized to view this project")
        except GitlabParsingError:
            print("Project could not be found or does not exist")

        if project is None:
            exit(1)

        return project.issues.list(all=True)
