#!/usr/bin/env python3

from setuptools import setup, find_packages
import os
import git

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version():
    """
    Read git tag and version given by environment variable and convert it to a version number.
    Git describe gives something like
        v1.0.0-158-g6c5be28
    From the git describe help:
        The command finds the most recent tag that is reachable from a commit.
        If the tag points to the commit, then only the tag is shown. Otherwise,
        it suffixes the tag name with the number of additional commits on top
        of the tagged object and the abbreviated object name of the most recent
        commit.
    We will keep the first two number and replace the last with the number of commits since the tag:
        v1.0.0-158-g6c5be28 -> v1.0.158
    :return:
    """
    if 'FLATPAK_INSTALL' in os.environ:
        f = open('version.txt','r')
        git_describe = f.readline()
        f.close()        
    else: 
        try:
            r = git.repo.Repo(here)
            git_describe = r.git.describe()
            f = open('version.txt','w')
            f.write(git_describe)
            f.close()
            # and do it one more for packaging if possible
            # f = open('src/rwth-nb/version.txt','w')
            # f.write(git_describe)
            # f.close()
        except (git.InvalidGitRepositoryError):
            f = open('version.txt','r')
            git_describe = f.readline()
            f.close()

    version = None
    split_describe = git_describe.split('-')
    if len(split_describe) == 1:
        if '.' not in git_describe:
            raise Exception("Tag does not comply to the versioning spec. It should be something like v1.0.0, but is %s"
                            % git_describe)
        version = git_describe
    elif len(split_describe) == 3:
        tag = split_describe[0]
        commits_since_tag = split_describe[1]

        # replace last digit with commits_since_tag
        split_tag = tag.split('.')
        if len(split_tag) == 1:
            raise Exception("Tag does not comply to the versioning spec. It should be something like v1.0.0, but is %s"
                            % tag)
        split_tag[-1] = commits_since_tag
        version = '.'.join(split_tag)

    else:
        raise Exception("Can not handle this type of git describe, there should be either no or two '-'. %s"
                        % git_describe)

    return version


setup(name='rwth_nb',
      # Versions should comply with PEP440.  For a discussion on single-sourcing
      # the version across setup.py and the project code, see
      # https://packaging.python.org/en/latest/single_source_version.html
      version=get_version(),
      description='RWTH Python Library for Jupyter Notebooks',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.rwth-aachen.de/jupyter/rwth-nb',
      author='Christian Rohlfing, Lars Thieling, Christoph Weyer, Jens Schneider, Steffen Vogel',
      author_email='rohlfing@ient.rwth-aachen.de',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[], # todo
      zip_safe=False)
