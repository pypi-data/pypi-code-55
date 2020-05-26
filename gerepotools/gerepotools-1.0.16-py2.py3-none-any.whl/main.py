#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

import os
import sys
import logging
import ctypes
import argparse
import tempfile
import webbrowser

import gerepotools.inoutstream as ios
import gerepotools.repo as repo
import gerepotools.gejira as gejira
import gerepotools.slack as slack
import gerepotools.core as core


###############################################################################
# Create a windows message box
#
# @param text The message
# @param title The title of the windows
# @return nothing.
###############################################################################
def message_box(text, title):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

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
# Logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'

    if ios.is_frozen():
        log_filename = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            os.path.basename(__get_this_filename()) + '.log'))

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler(ios.initial_stream().stdout)
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    # if not ios.is_frozen():
    logging.getLogger('').addHandler(console)

    return console


###############################################################################
# Find the filename of this file (depend on the frozen or not)
###############################################################################
def get_this_filename():
    result = ""
    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__
    return result


###############################################################################
# Define the parsing of arguments of the command line
###############################################################################
def get_parser_for_command_line():
    description_arg = core.__logo__ + "\n" +\
        "This program take a file and upload it on repo."

    parser = argparse.ArgumentParser(description=description_arg)
    parser.add_argument('--windows',
                        action='store_true', dest='windows',
                        help='Define if we need all popups windows.')
    parser.add_argument('--verbose',
                        action='store_true', dest='verbose',
                        help='Put the logging system on the console for info.')
    parser.add_argument('--console', action='store_true', dest='console',
                        help='Set the output to the standard output '
                        'for console')

    parser.add_argument('--filename', metavar='filename', required=True,
                        help='file to upload.')

    parser.add_argument('--extra-file', nargs='*', dest='extra_files',
                        help='Extra file to upload.')

    parser.add_argument('--package-name', metavar='package_name',
                        required=False,
                        help='Name of the package')

    parser.add_argument('--package-only', action='store_true',
                        dest='package_only', help='Only create the package')

    parser.add_argument('--repo-url', metavar='repo_url', help='url of repo')
    parser.add_argument('--repo-login', metavar='repo_login', help='login')
    parser.add_argument('--repo-password', metavar='repo_password')
    parser.add_argument('--repo-group', metavar='repo_group')
    parser.add_argument('--repo-id', metavar='repo_id')
    parser.add_argument('--release-version', metavar='release_version',
                        help='artifact version')

    parser.add_argument('--jira', action='store_true',
                        dest='jira', help='Post a Jira issue')
    parser.add_argument('--jira-url',
                        metavar='jira_url', help='jira url')
    parser.add_argument('--jira-login',
                        metavar='jira_login', help='jira login')
    parser.add_argument('--jira-password',
                        metavar='jira_password', help='jira password')
    parser.add_argument('--jira-project',
                        metavar='jira_project', help='jira project')

    parser.add_argument('--slack', action='store_true',
                        dest='slack', help='Post a Slack message')
    parser.add_argument('--slack-url',
                        metavar='slack_url', help='Slack url webhook')

    return parser

###############################################################################
# Logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'

    if ios.is_frozen():
        log_filename = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            os.path.basename(__get_this_filename()) + '.log'))

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler(ios.initial_stream().stdout)
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    # if not xe2.inoutstream.is_frozen():
    logging.getLogger('').addHandler(console)

    return console

###############################################################################
# Main script
###############################################################################
def __main():
    console = __set_logging_system()
    # ------------------------------------
    logging.info('+')
    logging.info('-------------------------------------------------------->>')
    logging.info('Started %s', __get_this_filename())
    logging.info('The Python version is %s.%s.%s',
                 sys.version_info[0], sys.version_info[1], sys.version_info[2])

    try:
        parser = get_parser_for_command_line()
        logging.info("parsing args")
        args = parser.parse_args()
        logging.info("parsing done")

        if args.verbose == "yes":
            console.setLevel(logging.INFO)
        if args.console == "yes":
            ios.initial_stream().apply_to_std_stream()
            if ios.is_frozen():
                logging.getLogger('').addHandler(console)

        logging.info(core.__logo__)
        logging.info("windows=%s", args.windows)
        logging.info("console=%s", args.console)
        logging.info("verbose=%s", args.verbose)

        logging.info("filename=%s", args.filename)
        logging.info("extr_files=%s", args.extra_files)
        logging.info("package_name=%s", args.package_name)
        logging.info("package_only=%s", args.package_only)

        logging.info("repo url=%s", args.repo_url)
        logging.info("repo login=%s", args.repo_login)
        logging.info("repo password=%s",
                     len(args.repo_password) * "*"
                     if args.repo_password else "None")
        logging.info("repo group=%s", args.repo_group)
        logging.info("repo id=%s", args.repo_id)
        logging.info("release_version=%s", args.release_version)

        logging.info("jira=%s", args.jira)
        logging.info("jira_url=%s", args.jira_url)
        logging.info("jira_login=%s", args.jira_login)
        logging.info("jira_password=%s",
                     len(args.repo_password) * "*"
                     if args.repo_password else "None")
        logging.info("jira_project=%s", args.jira_project)

        if os.path.isdir(args.filename):
            args.filename = repo.package_folder(
                args.filename, args.release_version,
                extra_files=args.extra_files)

        # upload on repo
        if not args.package_only:
            artifact = repo.upload_release(
                args.filename,
                group=args.repo_group, repo_id=args.repo_id,
                url=args.repo_url,
                login=args.repo_login, password=args.repo_password,
                version=args.release_version)

            logging.info("Artifact is loaded: %s", artifact.url)
            text_result = "Artificat loaded: %s" % str(artifact.url)

        # jira
        jira_issue = None
        jira_url = None
        if args.jira and not args.package_only:
            jira_issue = gejira.create_issue(
                artifact, project=args.jira_project,
                url=args.jira_url,
                login=args.jira_login, password=args.jira_password)

            if jira_issue is not None:
                logging.info('jira created : %s', jira_issue.key)
                text_result += "jira : %s" % jira_issue.key
                (jira_url, unused_login, unused_password) = \
                    gejira.fill_jira_credential(
                        args.jira_url,
                        args.jira_login,
                        args.jira_password)
                webbrowser.open(os.path.join(jira_url, "browse",
                                             jira_issue.key))

        # slack
        if args.slack and not args.package_only:
            slack.slack_message(artifact, jira_issue, jira_url,
                                webhook_url=args.slack_url)

        # End message
        if 'args' in locals() and args.windows and not args.package_only:
            message_box(text=text_result, title='Artifact uploaded')

    except argparse.ArgumentError as errmsg:
        logging.error(str(errmsg))
        if 'args' in locals() and args.windows:
            message_box(text=parser.format_usage(), title='Usage')

    except SystemExit:
        logging.error("Exit")
        if 'args' in locals() and args.windows:
            message_box(text=parser.format_help(), title='Help')

    except BaseException as ex:
        logging.error(str(ex))
        if 'args' in locals() and args.windows:
            message_box(text=str(ex), title='Usage')

    logging.info('Finished')
    logging.info('<<--------------------------------------------------------')
    logging.info('+')


###############################################################################
# Call main if the script is main
###############################################################################
if __name__ == '__main__':
    __main()
