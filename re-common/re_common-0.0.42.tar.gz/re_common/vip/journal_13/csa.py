# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : cjbcn.py
# @Software: PyCharm

# 1.计算机系统应用

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

class Csa(object):

    def __init__(self):
        self.journal = '计算机系统应用'
        self.base_url = "http://www.c-s-a.org.cn/csa/ch/reader/"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://www.c-s-a.org.cn/csa/ch/reader/issue_list.aspx?year_id={}&quarter_id={}".format(years,num)
        print(url)
        try:
            r = requests.get(url, headers=hdrs, timeout=60)
        except:

            print('---------------访问失败--------------')
            return False
        line = 'No.' + str(num)
        print(line)

        html = Selector(r.text)
        li_list  = html.xpath("//li[@class='zynf']")
        self.all_num = len(li_list)
        for li in li_list:
            info = li.xpath("./text()").extract()[0]
            a = li.xpath(".//a[contains(@href,'create_pdf')]/@href").extract()[0]
            info_pa = '\):(.*?) \['
            title = re.findall(info_pa, info)[0]

            pdfurl = self.base_url + a
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
#     c = Csa()
#     c.getpdf("1992",'1','./')