# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 10:12
# @Author  : suhong
# @File    : jos.py
# @Software: PyCharm
import sys

import requests
from urllib import parse
import parent
from bs4 import BeautifulSoup

# 软件学报

hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Referer" :"http://www.jos.org.cn/",

}
Parent = parent.Parent()

class Jos(object):


    def __init__(self):
        self.url = 'http://www.jos.org.cn/jos/ch/reader/issue_browser.aspx'
        self.ero = 0
        self.suc = 0
        self.cnt = 0

        self.journal = '软件学报'

    def getpdf(self,years, num,pdfRoot):

        url = 'http://www.jos.org.cn/jos/ch/reader/issue_list.aspx?year_id=%s&quarter_id=%s' % (years, num)

        try:
            r = requests.get(url, headers=hdrs, timeout= 100)
        except:

            print('---------访问页面失败-----------')
            return False
        soup = BeautifulSoup(r.text, 'lxml')
        all_table = soup.find_all('table', id='table24')
        title = ''
        # print(all_table)
        # with open("./jos.html", "w", encoding="utf-8") as f:
        #     print("写入成功")
        #     f.write(r.content.decode())
        downlist=[]
        titlenum = 0

        for table in all_table[1:]:
            all_td = table.find_all('a', target='_blank')


            print("first pdf:%s" % self.cnt)
            for ta in all_td:


                b = ta.find('b')
                if b.text.upper() != 'PDF':
                    continue

                self.cnt +=1
        # print("first pdf:%s" % self.cnt)
        for table in all_table[1:]:
            all_td = table.find_all('a', target='_blank')



            for ta in all_td:


                b = ta.find('b')
                if b.text.upper() != 'PDF':
                    continue
                pagedtad = ta.parent.text.strip()
                downlist.append("1")

                list = pagedtad.split('[')
                data = list[0]
                title = data.split(':')[1].strip()

                if num == "0" and years =="0":

                    titlenum += 1
                    title = str(titlenum)
                if title =="0":
                    titlenum += 1
                    title = str(titlenum)
                if len(title.strip()) == 0:
                    title = table.previous_sibling.text
                href = ta.get('href')
                parseResult = parse.urlparse(href)
                param_dict = parse.parse_qs(parseResult.query)
                id = param_dict['file_no'][0]
                pdfurl = 'http://www.jos.org.cn/jos/ch/reader/create_pdf.aspx?file_no=%s&year_id=%s&quarter_id=%s&falg=1' % (
                id, years, num)
                # print(pdfurl)
                print(pdfurl)
                print('--------开始下载---------: %s' % title)

                pdfFilePath = Parent.makedir(self.journal, years, str(num), title, pdfRoot)
                if pdfFilePath == 1:
                    self.suc += 1
                    continue
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
            # self.cnt = len(downlist)
            print('journal: %s, vol: %s。共有文章 %d；' % (
                self.journal,num, self.cnt))

        # 下载封面
        print("--------------------开始下载封面------------------")
        data = '00' + num
        href = ''
        url = 'http://www.jos.org.cn/jos/ch/reader/view_fixed_content.aspx?id=gqfm'
        titlename = '%s年第%s期' % (years, data[-2:])
        # print(titlename)

        try:
            r = requests.get(url, headers=hdrs, timeout= 100)
        except:

            print('----------访问失败----------------')

        soup = BeautifulSoup(r.text, 'lxml')
        span = soup.find('span', id ='Content')

        all_a = span.find_all('a')

        fmurl=""
        for ta in all_a:

            if ta.text.strip()  == titlename:

                href = ta.get('href')

                fmurl = href
            if num.find("K") != -1 or num.find("k") != -1:


                titlename = '%s年' % (years)

                # print('%s年第%s期' % (years, data[-2:]))
                # print(ta.text.strip())

                if ta.text.strip() == titlename +"增刊":
                    #print("增刊")

                    href = ta.get('href')

                    fmurl = href

                elif ta.text.strip() == titlename +"ZK期":
                    #print("zk期")
                    href = ta.get('href')

                    fmurl = href
                elif ta.text.strip() == titlename + "增刊2":
                    #print("增刊2")
                    href = ta.get('href')

                    fmurl = href
                elif ta.text.strip() == titlename + "增刊1":
                    #print("增刊1")
                    href = ta.get('href')

                    fmurl = href
                elif ta.text.strip() == titlename + "第ZK期":
                    #print("增刊1")
                    href = ta.get('href')

                    fmurl = href

        if fmurl=="":
            print("--------------下载封面存在特殊情况,请检查---------------%s,%s"%(years, str(num)))
            if num == "0" and years == "0":
                print("------------经检查，0年0期无封面下载----------")
                endline = ""
                Parent.Record(endline, self.journal)
                return True
            return False
        if fmurl.find("www") ==-1:
            fmurl = "http://www.jos.org.cn" +fmurl

        print("---------封面链接---------%s"%fmurl)
        pdfFilePath = Parent.makedir(self.journal, years, str(num), years+"_"+str(num), pdfRoot)
        if pdfFilePath == 1:
            self.suc += 1
            return False
        print("当前封面下载链接：%s"%fmurl)
        fig = Parent.getPdf(fmurl, years+"_"+str(num), pdfFilePath, hdrs)
        if fig == -1:
            self.ero += 1
            line = 'journal: %s, years: %s, issue: %s: %s 下载失败' % (
                self.journal, years, num, (years+"_"+str(num)).strip())
            line = line + '\n'
            Parent.Record(line, self.journal)
        if fig == 1:
            print('%s,pdf下载成功' % (years+"_"+str(num)))
            self.suc += 1

            line = 'journal: %s, years: %s, issue: %s。共有文章 %d；下载PDF %d；失败 %d' % (
                self.journal, years, num, self.cnt, self.suc, self.ero)
            line = line + '\n'
            Parent.Record(line, self.journal)

        endline = ""
        Parent.Record(endline, self.journal)
        return True

# if __name__ == '__main__':
#     work = Jos()
#     work.getpdf("2019","9","./")


