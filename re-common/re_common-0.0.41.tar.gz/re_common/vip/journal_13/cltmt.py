# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 15:15
# @Author  : qianjun
# @FileName: cltmt.py
# @Software: PyCharm

import sys
import time

import requests
import  parent
from urllib import parse
from bs4 import BeautifulSoup
from lxml import etree

# 汉语教学方法与技术
data = {}
hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"https://engagedscholarship.csuohio.edu",

}
Parent = parent.Parent()
class cltmt(object):


    def __init__(self):
        self.url = 'https://engagedscholarship.csuohio.edu/cltmt/'
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.journal = '汉语教学方法与技术'

    def getpdf(self,vol, num,pdfRoot):

        url = 'https://engagedscholarship.csuohio.edu/cltmt/vol{}/iss{}'.format(vol,num)
        # data['year_id'] = years
        # data['quarter_id'] = num
        # print(years,num)
        # print(data)
        # print(url)

        try:
            r = requests.get(url, headers=hdrs,  timeout =60)

            time.sleep(5)
        except:
            print('---------------访问失败------------')
            return False

        bs = BeautifulSoup(r.text, 'lxml')

        if bs.find(class_='article-list'):

            if bs.find(class_='article-list').find_all(class_="doc"):
                self.cnt = len(bs.find(class_='article-list').find_all(class_="doc"))
                print('journal: %s, vol: %s, issue: %s。共有文章 %d；' % (
                        self.journal, vol, num, self.cnt))

                for infotag in bs.find(class_='article-list').find_all(class_="doc"):
                    pdfurl =""
                    title=""

                    if infotag.find(class_="pdf"):

                        # 获取pdf下载链接
                        pdfurl = "".join(infotag.find(class_="pdf").find("a")["href"])

                        # 获取所有的p标签
                        allPtag =infotag.find_all("p")

                        for Ptag in allPtag:
                            if 'class' not in Ptag.attrs:

                                title = "".join(Ptag.a.stripped_strings)

                    if title=="":
                        title="no title to get"

                    print('--------开始下载---------: %s' % title)
                    print('--------下载链接---------: %s' % pdfurl)
                    pdfFilePath =Parent.makedir(self.journal, vol, str(num),str(self.suc),pdfRoot)
                    if pdfFilePath == 1:
                        self.suc += 1
                        continue
                    fig = Parent.getPdf(pdfurl, title, pdfFilePath,hdrs)
                    if fig == -1:
                        self.ero += 1
                        line = 'journal: %s, vol: %s, issue: %s: %s 下载失败' % (
                        "汉语教学方法与技术", vol, num, title.strip())
                        line = line + '\n'
                        Parent.Record(line,self.journal)
                    if fig == 1:
                        print('%s,pdf下载成功' % title)
                        self.suc += 1

                        line = 'journal: %s, vol: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                        self.journal, vol, num, self.cnt, self.suc, self.ero)
                        line = line + '\n'
                        Parent.Record(line,self.journal)
                line =""
                line = line + '\n'
                Parent.Record(line, self.journal)
                return True


# if __name__ == "__main__":
#
#     work =cltmt()
#     work.getpdf("1","3","./")
