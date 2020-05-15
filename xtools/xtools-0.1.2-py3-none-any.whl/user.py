"""
Endpoints related to users.

https://xtools.readthedocs.io/en/stable/api/user.html
"""

from typing import Optional, Generator, Sequence
from datetime import date

from . import base


def simple_edit_count(project: str, username: str,
                      namespace: Optional[int] = None,
                      start: Optional[date] = None,
                      end: Optional[date] = None) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#simple-edit-count

    Example:

        >>> simple_edit_count("en.wikipedia.org", "Jimbo_Wales")
        {
          "project": "en.wikipedia.org",
          "username": "Jimbo_Wales",
          "namespace": "all",
          "user_id": 24,
          "deleted_edit_count": 424,
          "live_edit_count": 13751,
          ...,
          "elapsed_time": 80.916
        }

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :return:
    """

    path = base.build_path("/user/simple_editcount/{project}/{username}/{namespace}/{start}/{end}", (
        ("project", project, ""),
        ("username", username, ""),
        ("namespace", namespace, "0"),
        ("start", start, ""),
        ("end", end, ""),
    ))

    return base.get(path)


def number_of_pages_created(project: str, username: str,
                            namespace: Optional[str] = None,
                            redirects: Optional[str] = None,
                            deleted: Optional[str] = None,
                            start: Optional[date] = None,
                            end: Optional[date] = None) -> dict:
    """
    Return the number of pages created by a user along with some other info.

    Example:

        >>> number_of_pages_created("en.wikipedia", "Jimbo_Wales")
        {
          "project": "en.wikipedia.org",
          "username": "Jimbo_Wales",
          ...
          "counts": {
            "count": 42,
            "total_length": 30691,
            "avg_length": 730.7380952380952,
            "deleted": 1
          },
          "elapsed_time": 0.059,
        }

    https://xtools.readthedocs.io/en/stable/api/user.html#number-of-pages-created

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param redirects: either ``"noredirects"`` (default), ``"onlyredirects"``, or ``"all"`` for both.
    :param deleted: either ``"live"``, ``"deleted"``, or ``"all"`` (default).
    :param start:
    :param end:
    :return:
    """
    path = base.build_path("/user/pages_count/{project}/{username}/{namespace}/{redirects}/{deleted}/{start}/{end}", (
        ("project", project, ""),
        ("username", username, ""),
        ("namespace", namespace, "0"),
        ("redirects", redirects, "noredirects"),
        ("deleted", deleted, "all"),
        ("start", start, ""),
        ("end", end, ""),
    ))

    return base.get(path)


def _fix_page(page: dict) -> dict:
    """
    Fix a page dict as returned by the API.
    :param page:
    :return:
    """
    # Some (all?) pages with a number as their title have an int in this field.
    # E.g. https://fr.wikipedia.org/wiki/2040.
    if "page_title" in page:
        page["page_title"] = str(page["page_title"])
    return page


def pages_created(project: str, username: str,
                  namespace: str = None,
                  redirects: Optional[str] = None,
                  deleted: Optional[str] = None,
                  start: Optional[date] = None,
                  end: Optional[date] = None,
                  offset: Optional[int] = None,
                  all_times: bool = False) -> dict:
    """
    Return pages created by a user. This does not handle pagination; see ``pages_created_iter`` for that.

    Note that XTools doesn't support users with >400,000 edits, and this function raises
    a ``xtools.exceptions.TooManyEdits`` exception if you try.

    Example:

        >>> pages_created("enwiki", "Jimbo_Wales")
        {
          "pages": [
            {
              "namespace": 0,
              "type": "rev",
              "page_title": "Helen Crlenkovich",
              "page_is_redirect": 0,
              "length": 10691,
              "page_len": 11597,
              "rev_timestamp": 20200509210713,
              "rev_len": 10691,
              "rev_id": 170658958,
              "recreated": null,
              "pa_class": null,
              "pa_importance": null,
              "pa_page_revision": null,
              "raw_time": 20200509210713,
              "human_time": "2020-05-09 21:07",
              "badge": "https://upload.wikimedia.org/....svg",
            },
            ...
          ],
          "continue": 1,
        }

    https://xtools.readthedocs.io/en/stable/api/user.html#pages-created

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param redirects: either ``"noredirects"`` (default), ``"onlyredirects"``, or ``"all"`` for both.
    :param deleted: either ``"live"``, ``"deleted"``, or ``"all"`` (default).
    :param start:
    :param end:
    :param offset:
    :param all_times: if ``True``, fetch all pages instead of the more recent ones. This overrides ``start``
      and ``end``.
    :return:
    """
    if all_times:
        start = base.START_TIME
        end = base.END_TIME

    path = base.build_path(
        "/user/pages/{project}/{username}/{namespace}/{redirects}/{deleted}/{start}/{end}/{offset}",
        (
            ("project", project, ""),
            ("username", username, ""),
            ("namespace", namespace, "0"),
            ("redirects", redirects, "noredirects"),
            ("deleted", deleted, "all"),
            ("start", start, ""),
            ("end", end, ""),
            ("offset", offset, ""),
        ))

    ret = base.get(path)

    # Flatten the 'pages' key
    pages = ret["pages"]
    # single namespace: {"0": A, "1": B, ...}
    # all namespaces: {"0": [A, B], "1": [C, D, E], ...}
    keys = sorted(pages.keys(), key=int)

    is_namespaced = False
    try:
        is_namespaced = isinstance(next(pages.values().__iter__()), list)
    except StopIteration:
        pass

    if is_namespaced:
        ret["pages"] = [_fix_page(page) for k in keys for page in pages[k]]
    else:
        ret["pages"] = [_fix_page(pages[k]) for k in keys]

    return ret


def pages_created_iter(project: str, username: str,
                       namespace: str = None,
                       redirects: Optional[str] = None,
                       deleted: Optional[str] = None,
                       start: Optional[date] = None,
                       end: Optional[date] = None,
                       all_times: bool = False) -> Generator[dict, None, None]:
    """
    Equivalent of ``pages_created`` that yields page dicts and does the pagination for you.

    See ``pages_created`` for sample return values.

    Example:

        >>> for page in pages_created_iter("enwiki", "Jimbo_Wales"):
        ...     print(page["page_title"])

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param redirects: either ``"noredirects"`` (default), ``"onlyredirects"``, or ``"all"`` for both.
    :param deleted: either ``"live"``, ``"deleted"``, or ``"all"`` (default).
    :param start:
    :param end:
    :param all_times: if ``True``, fetch all pages instead of the more recent ones. This overrides ``start``
      and ``end``.
    :return:
    """
    offset = 0

    while offset is not None:
        ret = pages_created(project, username,
                            namespace=namespace, redirects=redirects, deleted=deleted,
                            start=start, end=end, all_times=all_times, offset=offset)
        offset = ret.get("continue")
        for page in ret["pages"]:
            yield page


def automated_edit_counter(project: str, username: str,
                           namespace: Optional[str] = None,
                           start: Optional[date] = None,
                           end: Optional[date] = None,
                           offset: Optional[int] = None,
                           tools: bool = False) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#automated-edit-counter

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :param offset:
    :param tools:
    :return:
    """
    path = base.build_path(
        "/user/automated_editcount/{project}/{username}/{namespace}/{start}/{end}/{offset}/{tools}",
        (
            ("project", project, ""),
            ("username", username, ""),
            ("namespace", namespace, "0"),
            ("start", start, ""),
            ("end", end, ""),
            ("offset", offset, ""),
            ("tools", "true" if tools else "", ""),
        ))
    return base.get(path)


def _edits(what: str, project: str, username: str, namespace: str = "0",
           start: Optional[date] = None,
           end: Optional[date] = None,
           offset: Optional[int] = None) -> dict:
    """
    Base function for both ``non_automated_edits`` and ``automated_edits``.

    :param what:
    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :param offset:
    :return:
    """
    path = base.build_path("/user/{what}/{project}/{username}/{namespace}/{start}/{end}/{offset}", (
        ("what", what, ""),
        ("project", project, ""),
        ("username", username, ""),
        ("namespace", namespace, "0"),
        ("start", start, ""),
        ("end", end, ""),
        ("offset", offset, ""),
    ))
    return base.get(path)


def non_automated_edits(project: str, username: str,
                        namespace: Optional[str] = None,
                        start: Optional[date] = None,
                        end: Optional[date] = None,
                        offset: Optional[int] = None) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#non-automated-edits

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :param offset:
    :return:
    """
    return _edits("nonautomated_edits", project, username,
                  namespace=namespace, start=start, end=end, offset=offset)


def automated_edits(project: str, username: str,
                    namespace: Optional[str] = None,
                    start: Optional[date] = None,
                    end: Optional[date] = None,
                    offset: Optional[int] = None) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#automated-edits

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :param offset:
    :return:
    """
    return _edits("automated_edits", project, username,
                  namespace=namespace, start=start, end=end, offset=offset)


def edit_summaries(project: str, username: str,
                   namespace: Optional[str] = None,
                   start: Optional[date] = None,
                   end: Optional[date] = None) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#edit-summaries

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param start:
    :param end:
    :return:
    """
    path = base.build_path("/user/edit_summaries/{project}/{username}/{namespace}/{start}/{end}", (
        ("project", project, ""),
        ("username", username, ""),
        ("namespace", namespace, "0"),
        ("start", start, ""),
        ("end", end, ""),
    ))
    return base.get(path)


def top_edits(project: str, username: str,
              namespace: Optional[str] = None,
              page_title: Optional[str] = None) -> dict:
    """
    Return the top-edited pages by a user, or all edits made by a user to a specific page.

    https://xtools.readthedocs.io/en/stable/api/user.html#top-edits

    :param project:
    :param username:
    :param namespace: one namespace (default is ``"0"``, the main one) or ``"all"`` for all of them.
    :param page_title: page title. For non-main pages you must either fill the ``namespace`` parameter or set it
      to a blank string and use the namespace-prefixed article title.
    :return:
    """
    path = base.build_path("/user/top_edits/{project}/{username}/{namespace}/{article}", (
        ("project", project, ""),
        ("username", username, ""),
        ("namespace", namespace, "0"),
        ("article", page_title, ""),
    ))
    return base.get(path)


def category_edit_counter(project: str, username: str, categories: Sequence[str],
                          start: Optional[date] = None,
                          end: Optional[date] = None) -> dict:
    """
    https://xtools.readthedocs.io/en/stable/api/user.html#category-edit-counter

    :param project:
    :param username:
    :param categories: Categories. The namespace prefix can be omitted.
    :param start:
    :param end:
    :return:
    """
    path = base.build_path("/user/category_editcount/{project}/{username}/{categories}/{start}/{end}", (
        ("project", project, ""),
        ("username", username, ""),
        ("categories", "|".join(categories), ""),
        ("start", start, ""),
        ("end", end, ""),
    ))
    return base.get(path)


def log_counts(project: str, username: str) -> dict:
    """
    Return counts of logged actions made by a user.

    https://xtools.readthedocs.io/en/stable/api/user.html#log-counts

    Example:

        >>> log_counts("en.wikipedia.org", "Jimbo_Wales")
        {
          "project": "en.wikipedia.org",
          "username": "Jimbo_Wales",
          "log_counts": {
            "block-block": 83,
            "block-unblock": 42,
            "create-create": 2,
            "delete-delete": 325,
            "delete-delete_redir": 1,
            "delete-event": 1,
            "delete-restore": 20,
            ...
          },
        }

    :param project:
    :param username:
    :return:
    """
    return base.get("/user/log_counts/%s/%s" % (project, username))


def namespace_totals(project: str, username: str) -> dict:
    """
    Return the edit count for each namespace with at least 1 edit.

    https://xtools.readthedocs.io/en/stable/api/user.html#namespace-totals

    :param project:
    :param username:
    :return:
    """
    return base.get("/user/namespace_totals/%s/%s" % (project, username))


def month_counts(project: str, username: str) -> dict:
    """
    Return the edit count of a user, grouped by namespace then year and month.

    https://xtools.readthedocs.io/en/stable/api/user.html#month-counts

    :param project:
    :param username:
    :return:
    """
    return base.get("/user/month_counts/%s/%s" % (project, username))


def time_card(project: str, username: str) -> dict:
    """
    Return the relative distribution of edits made by a user based on hour of the day and day of the week.

    Example:

        >>> time_card("en.wikipedia.org", "Jimbo_Wales")
        {
          "project": "en.wikipedia.org",
          "username": "Jimbo_Wales",
          "timecard": [
            {
              "day_of_week": 1,
              "hour": 0,
              "value": 83,
              "scale": 9
            },
            ...
          ],
        }

    https://xtools.readthedocs.io/en/stable/api/user.html#time-card

    :param project:
    :param username:
    :return:
    """
    return base.get("/user/timecard/%s/%s" % (project, username))