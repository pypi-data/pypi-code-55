# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 16:04
# @Author  : suhong
# @File    : hyxb.py
# @Software: PyCharm


# 1.海洋学报：英文版

import sys


import requests
from bs4 import BeautifulSoup
# from parsel import Selector
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "http://www.hyxb.org.cn/aosen/ch/reader/issue_list.aspx",
        }

Parent = parent.Parent()

class Hyxb(object):

    def __init__(self):
        self.journal = '海洋学报(英文版)'
        self.base_url = "http://www.hyxb.org.cn/aosen/ch/reader/"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://www.hyxb.org.cn/aosen/ch/reader/issue_list.aspx"
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
        all_table = soup.find_all('table', id='table24')
        if len(all_table) == 1:
            print("年份或者期刊错误")
            return False
        for table in all_table:
            for table_2 in table.find_all("table",width='100%'):
                for t in table_2:
                    a_num = len(t.find_all("a"))
                    if a_num == 3:
                        self.all_num += 1
                    if "Package" in t.get_text():
                        self.all_num -= 1
                        continue
                    continue
        title = 1
        for table in all_table:
            for table_2 in table.find_all("table", width='100%'):
                for t in table_2:
                    a_num = len(t.find_all("a"))
                    if a_num == 3:
                        pdfurl = self.base_url + t.find_all('td')[2].find("a").get('href')
                        print('-----------开始下载-------------: %s' % title)
                        if "Package" in t.get_text():
                            p_title = years + '-' + num + '整刊'
                            pdfFilePath = Parent.makedir(self.journal, years, str(num), str(p_title), pdfRoot)
                        else:
                            pdfFilePath = Parent.makedir(self.journal, years, str(num), str(title), pdfRoot)
                            if type(title) == int:
                                title += 1
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
                            print('%s,pdf下载成功' % (title-1))
                            self.suc += 1
                            line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                                self.journal, years, num, self.all_num+1, self.suc, self.ero)
                            line = line + '\n'
                            Parent.Record(line, self.journal)
        return True
# if __name__ == '__main__':
#     h = Hyxb()
#     h.getpdf("2020",'4','./')