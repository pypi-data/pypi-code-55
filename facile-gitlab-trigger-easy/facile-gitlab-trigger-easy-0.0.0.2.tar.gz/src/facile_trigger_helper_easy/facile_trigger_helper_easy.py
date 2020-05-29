"""GitLab trigger module.
This module helps docker bypassing "multi-project pipelines"
capability which is covered on on gitLab silver or higher.
"""
import sys
import time
import argparse
from typing import List
from colors import color
import gitlab


class facile_trigger_helper_easy:
    """

        :param args:
        :return: Args trasformed by the user
    """
    @staticmethod
    def convert_args(args: List[str]):

        """

        :param args:
        :return: Args trasformed by the user
        """
        parser = argparse.ArgumentParser(
            description='Gilab trigger helper',
            add_help=False)

        parser.add_argument('-a', '--api-token', required=True,
                            help='personal access token (not required when running detached)',
                            dest='gitlab_api_token')

        parser.add_argument('-h', '--host', default='gitlab.com', dest="git_lab_host")

        parser.add_argument('--help', action='help', help='show this help message and exit')

        parser.add_argument('-t', '--target-ref', default='master',
                            help='target ref (branch, tag, commit)', dest='target_branch')

        parser.add_argument('-p', '--project-id', required=True,
                            help='repository id found on settings', dest='project_id')

        parsed_args = parser.parse_args(args)

        return parsed_args

    def main(self, args: List[str]):

        """

        :project_id variable aims gitlab id found on project >> General:
        """
        # Require parameters
        args = self.convert_args(args)
        assert args.gitlab_api_token, 'token should be set'
        assert args.project_id, 'project id must be set'

        #  Moving args to local variables
        git_lab_host = args.git_lab_host
        project_id = args.project_id
        api_gilab_token = args.gitlab_api_token
        target_branch = args.target_branch

        facile_trigger_helper_easy.trigger_pipeline(git_lab_host, api_gilab_token,
                                                    target_branch, project_id)
               
    @staticmethod
    def trigger_pipeline(git_lab_host, api_gilab_token, target_branch, project_id):
        """

        :project_id variable aims gitlab id found on project >> General:
        """

        git_trigger = gitlab.Gitlab(git_lab_host, private_token=api_gilab_token)
        project = git_trigger.projects.get(project_id)
        create_pipeline = project.pipelines.create(
            {'ref': target_branch, 'variables': [{'key': 'TRIGG_TEST', 'value': project_id}]})

        pipeline = project.pipelines.get(create_pipeline.id)
        pipe_jobs = pipeline.jobs.list()
        pipeline_jobs_count = len(pipe_jobs)
        pipeline_jobs_count = str(pipeline_jobs_count)
        print(color("Triggered pipeline holds " + pipeline_jobs_count + " jobs", fg='yellow'))
        timeout = time.time() + 60 * 30

        while pipeline.finished_at is None:

            pipeline.refresh()

            if pipeline.status == "pending":
                print(color(project.name + " is " + pipeline.status, fg='yellow'))
            elif pipeline.status == "running":
                print(color(project.name + " is " + pipeline.status, fg='blue'))
            if pipeline.status == "success":
                print(color(project.name + " is " + pipeline.status, fg='green'))
            elif pipeline.status == "failed":
                print(color(project.name + " is " + pipeline.status, fg='red'))
                sys.exit(1)
            elif pipeline.status == "canceled":
                print(color(project.name + " is " + pipeline.status, fg='red'))
                sys.exit(1)
            elif time.time() > timeout:
                print(color(project.name + " is " + pipeline.status, fg='red'))
                sys.exit(1)

            time.sleep(2)


def run_cli(arguments=None):
    """

    :project_id variable aims gitlab id found on project >> General:
    """
    if arguments is None:
        arguments = sys.argv[1:]

    return facile_trigger_helper_easy().main(arguments)


if __name__ == '__main__':
    run_cli(sys.argv[1:])
    sys.exit(0)
