"""
Endpoints related to pages.

https://xtools.readthedocs.io/en/stable/api/page.html
"""

from typing import Optional, Sequence
from datetime import date

from . import base


def _get_page_dict(what: str, project: str, article: str) -> dict:
    return base.get("/page/%s/%s/%s" % (what, project, article))


def article_info(project: str, article: str) -> dict:
    """
    Return basic information about an article, such as page views, watchers, edits counts; author; assessment.

    https://xtools.readthedocs.io/en/stable/api/page.html#article-info

    :param project:
    :param article:
    :return:
    """
    return _get_page_dict("articleinfo", project, article)


def prose(project: str, article: str) -> dict:
    """
    Return prose information about an article, such as references and words counts.

    https://xtools.readthedocs.io/en/stable/api/page.html#prose

    Example:

        >>> prose("en.wikipedia.org", "Albert_Einstein")
        {
            "project": "en.wikipedia.org",
            "page": "Albert_Einstein",
            "characters": 66690,
            "words": 10536,
            "references": 308,
            "unique_references": 251,
            "sections": 63,
            "elapsed_time": 0.645,
        }

    :param project:
    :param article:
    :return:
    """
    return _get_page_dict("prose", project, article)


def links(project: str, article: str) -> dict:
    """
    Return in and outgoing links counts of an article.

    Example:

        >>> links("enwiki", "Albert_Einstein")
        {
          "project": "en.wikipedia.org",
          "page": "Albert_Einstein",
          "links_ext_count": 372,
          "links_out_count": 1178,
          "links_in_count": 9744,
          "redirects_count": 19,
          "elapsed_time": 17.902
        }

    https://xtools.readthedocs.io/en/stable/api/page.html#links

    :param project:
    :param article:
    :return:
    """
    return _get_page_dict("links", project, article)


def top_editors(project: str, article: str,
                start: Optional[date] = None,
                end: Optional[date] = None,
                limit: Optional[int] = None,
                exclude_bots: bool = False) -> dict:
    """
    Get top editors on an article.

    Note: as of 2020/05/10, passing a limit without start and end gives an error.

    Example:

        >>> top_editors("en.wikipedia", "Albert_Einstein")
        {
          "project": "en.wikipedia.org",
          "page": "Albert_Einstein",
          "limit": 20,
          "top_editors": [
            {
              "rank": 1,
              "username": "Otterpops",
              "count": 509,
              "minor": 46,
              "first_edit": {"id": 111357663, "timestamp": 20070227165531},
              "latest_edit": {"id": 115188249, "timestamp": 20070314232325},
            },
            ...
          ],
          "elapsed_time": 0.133,
        }

    https://xtools.readthedocs.io/en/stable/api/page.html#top-editors

    :param project:
    :param article:
    :param start: optional start date.
    :param end: optional end date.
    :param limit: optional limit (XTools' default is 20)
    :param exclude_bots: if True, exclude bots.
    :return:
    """
    path = base.build_path("/page/top_editors/{project}/{article}/{start}/{end}/{limit}", (
        ("project", project, ""),
        ("article", article, ""),
        ("start", start, ""),
        ("end", end, ""),
        ("limit", limit, ""),
    ))
    params = {}
    if exclude_bots:
        params["nobots"] = "1"

    return base.get(path, params)


def assessments(project: str, articles: Sequence[str],
                class_only: bool = False) -> dict:
    """
    Get assessment data for the given articles.

    Example:

        >>> assessments("en.wikipedia.org", ["Albert_Einstein", "Bob_Dylan"], class_only=True)
        {
          "project": "en.wikipedia.org",
          "Albert Einstein": {
            "value": "GA",
            "color": "#66FF66",
            "category": "Category:GA-Class articles",
            "badge": "https://upload.wikimedia.org/wikipedia/commons/9/94/Symbol_support_vote.svg"
          },
          "Bob Dylan": {
            "value": "FA",
            "color": "#9CBDFF",
            "category": "Category:FA-Class articles",
            "badge": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Featured_article_star.svg"
          },
          "elapsed_time": 0.361
        }

    https://xtools.readthedocs.io/en/stable/api/page.html#assessments

    :param project:
    :param articles:
    :param class_only:
    :return:
    """
    params = {}
    if class_only:
        params["classonly"] = "1"

    return base.get("/page/assessments/%s/%s" % (project, "|".join(articles)), params)