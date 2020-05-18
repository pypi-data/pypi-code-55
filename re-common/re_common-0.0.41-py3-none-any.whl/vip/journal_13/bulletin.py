# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : bulletin.py
# @Software: PyCharm

# 1.中国科学院院刊

import sys

import re
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "http://www.bulletin.cas.cn/zgkxyyk/ch/reader/issue_list.aspx",
        }

Parent = parent.Parent()

class Bulletin(object):

    def __init__(self):
        self.journal = '中国科学院院刊'
        self.base_url = "http://www.actasc.cn/hjkxxb/ch/reader/"
        self.base_url = "http://www.bulletin.cas.cn/zgkxyyk/ch/reader/"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://www.bulletin.cas.cn/zgkxyyk/ch/reader/issue_list.aspx"
        print(url)
        try:
            data = {
                'year_id': years,
                'quarter_id': num
            }
            r = requests.post(url, headers=hdrs,data=data, timeout=60)
        except:

            print('---------------访问失败--------------')
            return False
        line = 'No.' + str(num)
        print(line)

        soup = BeautifulSoup(r.text, 'lxml')
        tr_list = soup.find_all('tr',class_='listtr')
        self.all_num = len(tr_list)
        title = 1
        for tr in tr_list:
            pdfurl = self.base_url + tr.find_all('td')[3].find("a").get('href')

            print('-----------开始下载-------------: %s' % title)
            pdfFilePath = Parent.makedir(self.journal, years, str(num), str(title), pdfRoot)
            if pdfFilePath == 1:
                self.suc += 1
                continue
            fig = Parent.getPdf(pdfurl, title, pdfFilePath, hdrs)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                    self.journal, years, num, str(title))
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
                title +=1
        return True
if __name__ == '__main__':
    b = Bulletin()
    b.getpdf("2020",'2','./')