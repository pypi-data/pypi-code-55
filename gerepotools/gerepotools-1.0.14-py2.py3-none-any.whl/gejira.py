#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
# -----------------------------------------------------------------------------
import sys
import os
import os.path
import logging
import codecs
import yaml
import jinja2
from jira import JIRA
from brainyquote import pybrainyquote
import upref

from . import core

# -----------------------------------------------------------------------------
def fill_jira_target(project=None,
                     force_renew=False):
    """ Fill the target usage of the jira.

    @param group the group of the target
    @param repo_id Id of the repo

    @return (group, repo_id)
    """

    if project is not None:
        return project

    conf_filename = os.path.join(__get_this_folder(),
                                 "templates", "repotools-jira-target-last.yml")

    conf_filename = core.check_is_file_and_correct_path(conf_filename)

    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        data_desc = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if project is not None:
        data_desc['project']['value'] = project

    data = upref.get_pref(data_desc, 'repotools-jira-target-last',
                          force_renew=force_renew)

    return data['project']

# -----------------------------------------------------------------------------
def fill_jira_credential(url=None, login=None, password=None,
                         force_renew=False):
    """ Fill url, login, password with the user preference.

    @param url URL of the repository
    @param login The url
    @param password The password

    @return (url,login,password)
    """

    if url is not None and login is not None and password is not None:
        return (url, login, password)

    conf_filename = os.path.join(__get_this_folder(),
                                 "templates", "repotools-jira-credential.yml")

    conf_filename = core.check_is_file_and_correct_path(conf_filename)

    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        data_desc = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if url is not None:
        data_desc['url']['value'] = url
    if login is not None:
        data_desc['login']['value'] = login
    if password is not None:
        data_desc['password']['value'] = password

    data = upref.get_pref(data_desc, 'repotools-jira-credential',
                          force_renew=force_renew)

    return (data['url'], data['login'], data['password'])


# -----------------------------------------------------------------------------
# create an issue on Jira
# -----------------------------------------------------------------------------
def create_issue(artifact, project=None, url=None, login=None, password=None,
                 quote=None):

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(__get_this_folder(),
                                                    "templates")),
        autoescape=jinja2.select_autoescape(['html', 'xml']))

    if quote is None:
        quote = pybrainyquote.get_quotes('inspirational')[0]

    context = {
        "artifact": artifact,
        "quote": quote,
    }

    description = template_env.get_template("jira_issue.j2").render(context)
    summary = "[%s] %s %s" % (artifact.artifact,
                              artifact.group, artifact.version)

    (url, login, password) = fill_jira_credential(url, login, password)
    project = fill_jira_target(project, force_renew=True)

    connector = JIRA(url, basic_auth=(login, password), max_retries=0)

    result = connector.create_issue(project=project,
                                    summary=summary,
                                    description=description,
                                    issuetype={'name': 'Delivery Bill'})

    logging.info("Create the jira issue %s", result)
    return result


###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the folder of THIS script.
###############################################################################
def __get_this_folder():
    return os.path.split(os.path.abspath(os.path.realpath(
        __get_this_filename())))[0]


###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the filename of THIS script.
###############################################################################
def __get_this_filename():
    result = ""

    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__

    return result
