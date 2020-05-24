# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : cjbcn.py
# @Software: PyCharm

# 1.生物工程学报

import sys

import re
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "http://journals.im.ac.cn/cjbcn/ch/reader/issue_list.aspx",
        }

Parent = parent.Parent()

class Cjbcn(object):

    def __init__(self):
        self.journal = '生物工程学报'
        self.base_url = "http://journals.im.ac.cn/cjbcn/ch/reader/"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://journals.im.ac.cn/cjbcn/ch/reader/issue_list.aspx?year_id={}&quarter_id={}".format(years,num)
        print(url)
        try:
            r = requests.get(url, headers=hdrs, timeout=60)
        except:

            print('---------------访问失败--------------')
            return False
        line = 'No.' + str(num)
        print(line)
        html = Selector(r.text)
        a_list = html.xpath("//a[contains(@href,'create_pdf')]/@href").extract()
        self.all_num = len(a_list)
        for i,item in enumerate(a_list):
            title = str(i+1)
            pdfurl = self.base_url + item
            print('-----------开始下载-------------: %s' % title)
            pdfFilePath = Parent.makedir(self.journal, years, str(num), title, pdfRoot)
            if pdfFilePath == 1:
                self.suc += 1
                continue
            fig = Parent.getPdf(pdfurl, title, pdfFilePath, hdrs)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                    self.journal, years, num, title.strip())
                line = line + '\n'
                Parent.Record(line, self.journal)
                # print(line)
            if fig == 1:
                print('%s,pdf下载成功' % title)
                self.suc += 1
                line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                    self.journal, years, num, self.all_num, self.suc, self.ero)
                line = line + '\n'
                Parent.Record(line, self.journal)
        return True

# if __name__ == '__main__':
#     c = Cjbcn()
#     c.getpdf("2020",'1','./')