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
import codecs
import logging
import yaml
import jinja2
from brainyquote import pybrainyquote
import json
import requests

import upref

from . import core

# -----------------------------------------------------------------------------
def fill_slack_credential(webhook_url=None, force_renew=False):
    """ Fill url, login, password with the user preference.

    @param url URL of the repository

    @return (url,login,password)
    """

    if webhook_url is not None:
        return webhook_url

    conf_filename = os.path.join(__get_this_folder(),
                                 "templates", "repotools-slack-credential.yml")

    conf_filename = core.check_is_file_and_correct_path(conf_filename)

    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        data_desc = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if webhook_url is not None:
        data_desc['webhook_url']['value'] = webhook_url

    data = upref.get_pref(data_desc, 'repotools-slack-credential',
                          force_renew=force_renew)

    return data['webhook_url']


# -----------------------------------------------------------------------------
# create an issue on Jira
# -----------------------------------------------------------------------------
def slack_message(artifact, jira_issue=None, jira_url=None,
                  webhook_url=None, quote=None):

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

    if jira_issue is not None:
        context['jira'] = jira_issue

    if jira_url is not None:
        if jira_url[-1] != '/':
            jira_url = jira_url + "/"
        context['jira_url'] = jira_url

    description = template_env.get_template(
        "slack_message.json.j2").render(context)

    webhook_url = fill_slack_credential(webhook_url)

    slack_data = "{'blocks': %s}" % description

    response = requests.post(
        webhook_url, data=slack_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    logging.info("Create the slack message")
    return slack_data


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
