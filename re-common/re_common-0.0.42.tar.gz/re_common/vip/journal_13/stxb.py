# -*- coding: utf-8 -*-
# @Time    : 2019/7/4 16:20
# @Author  : suhong
# @FileName: stxb.py
# @Software: PyCharm
import sys
import time

import requests
import  parent
from urllib import parse
from bs4 import BeautifulSoup
from lxml import etree

data = {}
hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"http://www.ecologica.cn",

}
Parent = parent.Parent()
class stxb(object):


    def __init__(self):
        self.url = 'http://www.ecologica.cn/stxb/ch/reader/issue_list.aspx?'
        self.ero = 0
        self.suc = 0
        self.cnt = 0
        self.title_c = 1
        self.journal = '生态学报'

    def getpdf(self,years, num,pdfRoot):

        url = 'http://www.ecologica.cn/stxb/ch/reader/issue_list.aspx?year_id=%s&quarter_id=%s'%(years,num)


        try:
            r = requests.get(url, headers=hdrs,  timeout =60)

            time.sleep(5)
        except:
            print('---------------访问失败------------')
            return False

        html = etree.HTML(r.content.decode())
        all_table = html.xpath("//table[@id='table24']")
        for tables in all_table[1:]:

            # 获取当前节点下所有的td width="430"
            all_td = tables.xpath("//td[@width='430']")
            self.cnt = len(all_td)

            for one in all_td:
                title =""
                id=""
                url=""
                # print(one.xpath("./a/text()"))
                # print(  one.xpath("normalize-space(./a/text())"))
                # print( one.xpath("./a/@href")[0].split("&")[0].split("=")[-1])
                try:
                    title = str(self.title_c)
                    # title = one.xpath("normalize-space(./a/text())")
                    print("pdf下载title:%s" % title)
                    id = one.xpath("./a/@href")[0].split("&")[0].split("=")[-1]
                    print("pdf下载id:%s" % id)
                    url ="http://www.ecologica.cn/stxb/ch/reader/create_pdf.aspx?file_no={}&quater_id=2&falg=1".format(id)

                    print("pdf下载链接：%s" % url)
                except Exception as e:
                    print("--------页面存在异常格式:%s-%s,错误原因:%s" % (years, num,str(e)))
                    sys.exit(-1)

                print('--------开始下载---------: %s' % title)

                pdfFilePath =Parent.makedir(self.journal, years, str(num),title,pdfRoot)
                if pdfFilePath == 1:
                    self.suc += 1
                    continue
                fig = Parent.getPdf(url, title, pdfFilePath,hdrs)
                if fig == -1:
                    self.ero += 1
                    line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                    self.journal, years, num, title.strip())
                    line = line + '\n'
                    Parent.Record(line,self.journal)
                if fig == 1:
                    print('%s,pdf下载成功' % title)
                    self.suc += 1
                    self.title_c += 1

                    line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                    self.journal, years, num, self.cnt, self.suc, self.ero)
                    line = line + '\n'
                    Parent.Record(line,self.journal)
            endline = ""
            Parent.Record(endline, self.journal)

            return True


if __name__ == "__main__":
    work =stxb()
    work.getpdf("2015","3","./")