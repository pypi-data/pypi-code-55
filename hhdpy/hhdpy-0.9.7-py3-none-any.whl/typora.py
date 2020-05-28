# -*- coding: utf-8 -*-

import os
import datetime

USAGE = """
hhdpy typora_new_file "실험결과 최종보고서"
hhdpy typora_github_io_article_step1 "200101 실험결과 최종보고서.md"
hhdpy typora_github_io_article_step2 "2020-01-01-실험결과-최종보고서.md" 
"""

def new_file(title):

    print("__file__[{}]".format(__file__))
    print("os.getcwd()[{}]".format(os.getcwd()))

    # yymmdd = datetime.datetime.now().strftime("%y%m%d")
    # mdFileName = "{} {}.md".format(yymmdd, title)
    # mdFile = open("c:\\temp\\temp.md", "w", encoding="utf-8", newline="")
    # mdFile.write("# {} {}\n".format(yymmdd, title))
    # mdFile.close()
