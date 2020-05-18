# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 12:19
# @Author  : suhong
# @FileName: springer.py
# @Software: PyCharm
import math
import sys
import time

import requests
import  parent
from urllib import parse
from bs4 import BeautifulSoup
from lxml import etree

data = {}
hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"https://link.springer.com",

}
Parent = parent.Parent()
class springer(object):


    def __init__(self):
        self.url = 'https://link.springer.com'
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.journal = 'springer'

    def getpdf(self,jid,vol, num,pdfRoot):

        url = 'https://link.springer.com/journal/{}/{}/{}'.format(jid,vol,num)
        # data['year_id'] = years
        # data['quarter_id'] = num
        # print(years,num)
        # print(data)

        if "suppl" in num:
            url ='https://link.springer.com/journal/{}/{}/{}/{}'.format(jid,vol,num.split("_")[0],num.split("_")[-1])
        print(url)
        try:
            r = requests.get(url, headers=hdrs,  timeout =60)

            time.sleep(5)
        except:
            print('---------------访问失败------------')
            return False

        bs = BeautifulSoup(r.text, 'lxml')

        if bs.find(class_='toc').find("h2").find("span"):

            self.cnt = int("".join((bs.find(class_='toc').find("h2").find("span").stripped_strings)).replace(" articles","").replace("(","").replace(")",""))
            print("共计获取pdf文章:%s"%self.cnt)

        divs = bs.find_all(class_="toc-item")
        pdfnum = 0
        for onediv in divs:
            pdfnum +=1
            pdfurl =""
            page =""
            title1=""
            title=""

            if onediv.find(class_="actions"):

                if onediv.find(class_="actions").find("a",id='toc-pdf-link'):

                    # 获取下载pdf连接
                    pdfurl = "".join(onediv.find(class_="actions").find("a",id='toc-pdf-link')["href"])

                # 获取页数
                if onediv.find(class_="page-range"):
                    page = "".join(onediv.find(class_="page-range").stripped_strings).replace("Pages","").strip()

                # 获取title
                if onediv.find("h3",class_="title"):

                    if onediv.find("h3",class_="title").find("a"):

                        title1 = "".join(onediv.find("h3",class_="title").find("a").stripped_strings).strip()
            if page=="":
                title =title1

            else:
                title=page

            # 计数命名pdf
            title=str(pdfnum)

            if pdfurl == "":
                print("未发现pdf存在")
                continue
            url = "https://link.springer.com" +pdfurl

            print('--------开始下载---------: %s' % title1)
            pdfFilePath =Parent.makedir(self.journal, vol, str(num),title,pdfRoot)
            if pdfFilePath == 1:
                self.suc += 1
                continue
            pdf_hdrs = {"Connection": "keep-alive",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "Referer": "https://link.springer.com", }
            fig = Parent.getPdf(url, title, pdfFilePath,pdf_hdrs)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, vol: %s, issue: %s: %s 下载失败' % (
                self.journal, vol, num, title.strip())
                line = line + '\n'
                Parent.Record(line,self.journal)
            if fig == 1:
                print('%s,pdf下载成功' % title)
                self.suc += 1

                line = 'journal: %s, vol: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                self.journal, vol, num, self.cnt, self.suc, self.ero)
                line = line + '\n'
                Parent.Record(line,self.journal)

        if  math.ceil(self.cnt  / 20) > 1 :
            # 进行翻页操作
            allnum= math.ceil(self.cnt  / 20)

            for i in range(2,allnum+1):
                url = 'https://link.springer.com/journal/{}/{}/{}/page/{}'.format(jid, vol, num,str(i))
                # data['year_id'] = years
                # data['quarter_id'] = num
                # print(years,num)
                # print(data)

                if "suppl" in num:
                    url = 'https://link.springer.com/journal/{}/{}/{}/{}/page/{}'.format(jid, vol, num.split("_")[0],
                                                                                 num.split("_")[-1],str(i))
                print(url)
                try:
                    r = requests.get(url, headers=hdrs, timeout=60)

                    time.sleep(5)
                except:
                    print('---------------访问失败------------')
                    return False

                bs = BeautifulSoup(r.text, 'lxml')

                # if bs.find(class_='toc').find("h2").find("span"):
                #     self.cnt = int(
                #         "".join((bs.find(class_='toc').find("h2").find("span").stripped_strings)).replace(" articles",
                #                                                                                           "").replace(
                #             "(", "").replace(")", ""))
                #     print("共计获取pdf文章:%s" % self.cnt)

                divs = bs.find_all(class_="toc-item")

                for onediv in divs:
                    pdfnum +=1
                    pdfurl = ""
                    page = ""
                    title1 = ""
                    title = ""

                    if onediv.find(class_="actions"):

                        if onediv.find(class_="actions").find("a", id='toc-pdf-link'):
                            # 获取下载pdf连接
                            pdfurl = "".join(onediv.find(class_="actions").find("a", id='toc-pdf-link')["href"])

                        # 获取页数
                        if onediv.find(class_="page-range"):
                            page = "".join(onediv.find(class_="page-range").stripped_strings).replace("Pages",
                                                                                                      "").strip()

                        # 获取title
                        if onediv.find("h3", class_="title"):

                            if onediv.find("h3", class_="title").find("a"):
                                title1 = "".join(onediv.find("h3", class_="title").find("a").stripped_strings).strip()
                    if page == "":
                        title = title1

                    else:
                        title = page

                    # 重命名
                    title = str(pdfnum)

                    if pdfurl == "":
                        print("未发现pdf存在")
                        continue
                    url = "https://link.springer.com" + pdfurl

                    print('--------开始下载---------: %s' % title1)
                    pdfFilePath = Parent.makedir(self.journal, vol, str(num), title, pdfRoot)
                    if pdfFilePath == 1:
                        self.suc += 1
                        continue
                    pdf_hdrs ={   "Connection":"keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"https://link.springer.com",}
                    fig = Parent.getPdf(url, title, pdfFilePath, pdf_hdrs)
                    if fig == -1:
                        self.ero += 1
                        line = 'journal: %s, vol: %s, issue: %s: %s 下载失败' % (
                            self.journal, vol, num, title.strip())
                        line = line + '\n'
                        Parent.Record(line, self.journal)
                    if fig == 1:
                        print('%s,pdf下载成功' % title)
                        self.suc += 1

                        line = 'journal: %s, vol: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                            self.journal, vol, num, self.cnt, self.suc, self.ero)
                        line = line + '\n'
                        Parent.Record(line, self.journal)

        endline = ""
        Parent.Record(endline, self.journal)
        return True


if __name__ == "__main__":

    work =springer()
    work.getpdf("40820","10","3","F:\\")