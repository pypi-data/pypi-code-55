from jira import JIRA
from src.imports import os
from src.imports import environ
from src.utils import get_config

config = get_config()
jira_user = config["jira"]["username"]
jira_token = config["jira"]["token"]
base_url = 'https://heliconjira.atlassian.net'
options = {'server': base_url}
jira = JIRA(options, basic_auth=(jira_user, jira_token))
#! JIRA
def get_projects_names():
  names = []
  for project in jira.projects():
      names.append(project.name)
  return names

def get_projects_keys():
  keys = []
  for project in jira.projects():
      keys.append(project.key)
  return keys

def get_issues_project(project):
  issues = []
  jql = 'project =%s AND status not in (Closed, Resolved, Done) AND assignee=currentuser()' % project
  for issue in jira.search_issues(jql_str= jql,maxResults=200):
    issues.append(issue.key)
  return issues

def get_all_issues(project_name, fields):
    issues = []
    i = 0
    chunk_size = 100
    while True:
        chunk = jira.search_issues(f'project = {project_name}', startAt=i, maxResults=chunk_size, fields=fields)
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues