# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : actasc.py
# @Software: PyCharm

# 1.环境科学学报

import sys

import re
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "http://www.actasc.cn/hjkxxb/ch/reader/issue_list.aspx",
        }

Parent = parent.Parent()

class Actasc(object):

    def __init__(self):
        self.url = 'http://www.actasc.cn/hjkxxb/ch/index.aspx'
        self.journal = '环境科学学报'
        self.base_url = "http://www.actasc.cn/hjkxxb/ch/reader/"
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://www.actasc.cn/hjkxxb/ch/reader/issue_list.aspx"
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
        all_table = soup.find_all('table',id='table24')
        if len(all_table) == 1:
            print("年份或者期刊错误")
            return False
        for table in all_table:
            for tr in table.find_all("tr"):
                a_num = len(tr.find_all("a"))
                if a_num == 3:
                    self.all_num += 1
                    continue
                continue
                # 当a_num == 3 就是包含信息的tr
        for table in all_table:
            for tr in table.find_all("tr"):
                a_num = len(tr.find_all("a"))
                if a_num == 3:
                    pdfurl =self.base_url + tr.find_all('td')[1].find_all('a')[2].get('href')
                    info = tr.find_all('td')[1].get_text()
                    info_pa = ':(.*) \[摘要\]'
                    title = re.findall(info_pa,info)[0]

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
#     a = Actasc()
#     a.getpdf("1985",'1','./')