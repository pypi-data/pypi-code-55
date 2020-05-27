#!/usr/bin/env python3

"""\
html parser for sample forms and project initiation forms
"""

import re
import sys

import regex

import pandas as pd
from bs4 import BeautifulSoup
from dateutil.parser import parse
from lxml.html.clean import Cleaner


class ParseHtml:
    """\
    HTML parser that returns clean parameters and data extracted from *iLabs*
    submitted forms.

    :type html: str
    :type kill_tags: list

    :param html:
        Input HTML
    :param kill_tags:
        HTML tags to be cleaned and removed

    :rtype: str
    :return:
        Cleaned html string

    Example
    -------

    >>> from SCRIdb.htmlparser import cleanhtml
    >>> cleanhtml("<p>Some<b>bad<i>HTML")

    """

    def __init__(self, func):
        self.func = func
        self.kargs = {}
        self.tables = {}
        self.soup = str
        self.id = 1

    def __call__(self, *args):

        new_html = self.func(*args)
        self.soup = BeautifulSoup(new_html, "html.parser")
        tags = self.soup.find_all("table")
        n = 0
        for tag in tags:
            tag["id"] = n
            self.tables[n] = str(tag)
            n += 1

    def reset(self):
        self.__init__(self.func)

    def get_general_attrs(self, option_set: list = None):

        self.soup.a.decompose()
        request_id = self.soup.h2.string.strip().split()[0]
        date_created = self.soup.find(text=regex.compile("Created")).strip()
        date_created = re.sub("Created:", "", date_created)
        date_created = parse(date_created).strftime("%Y-%m-%d")
        if "Lab Name:" in self.soup.text:
            labName = re.findall(
                r"(?<=Lab Name:)(.*?)(?=Lab PI)", self.soup.text, re.DOTALL
            )
            labName = labName[0].strip()
            self.kargs["labName"] = labName
        if "Customer institute:" in self.soup.text:
            institute = re.findall(
                r"(?<=Customer institute:)(.*?)(?=URL:)", self.soup.text, re.DOTALL
            )
            institute = institute[0].strip()
            self.kargs["institute"] = institute
            labinfo = re.findall(
                r"(?<=Lab PI\(s\):)(.*?)(?=Customer institute:)",
                self.soup.text,
                re.DOTALL,
            )
            PI_name = labinfo[0].strip().split(":")[0]
            PI_email = [i for i in labinfo[0].strip().split() if "@" in i][0]
            phone = labinfo[0].strip().split(":")[-1]
            self.kargs["PI_name"] = PI_name if PI_name else "NULL"
            self.kargs["PI_email"] = PI_email if PI_email else "NULL"
            self.kargs["Phone"] = phone if phone else "NULL"
        self.kargs["request_id"] = request_id
        self.kargs["date_created"] = date_created

        g = self.soup("table", id=self.id)[0]
        # count how many tables within main table
        idx = len(g.find_all("table"))
        # get rid of all inner tables and their contents
        for i in range(idx):
            g.table.decompose()
        try:
            g.b.decompose()
        except AttributeError:
            pass
        for i in g("a"):
            try:
                i.parent.decompose()
            except AttributeError:
                pass
        # get rid of none checked radio buttons and checkboxes
        for i in g.find_all("input", attrs={"checked": False}):
            try:
                i.parent.decompose()
            except AttributeError:
                pass

        for i in g.find_all(text=regex.compile(r"\L<options>", options=option_set)):
            try:
                i.parent.decompose()
            except AttributeError:
                pass
        # read clean main table
        g = pd.read_html(str(g))[0]
        g = g.drop(0, axis=1)
        g = g.set_index(1)
        g = g.loc[g.index.dropna()]
        g = g.to_dict()[2]
        return self.kargs.update(g)

    def get_tables(self, index: str = "Sample Name"):
        # get the index and test for discrepancy between tables
        hashtag_table_id = None
        converters = {
            "Hash tag barcode (4 digit)": str,
            "Hash Tag Sequence": str,
            "Barcode": str,
            "Label": str,
        }
        len_tables = [2, 3]
        if self.kargs['Cell "Hashing"?'].lower() == "yes":
            hashtag_table_id = 3
            len_tables = [4, 5]
        t = pd.read_html(
            self.tables[len_tables[0]], index_col=0, converters=converters
        )[0]
        # Important: get rid of spaces in sample name, since sample name is used to
        # construct prefix for seqc outputs
        t[index] = t[index].replace(to_replace=r" ", value="_", regex=True)
        t = t.set_index(index)
        idx = t.index

        for i in len_tables:
            t = pd.read_html(self.tables[i], index_col=0, converters=converters)[0]
            t[index] = t[index].replace(to_replace=r" ", value="_", regex=True)
            try:
                t = t.set_index(index)
                assert not bool(
                    t.index.difference(idx).values.any()
                ), "sample names don't match in tables"
                idx = t.index
            except (KeyError, AssertionError) as e:
                print("ERROR: index = ", index)
                print(pd.DataFrame({i: pd.Series(t.index), i + 1: pd.Series(idx)}))
                print(str(e))
                sys.exit("ERROR:\n" + str(e))

            t = t.dropna(how="all")
            t = t.to_dict(orient="i")
            for sample in t.keys():
                if "samples" not in self.kargs:
                    self.kargs["samples"] = {}
                if sample not in self.kargs["samples"]:
                    self.kargs["samples"][sample] = t[sample]
                else:
                    self.kargs["samples"][sample].update(t[sample])

        # for hashtag tables, attach hashtags to samples
        if hashtag_table_id:

            # read hashtags table
            t1 = pd.read_html(
                self.tables[hashtag_table_id], index_col=0, converters=converters
            )[0]
            t1 = t1.dropna(how="all")

            # read hashtag parameters
            if self.kargs["Hashtag Parameters"] == "yes":
                t2 = pd.read_html(self.tables[6], index_col=0)[0]
                t2[index] = t2[index].replace(to_replace=r" ", value="_", regex=True)
                t2 = t2.dropna(how="all")
                t2 = t2.to_dict(orient="i")

            if (
                t1["Sample Name (Optional)"].dropna().empty
            ):  # and len(self.kargs["samples"].keys()) == 1:
                t1 = t1.T.iloc[[0, 1, 2, 4]]
                t1.index = ["hlabels", "hashtags", "barcodes", "hashtag_notes"]
                t1 = t1.to_dict(orient="i")
                for sample in self.kargs["samples"]:
                    self.kargs["samples"][sample]["hastag_parameters"] = t1

            else:
                t1.columns = [
                    "hlabels",
                    "hashtags",
                    "barcodes",
                    "sample_name",
                    "hashtag_notes",
                ]
                t1 = t1.to_dict()
                for sample in self.kargs["samples"]:
                    hashtags = {
                        "hashtags": {
                            i: t1["hashtags"][i]
                            for i in [
                                k for k, v in t1["sample_name"].items() if v == sample
                            ]
                        }
                    }
                    barcodes = {
                        "barcodes": {
                            i: t1["barcodes"][i]
                            for i in [
                                k for k, v in t1["sample_name"].items() if v == sample
                            ]
                        }
                    }
                    hlabels = {
                        "hlabels": {
                            i: t1["hlabels"][i]
                            for i in [
                                k for k, v in t1["sample_name"].items() if v == sample
                            ]
                        }
                    }
                    hashtag_notes = {
                        "hashtag_notes": {
                            i: t1["hashtag_notes"][i]
                            for i in [
                                k for k, v in t1["sample_name"].items() if v == sample
                            ]
                        }
                    }

                    hastag_parameters = {}
                    [
                        hastag_parameters.update(i)
                        for i in [hashtags, barcodes, hlabels, hashtag_notes]
                    ]
                    self.kargs["samples"][sample][
                        "hastag_parameters"
                    ] = hastag_parameters

            if t2:
                for v in t2.values():
                    sample = v["Sample Name"]
                    v.pop("Sample Name")
                    self.kargs["samples"][sample]["hastag_parameters"].update(v)

        if (
            self.kargs["Platform"] == "Single-cell immune profiling"
            and self.kargs["TCR Parameters"].lower() == "yes"
        ):
            t = pd.read_html(
                self.tables[len(self.tables) - 1], index_col=0, converters=converters
            )[0]
            t = t.dropna(how="all")
            t = t.to_dict(orient="i")
            for v in t.values():
                sample = v["Sample Name"]
                v.pop("Sample Name")
                self.kargs["samples"][sample]["TCR_parameters"] = v


@ParseHtml
def cleanhtml(html: str = "", kill_tags: list = ["span"]) -> str:
    """\
    HTML parser that returns clean parameters and data extracted from *iLabs*
    submitted forms.

    :param html:
        Input HTML
    :param kill_tags:
        HTML tags to be cleaned and removed

    :return:
        Cleaned html string

    """
    cleaner = Cleaner(
        style=True,
        links=True,
        add_nofollow=True,
        javascript=True,
        meta=True,
        page_structure=True,
        kill_tags=kill_tags,
        processing_instructions=True,
        embedded=True,
        frames=True,
        forms=False,
    )
    new_html = cleaner.clean_html(html)

    return new_html
