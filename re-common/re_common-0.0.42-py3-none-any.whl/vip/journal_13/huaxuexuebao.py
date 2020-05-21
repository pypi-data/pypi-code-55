# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 11:49
# @Author  : suhong
# @File    : huaxuexuebao.py
# @Software: PyCharm

"""化学学报"""

import requests
from bs4 import BeautifulSoup
from lxml import etree
import  parent

# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 15:11
# @Author  : qianjun
# @FileName: huaxuexuebao.py
# @Software: PyCharm

"""化学学报"""
import sys

import requests
from bs4 import BeautifulSoup
from lxml import etree
import  parent

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer": "http://sioc-journal.cn",
        }

Parent = parent.Parent()

class jwk_hxxb(object):

    def __init__(self):
        self.url = 'http://sioc-journal.cn/Jwk_hxxb/CN/volumn/current.shtml'
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.journal = '化学学报'

    def getpdf(self,years, num,pdfRoot):

        url = 'http://sioc-journal.cn/Jwk_hxxb/CN/article/showTenYearVolumnDetail.do?nian=%s' % years
        print(url)
        try:
            r = requests.get(url, hdrs, timeout = 60)
        except:

            print('---------------访问失败--------------')
            return False
        line = 'No.' + str(num)
        print(line)
        # 创建xpath对象
        html = etree.HTML(r.content.decode())


        # # 获取所有的标签对象
        hreflist = html.xpath("//td[@height='1']/../../tr[last()]//a/@href")

        if not hreflist:
            print("------------页面存在变化------------")
            return False

        # 获取最大页数
        maxnum = len(hreflist)

        if  int(num) > maxnum or int(num)<0:
            print("------------输入期次异常，请输入正确期次------------")
            return False
        href = hreflist[::-1][int(num)-1].replace("..","")

        # 构建下一个url连接
        nexturl = 'http://sioc-journal.cn/Jwk_hxxb/CN' + href
        try:
            response = requests.get(nexturl, hdrs, timeout=60)
        except:
            print('--------页面访问失败------------')
            return False

        soup = BeautifulSoup(response.text, 'lxml')
        all_td = soup.find_all('div', class_='issue-item_metadata')
        for td in all_td:
            ta = td.find('span',class_ ='j-pdf').find("a")
            titletext = td.find('div', class_='abs_njq', ).text

            titlelist = titletext.split(',')

            title = titlelist[-1].replace('pp', '').strip()
            title = title.split("DOI")[0].strip()

            href = ta.get('onclick')

            list = href.split(',')

            htmlid = list[1]

            id = htmlid.replace('\'', '')

            pdfurl = "http://sioc-journal.cn/Jwk_hxxb/CN/article/downloadArticleFile.do?attachType=PDF&id=%s" % id

            print('-----------开始下载-------------: %s' % title)
            pdfFilePath = Parent.makedir(self.journal, years, str(num),title,pdfRoot)
            if pdfFilePath == 1:
                self.suc += 1
                continue
            fig = Parent.getPdf(pdfurl, title, pdfFilePath,hdrs)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                self.journal, years, num, title.strip())
                line = line + '\n'
                Parent.Record(line,self.journal)
                # print(line)
            if fig == 1:
                print('%s,pdf下载成功' % title)
                self.suc += 1
                line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                self.journal, years, num, len(all_td), self.suc, self.ero)
                line = line + '\n'
                Parent.Record(line,self.journal)
        return  True

# if __name__ == '__main__':
#     j = jwk_hxxb()
#     j.getpdf("2020","2",'./')