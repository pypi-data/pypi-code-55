# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : gfzxb.py
# @Software: PyCharm

# 1.高分子学报

import sys

import re
import requests
from bs4 import BeautifulSoup
from parsel import Selector
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }

Parent = parent.Parent()

class Gfzxb(object):

    def __init__(self):
        self.url = 'http://www.gfzxb.org/'
        self.journal = '高分子学报'
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.all_num = 0

    def getpdf(self, years, num, pdfRoot):

        url  = "http://www.gfzxb.org/article/{}/{}".format(years,num)
        print(url)
        try:
            r = requests.get(url, headers=hdrs, timeout=60)
        except:

            print('---------------访问失败--------------')
            return False
        line = 'No.' + str(num)
        print(line)
        soup = BeautifulSoup(r.text,'lxml')
        all_div = soup.find_all('div',class_='article-list')
        self.all_num = len(all_div)
        xx_num = 0
        for div in all_div:

            id_ = div.get('id')

            info = div.find('div',class_='article-list-time').find("font").get_text()
            info_pa = '\): (.*?)\.'
            title = re.findall(info_pa, info)
            if len(title) == 0:
                title = str(xx_num)
                xx_num +=1
            else:
                title = title[0]
            zy = div.find('div', class_='article-list-zy').find("font",class_='font3').find("a").get_text()
            if "[PDF 0KB]" in zy:
                self.suc +=1
                print('%s,pdf大小为0KB,跳过下载' % title)
                continue
            data = {
                'id':id_
            }
            pdfurl = 'http://www.gfzxb.org/article/exportPdf'
            print('-----------开始下载-------------: %s' % title)
            pdfFilePath = Parent.makedir(self.journal, years, str(num), title, pdfRoot)
            if pdfFilePath == 1:
                self.suc += 1
                continue
            fig = Parent.post_getpdf(data,pdfurl, title, pdfFilePath, hdrs)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (self.journal, years, num, title.strip())
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
#     a = Gfzxb()
#     a.getpdf("2020",'1','./')