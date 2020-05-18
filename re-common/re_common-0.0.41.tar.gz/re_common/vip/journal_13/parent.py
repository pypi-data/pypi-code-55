# -*- coding: utf-8 -*-
# @Time    : 2020/04/30 11:32
# @Author  : suhong
# @FileName: papent.py
# @Software: PyCharm
import logging
import time
import re
import os
from contextlib import closing

import requests
bar_length = 20



class Parent(object):

    def __int__(self):
        self.PDFRoot =""


    def isValidPDF_pathfile(self, pathfile):

        with open(pathfile, mode='rb') as f:
            content = f.read()
        partBegin = content[0:20]
        if partBegin.find(rb'%PDF-1.') < 0:
            print('Error: not find %PDF-1.')
            return False

        idx = content.rfind(rb'%%EOF')
        if idx < 0:
            print('Error: not find %%EOF')
            return False

        partEnd = content[(0 if idx - 100 < 0 else idx - 100): idx + 5]
        if not re.search(rb'startxref\s+\d+\s+%%EOF$', partEnd):
            print('Error: not find startxref')
            return False

        return True

    def Record(self, text,journal):
        name = time.strftime('%Y%m%d', time.localtime(time.time())) + '.txt'
        fileroot1 = os.path.join(self.PDFRoot, journal)
        filepath = os.path.join(fileroot1,name)
        with open(filepath, "a", encoding="utf-8") as f:
            line =text.strip() + '\n'
            f.write(line)

    def makedir(self,journal, years, num,tiele,pdfRoot):
        self.PDFRoot =pdfRoot
        newPdfPath = os.path.join(self.PDFRoot, journal, years, num)
        if not os.path.exists(newPdfPath):
            os.makedirs(newPdfPath)
        tiele = tiele.replace('\\', '_').replace('/', '_').replace(':', '_').replace('>', '_').replace('*', '_').replace('?','_').replace('<', '_').replace('|', '_').replace('"', '_').replace(':', '_')
        pdfFilePath = os.path.join(newPdfPath, tiele + '.pdf')
        if os.path.exists(pdfFilePath):
            filesize = os.path.getsize(pdfFilePath)
            if filesize <= 3072:
                print("%s,pdf存在，大小有问题" % tiele)
                os.remove(pdfFilePath)

            else:
                print('%s, pdf存在' % tiele)
                return 1
        return pdfFilePath

    def formatFloat(self,num):
        # 进度条函数
        return '{:.2f}'.format(num)

    def getPdf(self, pdfurl, title, pdfFilePath,hdrs):
        hashes = None
        try:
            try:
                r = requests.get(pdfurl)
            except:
                print('%s, pdf下载失败' % title)
                return -1
            if r== '':
                print('%s,pdf下载失败' % title)
                return -1
            print("pdf:%s"%pdfFilePath)
            if r.text.find("本篇文章目前没有全文可供下载！") > 1:
                print('%s,pdf无全文' % title)
                return -1
            length = float(len(r.content))
            count = 0
            time1 = time.time()


            with closing(r) as r:
                with open(pdfFilePath, 'wb') as f:

                    for chunk in r.iter_content(chunk_size=512):

                        if chunk:
                            f.write(chunk)
                            count += len(chunk)
                            if time.time() - time1 > 1:
                                print("**********")
                                p = count / length * 100
                                hashes = '▆' * int(p / 100.0 * bar_length)
                                spaces = ' ' * (bar_length - len(hashes))
                                print("\r----%s: |%s| %s%% " % (title, hashes + spaces, self.formatFloat(p)), end="")
                                time.sleep(0.3)
                                time1 = time.time()

            if count == length:
                hashes = '▆' * bar_length
                spaces = ' ' * (bar_length - len(hashes))
                print("\r----%s: |%s| %s%% " % (title, hashes + spaces, "100"), end="")
                print("")
                return 1

            if not Parent.isValidPDF_pathfile(self, pdfFilePath):
                os.remove(pdfFilePath)
                return -1

            return 1
        except Exception as e:
            print(str(e))
            if hashes:
               pass
            logging.info("sava_%s error %s" % (title,str(e)))
            return False

    def post_getpdf(self, data, pdfurl, title, pdfFilePath,hdrs):
        hashes = None
        try:
            try:
                r = requests.post(pdfurl,data=data)
            except:
                print('%s, pdf下载失败' % title)
                return -1
            if r == '':
                print('%s,pdf下载失败' % title)
                return -1
            print("pdf:%s" % pdfFilePath)
            length = float(len(r.content))
            count = 0
            time1 = time.time()

            with closing(r) as r:
                with open(pdfFilePath, 'wb') as f:

                    for chunk in r.iter_content(chunk_size=512):

                        if chunk:
                            f.write(chunk)
                            count += len(chunk)
                            if time.time() - time1 > 1:
                                print("**********")
                                p = count / length * 100
                                hashes = '▆' * int(p / 100.0 * bar_length)
                                spaces = ' ' * (bar_length - len(hashes))
                                print("\r----%s: |%s| %s%% " % (title, hashes + spaces, self.formatFloat(p)), end="")
                                time.sleep(0.3)
                                time1 = time.time()

            if count == length:
                hashes = '▆' * bar_length
                spaces = ' ' * (bar_length - len(hashes))
                print("\r----%s: |%s| %s%% " % (title, hashes + spaces, "100"), end="")
                print("")
                return 1

            if not Parent.isValidPDF_pathfile(self, pdfFilePath):
                os.remove(pdfFilePath)
                return -1

            return 1
        except Exception as e:
            print(str(e))
            if hashes:
                pass
            logging.info("sava_%s error %s" % (title, str(e)))
            return False

if __name__ == "__main__":
    pass