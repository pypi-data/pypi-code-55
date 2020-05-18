"""Cookiecutter repository functions."""

import os
import re

from libvis_mods.exceptions import RepositoryNotFound
from libvis_mods.download.vcs import clone
from libvis_mods.config_gen import BUILTIN_ABBREVIATIONS

REPO_REGEX = re.compile(
    r"""
# something like git:// ssh:// file:// etc.
((((git|hg)\+)?(git|ssh|file|https?):(//)?)
 |                                      # or
 (\w+@[\w\.]+)                          # something like user@...
)
""",
    re.VERBOSE,
)


def is_repo_url(value):
    """Return True if value is a repository URL."""
    return bool(REPO_REGEX.match(value))


def is_zip_file(value):
    """Return True if value is a zip file."""
    return value.lower().endswith(".zip")


def expand_abbreviations(template, abbreviations):
    """Expand abbreviations in a template name.
    :param template: The project template name.
    :param abbreviations: Abbreviation definitions.
    """
    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(":")
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template



def determine_repo_dir(
    template,
    clone_to_dir,
    abbreviations=BUILTIN_ABBREVIATIONS,
    checkout=None,
    no_input=True,
    password=None,
    directory=None,
):
    """
    Locate the repository directory from a template reference.
    Applies repository abbreviations to the template reference.
    If the template refers to a repository URL, clone it.
    If the template is a path to a local repository, use it.
    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param abbreviations: A dictionary of repository abbreviation
        definitions.
    :param clone_to_dir: The directory to clone the repository into.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param password: The password to use when extracting the repository.
    :param directory: Directory within repo where cookiecutter.json lives.
    :return: A tuple containing the cookiecutter template directory, and
        a boolean descriving whether that directory should be cleaned up
        after the template has been instantiated.
    :raises: `RepositoryNotFound` if a repository directory could not be found.
    """
    template = expand_abbreviations(template, abbreviations)

    if is_repo_url(template):
        cloned_repo = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=clone_to_dir,
            no_input=no_input,
        )
        repository_candidates = [cloned_repo]
    else:
        repository_candidates = [
            template,
            os.path.join(clone_to_dir, template),
        ]

    if directory:
        repository_candidates = [
            os.path.join(s, directory) for s in repository_candidates
        ]

    for repo_candidate in repository_candidates:
        return repo_candidate

    raise RepositoryNotFound(
        'A valid repository for "{}" could not be found in the following '
        "locations:\n{}".format(template, "\n".join(repository_candidates))
    )
