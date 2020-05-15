"""
Endpoints related to projects.

https://xtools.readthedocs.io/en/stable/api/project.html
"""

from typing import Optional, Sequence
from datetime import date

from . import base


def _get_project_dict(what: str, project: str) -> dict:
    return base.get("/project/%s/%s" % (what, project))


def normalize_project(project: str) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/project.html#normalize-project

    Example:

        >>> normalize_project("enwiki")
        {
          "project": "en.wikipedia.org",
          "domain": "en.wikipedia.org",
          "url": "https://en.wikipedia.org/",
          "api": "https://en.wikipedia.org/w/api.php",
          "database": "enwiki",
          "elapsed_time": 0.051
        }

    :param project:
    :return:
    """
    return _get_project_dict("normalize", project)


def namespaces(project: str) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/project.html#namespaces

    :param project:
    :return:
    """
    return _get_project_dict("namespaces", project)


def page_assessments(project: str) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/project.html#page-assessments

    :param project:
    :return:
    """
    return _get_project_dict("assessments", project)


def page_assessments_configuration() -> dict:
    """
    Return the list of wikis that support page assessments and the configuration for each.

    https://xtools.readthedocs.io/en/stable/api/project.html#page-assessments-configuration

    Example:

        >>> page_assessments_configuration()
        {
          "projects": [
            "ar.wikipedia.org",
            "en.wikipedia.org",
            "en.wikivoyage.org",
            ...
          ],
          "config": {
            "ar.wikipedia.org": { ... },
            ...
          },
        }

    :return:
    """
    return base.get("/project/assessments")


def automated_tools(project: str) -> dict:
    """
    Return a list of known (semi-)automated tools used on the project.

    Example:

        >>> automated_tools("en.wikipedia.org")
        {
          "project": "en.wikipedia.org",
          "Admin actions": {
            "regex": "^...",
            "link": "Project:Administrators",
            "label": "Admin actions",
            "namespaces": [],
            "tags": [],
          },
          "Advisor.js": {
            "regex": "...Advisor.js",
            ...
          },
          ...
        }

    Note the exact same endpoint exists under ``api/user``.

    https://xtools.readthedocs.io/en/stable/api/project.html#automated-tools
    https://xtools.readthedocs.io/en/stable/api/user.html#automated-tools

    :param project:
    :return:
    """
    return _get_project_dict("automated_tools", project)


def admins_and_user_groups(project: str) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/project.html#admins-and-user-groups

    :param project:
    :return:
    """
    return _get_project_dict("admins_groups", project)


def _get_project_stats_dict(what: str, project: str,
                            start: Optional[date] = None,
                            end: Optional[date] = None,
                            actions: Optional[Sequence[str]] = None) -> dict:
    path = base.build_path("/project/{what}/{project}/{start}/{end}", (
        ("what", what, ""),
        ("project", project, ""),
        ("start", start, ""),
        ("end", end, ""),
    ))

    params = {}
    if actions:
        params["actions"] = "|".join(actions)

    return base.get(path, params)


def admin_statistics(project: str,
                     start: Optional[date] = None,
                     end: Optional[date] = None,
                     actions: Optional[Sequence[str]] = None) -> dict:
    """
    Return admin users of the project with counts of the actions they took.

    XTools limits the time period to one month.

    https://xtools.readthedocs.io/en/stable/api/project.html#admin-statistics

    :param project:
    :param start:
    :param end:
    :param actions: available actions include: ``delete``, ``revision-delete``, ``log-delete``, ``restore``,
      ``re-block``, ``unblock``, ``re-protect``, ``unprotect``, ``rights``, ``merge``, ``import``.
    :return:
    """
    return _get_project_stats_dict("admin_stats", project, start, end, actions)


def patroller_statistics(project: str,
                         start: Optional[date] = None,
                         end: Optional[date] = None,
                         actions: Optional[Sequence[str]] = None) -> dict:
    """
    Same as ``admin_statistics`` with different actions.

    https://xtools.readthedocs.io/en/stable/api/project.html#patroller-statistics

    :param project: 
    :param start: 
    :param end: 
    :param actions: available actions include: ``patrol``, ``page-curation``, ``pc-accept``, ``pc-reject``.
    :return: 
    """
    return _get_project_stats_dict("patroller_stats", project, start, end, actions)


def steward_statistics(project: str,
                       start: Optional[date] = None,
                       end: Optional[date] = None,
                       actions: Optional[Sequence[str]] = None) -> dict:
    """
    Same as ``admin_statistics`` with different actions.

    https://xtools.readthedocs.io/en/stable/api/project.html#stewards-statistics

    :param project:
    :param start:
    :param end:
    :param actions: available actions include: ``global-account-un-lock`` (global locks and unlocks), ``global-block``,
      ``global-unblock``, ``global-rename``, ``global-rights``, ``wiki-set-change``.
    :return:
    """
    return _get_project_stats_dict("steward_stats", project, start, end, actions)