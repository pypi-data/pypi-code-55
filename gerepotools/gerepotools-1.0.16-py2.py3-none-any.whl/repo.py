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
import tarfile
import repositorytools
import yaml
import glob
import upref

from . import core

# -----------------------------------------------------------------------------
def fill_repo_credential(url=None, login=None, password=None,
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
                                 "templates", "repotools-repo-credential.yml")

    conf_filename = core.check_is_file_and_correct_path(conf_filename)

    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        data_desc = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if url is not None:
        data_desc['url']['value'] = url
    if login is not None:
        data_desc['login']['value'] = login
    if password is not None:
        data_desc['password']['value'] = password

    data = upref.get_pref(data_desc, 'repotools-repo-credential',
                          force_renew=force_renew)

    return (data['url'], data['login'], data['password'])


# -----------------------------------------------------------------------------
def fill_repo_target(group=None, repo_id=None,
                     force_renew=False):
    """ Fill the target usage of the repo.

    @param group the group of the target
    @param repo_id Id of the repo

    @return (group, repo_id)
    """

    if group is not None and repo_id is not None:
        return (group, repo_id)

    conf_filename = os.path.join(__get_this_folder(),
                                 "templates", "repotools-repo-target-last.yml")

    conf_filename = core.check_is_file_and_correct_path(conf_filename)

    with codecs.open(conf_filename, "r", "utf-8") as ymlfile:
        data_desc = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if group is not None:
        data_desc['group']['value'] = group
    if repo_id is not None:
        data_desc['repo_id']['value'] = repo_id

    data = upref.get_pref(data_desc, 'repotools-repo-target-last',
                          force_renew=force_renew)

    return (data['group'], data['repo_id'])

# -----------------------------------------------------------------------------
def package_folder(folder, version, package_name=None, extra_files=None):

    folder = core.check_folder(folder)

    logging.info("Create the archive folder %s ", folder)
    if not os.path.isdir(folder):
        raise BaseException("The folder %s does not exists" % folder)

    if package_name is None:
        if os.path.basename(folder) == '':
            folder = os.path.dirname(folder)
        package_name = os.path.basename(folder)

    output_folder = os.path.join(os.path.dirname(folder), package_name)

    if version is None or version in package_name:
        output_filename = output_folder + ".tar.gz"
    else:
        output_filename = output_folder + "-" + version + ".tar.gz"

    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(folder, arcname=package_name)
        if extra_files is not None and isinstance(extra_files, list):
            for file_idx in extra_files:
                filename = os.path.join(folder, file_idx)
                for filename in glob.glob(filename):
                    filename = core.check_is_file_and_correct_path(filename)
                    tar.add(filename, arcname=os.path.split(filename)[1])

    return output_filename


# -----------------------------------------------------------------------------
def upload_release(filename, group=None, repo_id=None, url=None,
                   login=None, password=None, extension=None, version=None):

    logging.info("Start upload the file %s", filename)
    if os.path.isdir(filename):
        filename = package_folder(filename, version)
    elif not os.path.isfile(filename):
        raise BaseException("%s is not a file or a folder" % filename)

    filename = core.check_is_file_and_correct_path(filename)
    if filename.endswith('.tar.gz'):
        extension = 'tar.gz'

    (url, login, password) = fill_repo_credential(url, login, password)
    (group, repo_id) = fill_repo_target(group, repo_id, force_renew=True)

    logging.info("Start RepoId=%s ; Group=%s", repo_id, group)

    client = repositorytools.repository_client_factory(
        repository_url=url, user=login, password=password)
    artifact = repositorytools.LocalArtifact(
        local_path=filename, group=group, version=version, extension=extension)

    remote_artifacts = client.upload_artifacts(
        local_artifacts=[artifact], repo_id=repo_id)

    logging.info("End upload the file %s", filename)

    return remote_artifacts[0]


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
