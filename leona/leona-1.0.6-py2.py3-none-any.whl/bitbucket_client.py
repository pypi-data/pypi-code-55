#!/usr/bin/python3.6
import os
import requests
import json
import subprocess
from os import environ
from os.path import basename
from requests.auth import HTTPBasicAuth
from src.utils import get_config

config = get_config()
bit_user = config["bitbucket"]["username"]
bit_pass = config["bitbucket"]["password"]
base_url = 'https://api.bitbucket.org/2.0/repositories/hlcn'
auth = HTTPBasicAuth(bit_user, bit_pass)  
headers = {"Accept": "application/json"}

#! BITBUCKET    
def get_commits(repo_name):
    url = '%s/%s/commits' % (base_url,repo_name)
    response = requests.request("GET",url,headers=headers,auth=auth)
    commits = json.loads(response.text)
    return commits

def create_pull_request(title, description, branch, reviewers, repo_name):
    if len(reviewers) == 0:
        json_data = {
            "title": title,
            "description": description,
            "destination": {
                "branch": {
                    "name": "develop"
                }
            },
            "source": {
                "branch": {
                    "name": branch
                }
            }
        }
    else:
        json_data = {
            "title": title,
            "description": description,
            "destination": {
                "branch": {
                    "name": "develop"
                }
            },
            "source": {
                "branch": {
                    "name": branch
                }
            },
            "reviewers": reviewers
        }
    url = "%s/%s/pullrequests" % (base_url,repo_name)
    response = requests.post(url,json=json_data,headers=headers,auth=auth)
    json_data = json.dumps(response.text)
    return json_data
def get_current_repo_name():
    command = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE)
    command = command.stdout.decode('utf-8')
    repo_name = basename(command)
    return repo_name

def get_current_branch_name():
    command = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    branch_name = command.stdout.decode('utf-8')
    return branch_name

def get_reviewers(repo_name):
    reviewers_uuid, reviewers_name = ([] for i in range(2))
    url = '%s/%s/default-reviewers' % (base_url ,repo_name)
    response = requests.request("GET",url,headers=headers,auth=auth)
    reviewers_response = json.loads(response.text)
    for reviewer in reviewers_response['values']:
        reviewers_name.append(reviewer['display_name'])
        reviewers_uuid.append(reviewer['uuid'])
    return reviewers_name, reviewers_uuid

def get_formated_uuid(reviewers_result, reviewers_name, reviewers_uuid):
    formated = []
    reviewers_dict = [{'name': i, 'uuid': j} for (i, j) in zip(reviewers_name, reviewers_uuid)]
    for reviewer in reviewers_dict:
        for reviewer_name in reviewers_result:
            if reviewer_name == reviewer['name']:
                formated.append(reviewer['uuid'])
    formated = [{'uuid': i} for (i) in zip(formated)]
    formated_uuid = str(formated).replace("(","").replace(",)", "")
    return formated_uuid

def get_diffs_data(diffs):
    diffs_data = []
    for diff in diffs:
        response = requests.request("GET",diff,headers=headers,auth=auth)
        diffs_data.append(response.text)
    return diffs_data

def get_diffs_stats(hashs,repo):
    lines_added = 0
    lines_removed = 0
    diff_stats, response_data, added, removed = ([] for i in range(4))
    for hashs_item in hashs:
        url = '%s/%s/diffstat/%s' % (base_url,repo, hashs_item)
        response = requests.request("GET",url,headers=headers,auth=auth).json()
        for item in response['values']:
            if 1 < len(response['values']):
                lines_added += item['lines_added']
                lines_removed += item['lines_removed']    
            else:
                lines_added = item['lines_added']
                lines_removed = item['lines_removed']
            added.append('lines added: %s' % lines_added)
            removed.append('lines removed: %s' % lines_removed)
    return added, removed