# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 14:51
# @Author  : qianjun
# @FileName: ogp.py
# @Software: PyCharm
"""石油地球物理勘探期刊我pdf 下载"""
import re
import sys

import requests
from urllib import parse
import parent
from bs4 import BeautifulSoup

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"http://www.ogp-cn.com.cn",

}
Parent = parent.Parent()

class ogp(object):


    def __init__(self):
        self.url = 'http://www.jos.org.cn/jos/ch/reader/issue_browser.aspx'
        self.ero = 0
        self.suc = 0
        self.cnt = 0

        self.journal = '石油地球物理勘探'

    def getpdf(self,years, num,pdfRoot):
        print(num)
        url = 'http://journal08.magtechjournal.com/Jwk_ogp/CN/article/showTenYearVolumnDetail.do?nian=%s' % (years)

        try:
            r = requests.get(url, headers=hdrs, timeout= 100)
        except:

            print('---------访问页面失败-----------')
            return False
        soup = BeautifulSoup(r.text, 'lxml')
        all_table = soup.select('a[href*="../volumn/volumn_"]')

        href =""
        # 循环取出列表中标签，剔除有img标签的
        for onetable in all_table:
            print("111")
            if onetable.find("img"):
                continue
            else:

                checkStr = "".join(onetable.stripped_strings).replace("\r\n","")

                matchObj = re.match(r'.*?No.(\S+).*?',checkStr)

                if matchObj:
                    print("222")
                    numStr = matchObj.group(1)
                    print(numStr)
                    # 当输入的期次与该值相等时，获取a链接标签,进行pdf下载操作
                    if numStr == num:
                        href = "".join(onetable['href']).replace("..","http://journal08.magtechjournal.com/Jwk_ogp/CN/")

        if not href:
            print("************格式异常*****************")
            return False

        # 重新请求页面
        print("列表url:%s"%href)
        try:
            r = requests.get(href, headers=hdrs, timeout= 100)

        except Exception as e:
            print("--------错误信息：%s-----------"%str(e))
            print('---------访问页面失败-----------')
            return False

        # 获取pdf链接

        soups = BeautifulSoup(r.text, 'lxml')
        pdf_hrefs = soups.select('a[href*="../article/downloadArticleFile.do?attachType=PDF"]')

        pdfnum =0
        self.cnt = len(pdf_hrefs)
        print('journal: %s, vol: %s。共有文章 %d；' % (
            self.journal, num, self.cnt))
        for one in pdf_hrefs:
            pdfnum += 1

            pdfurl ="".join(one['href']).replace("..","http://journal08.magtechjournal.com/Jwk_ogp/CN/")
            title = str(pdfnum)
            print("".join(one['href']))
            print('--------开始下载---------: %s' % title)

            pdfFilePath = Parent.makedir(self.journal, years, str(num), title, pdfRoot)
            if pdfFilePath == 1:

                self.suc += 1
                continue
            # pdf_hdrs = {"Cache-Control":"no-cache",
            #     "Connection":"keep-alive",
            #     "Content-Type":"application/x-download",
            #     "Server":"nginx/1.10.2",
            # "Accept-Encoding":"identity",
            #     "Transfer-Encoding":"chunked",
            #     "X-Frame-Options":"SAMEORIGIN"}
            fig = Parent.getPdf(pdfurl, title, pdfFilePath, hdrs)
            # self.cnt = len(downlist)
            # print("self.cnt:%s"%self.cnt)
            if fig == -1:
                self.ero += 1
                line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                    self.journal, years, num, title.strip())
                line = line + '\n'
                Parent.Record(line, self.journal)
            if fig == 1:
                print('%s,pdf下载成功' % title)
                self.suc += 1

                line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                    self.journal, years, num, self.cnt, self.suc, self.ero)
                line = line + '\n'
                Parent.Record(line, self.journal)

        return True

# if __name__ == '__main__':
#
#     work = ogp()
#     work.getpdf("2019","4","./")
