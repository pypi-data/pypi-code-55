#!/usr/bin/env python3

"""\
Submit new projects and samples
"""
import os
import sys

from .htmlparser import cleanhtml
from . import sql
from .query import db_connect


def data_sql(project: bool = False,):
    """\

    :param project
        Switch to project parser

    :return:
        `SCRIdb.sql` object
    """
    if project:
        return sql.projectdata_sql
    else:
        return sql.sampledata_sql


def data_submission_main(fn: str, mode: list, proj: bool = False,) -> None:
    """\
    A method that reads HTML data and submits new records into the database.

    :param fn:
        Input path to HTML, or HTML string
    :param mode:
        Action mode to submit new data and/or submit library preparation parameters.
        Choices are: submitnew, or stats, or both.
    :param proj:
        Project submission

    :return:
        `None`

    Example
    -------

    >>> from SCRIdb.submission import *
    >>> fn = "<p>Some<b>bad<i>HTML"
    >>> data_submission_main(fn=fn, mode=['submitnew'])

    """
    if os.path.isfile(fn):
        if os.path.splitext(fn)[1] != ".html":
            sys.exit("ERROR: Input file not `HTML` format!")
        with open(fn, "r") as f:
            html = f.read()
    else:
        html = fn

    cleanhtml(html)

    # Determine if `project intake form`
    if "Begin a new project" in html:
        proj = True
        cleanhtml.id = 5
        print("Switching to `Project Intake Form` mode!")

    # make sure sample submission forms are not treated as project intake forms
    if proj and "Begin a new project" not in html:
        sys.exit("Error: missing `--project`")

    cleanhtml.get_general_attrs(
        [
            "Additional sample information",
            "Upload samples from Excel?",
            "Sample parameters",
            "Hash tag antibodies",
            "Hash tag barcodes used",
        ]
    )
    # skip this step if parsing project intake forms
    if not proj:
        cleanhtml.get_tables()
    cleanhtml.kargs = sql.sqlargs(cleanhtml.kargs)

    if "submitnew" in mode:
        print("Submitting new data to the database ...")
        func_sql = data_sql(proj)
        func_sql(cleanhtml.kargs)

    if "stats" in mode:
        print("Updating data on `stats_data` table ...")
        sql.statsdata_sql(cleanhtml.kargs)

    db_connect.db.disconnect()

    return None
