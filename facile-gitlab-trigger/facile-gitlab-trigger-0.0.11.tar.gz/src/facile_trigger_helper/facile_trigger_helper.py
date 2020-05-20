"""GitLab trigger module.
This module helps docker bypassing "multi-project pipelines"
capability which is covered on on gitLab silver or higher.
"""
import sys
import time
import argparse
from typing import List
from blessings import Terminal
from colors import *
import pyfiglet
import gitlab
import yaml
import os

class facile_trigger_helper(object):
    """

        :param args:
        :return: Args trasformed by the user
    """

    def convert_args(self, args: List[str]):

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
        parser.add_argument('-b', '--branch-merged', required=True,
                            help='filled by git COMMIT_REF_NAME ', dest='ref_name')
        parser.add_argument('-f', '--yaml-file', required=True,
                            help='filled by git COMMIT_REF_NAME ', dest='yaml_file')

        parsed_args = parser.parse_args(args)

        return parsed_args

    def check_project(self, string_project, yaml_file):
        """

        :project_id variable aims gitlab id found on project >> General:
        """

        with open(yaml_file) as file:
            documents = yaml.safe_load(file)
            robot_path = ''
            for project_id, path in documents.items():
                if str(project_id) in string_project.upper():
                    robot_path = path               

            return robot_path


    def main(self, args: List[str]):
       
        """

        :project_id variable aims gitlab id found on project >> General:
        """
        # Require parameters
        args = self.convert_args(args)
        assert args.gitlab_api_token, 'token should be set'
        assert args.project_id, 'project id must be set'
        assert args.yaml_file, 'please provide valid yaml path'

        #  Moving args to local variables
        git_lab_host = args.git_lab_host
        project_id = args.project_id
        api_gilab_token = args.gitlab_api_token
        target_branch = args.target_branch
        #ref_name = args.ref_name
        print(args.ref_name)
        robot_path = self.check_project(args.ref_name, args.yaml_file)

        if robot_path:
            
            facile_trigger = pyfiglet.figlet_format("facile.it Trigger Helper", font = "larry3d"  ) 
            print(color(facile_trigger, fg='yellow'))
            print(color("Running robot path: " + robot_path, fg='green'))
        
            self.trigger_pipeline(robot_path, git_lab_host, 
            api_gilab_token, target_branch, project_id)

    def trigger_pipeline(self, ref_name, git_lab_host, api_gilab_token, target_branch, project_id):
        """

        :project_id variable aims gitlab id found on project >> General:
        """

        git_trigger = gitlab.Gitlab(git_lab_host, private_token=api_gilab_token)
        project = git_trigger.projects.get(project_id)
        create_pipeline = project.pipelines.create({'ref': target_branch , 'variables': [{'key': 'RF_PATH', 'value': ref_name }]})
        
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

def run_cli(arguments=None, exit=True):
       
    """

    :project_id variable aims gitlab id found on project >> General:
    """
    if arguments is None:
        arguments = sys.argv[1:]
    
    return facile_trigger_helper().main(arguments)
            
if __name__ == '__main__':
    run_cli(sys.argv[1:])
    sys.exit(0)