# -*- coding: utf-8 -*-

USAGE = """
hhdpy typora_new_file "실험결과 최종보고서"
hhdpy typora_github_io_article_step1 "200101 실험결과 최종보고서.md"
hhdpy typora_github_io_article_step2 "2020-01-01-실험결과-최종보고서.md" 
"""

def new_file(title):
    print("new_file title[{}]".format(title))
