# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 11:34
# @Author  : suhong
# @File    : down.py
# @Software: PyCharm


import os
import webbrowser

import toml
import actasc
import cltmt
import hyxb
import bulletin
import chinjmap
import gfzxb
import cjbcn
import jos
import csa
import huaxuexuebao
import ogp
import stxb
import springer
# import teepc_cn
# import jos

# import springer
# import cltmt
# import ogp

DstRoot=""

def ReadConfig():

    # 读取配置文件
    global DstRoot
    cfgFile = 'config.toml'

    with open(cfgFile, mode='rb') as f:
        content = f.read()

    if content.startswith(b'\xef\xbb\xbf'):  # 去掉 utf8 bom 头
        content = content[3:]

    dic = toml.loads(content.decode('utf8'))

    # 读取输出路径
    DstRoot = dic['DstRoot'].strip()
    if not os.path.exists(DstRoot):
        os.makedirs(DstRoot)

    print("PDFRoot: %s"%DstRoot)
    print("Read config.toml successed!")


def down():
    return 1
def work():
    # 开关控制
    while True:
        # 选择进行操作
        print("---------------程序初始化完成---------------")
        print("1、环境科学学报")
        print("2、海洋学报：英文版")
        print("3、中国科学院院刊")
        print("4、中国现代应用药学")
        print("5、高分子学报")
        print("6、生物工程学报")
        print("7、软件学报")
        print("8、计算机系统应用")
        print("9、化学学报")
        print("10、生态学报")
        print("11、纳微快报")
        print("12、汉语教学方法与技术")
        print("13、石油地球物理勘探")
        print("注意事项：期刊编号为11时（输入years,代表原网站期刊id,下载时，输入刊id,卷,期）--应通用于springer所有期刊")
        print("注意事项：期刊编号为12时（不用输入years,下载时,输入卷,期）")


        while True:
            journalChouse = input("请输入期刊对应编号：")
            if int(journalChouse) not in [i+1 for i in range(13)]:
                print([i+1 for i in range(13)])
                print("-----------请输入正确期刊对应编号-------------")
                continue
            if journalChouse == "1":
                url ="http://www.actasc.cn/hjkxxb/ch/index.aspx"
            if journalChouse == "2":
                url ="http://www.hyxb.org.cn/aosen/ch/index.aspx"
            if journalChouse == "3":
                url ="http://www.bulletin.cas.cn/zgkxyyk/ch/reader/issue_browser.aspx"
            if journalChouse == "4":
                url = "http://www.chinjmap.com/ch/index.aspx"
            if journalChouse == "5":
                url ="http://www.gfzxb.org/"
            if journalChouse == "6":
                url ="http://journals.im.ac.cn/cjbcn/ch/index.aspx"
            if journalChouse == "7":
                url ="http://www.jos.org.cn/jos/ch/reader/issue_browser.aspx"
            if journalChouse == "8":
                url ="http://www.c-s-a.org.cn/csa/ch/index.aspx"
            if journalChouse == "9":
                url ="http://sioc-journal.cn/Jwk_hxxb/CN/0567-7351/home.shtml"
            if journalChouse == "10":
                url ="http://www.ecologica.cn/stxb/ch/reader/issue_list.aspx?"
            if journalChouse == "11":
                url ="https://link.springer.com/journal/volumesAndIssues/40820"
            if journalChouse == "12":
                url = "https://engagedscholarship.csuohio.edu/cltmt/"
            if journalChouse == "13":
                url = "http://journal08.magtechjournal.com/Jwk_ogp/CN/volumn/home.shtml "


            webbrowser.open(url, new=0, autoraise=True)
            # webbrowser.open_new(url)
            # webbrowser.open_new_tab(url)
            if journalChouse != "12":
                if journalChouse == "11" :
                    year = input("请输入需要采集的期刊id:")
                else:
                    year = input("请输入需要采集的年份:")
                    if year != "0":
                        if len(year) != 4 or not year.isdigit():
                            print("-----------请输入正确年份-------------")
                            continue

            if journalChouse == "11" or journalChouse == "12":
                vol = input("请输入需要采集的卷次:")
                if (journalChouse) == "11":
                    print("如期次有：This is a supplement情况，输入期次时：期次+'_'+suppl 如(1_suppl)")

            if journalChouse == "13":
                print("num 为No. 后的值，如No.1 , num = 1.No.增刊1, num= 增刊1")

            num = input("请输入需要采集的期次:")
            check = input("确认输入无误：y / n：")

            if check =="y":
                break
            elif check =="n":
                continue
            else:
                print("请输入正确指令")


        checknum =False
        switch = ""

        if journalChouse == "1":
            ReadConfig()
            work = actasc.Actasc()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "2":
            ReadConfig()
            work = hyxb.Hyxb()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "3":
            ReadConfig()
            work = bulletin.Bulletin()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "4":
            ReadConfig()
            work = chinjmap.Chinjmap()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "5":
            ReadConfig()
            work =gfzxb.Gfzxb()
            checknum = work.getpdf(year,num, DstRoot)

        elif journalChouse == "6":
            ReadConfig()
            work = cjbcn.Cjbcn()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "7":
            ReadConfig()
            work = jos.Jos()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "8":
            ReadConfig()
            work = csa.Csa()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "9":
            ReadConfig()
            work = huaxuexuebao.jwk_hxxb()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "10":
            ReadConfig()
            work = stxb.stxb()
            checknum = work.getpdf(year, num, DstRoot)

        elif journalChouse == "11":
            ReadConfig()
            work = springer.springer()
            checknum = work.getpdf(year, vol, num, DstRoot)

        elif journalChouse == "12":
            ReadConfig()
            work = cltmt.cltmt()
            checknum = work.getpdf(vol, num, DstRoot)

        elif journalChouse == "13":
            ReadConfig()
            work = ogp.ogp()
            checknum = work.getpdf(year, num, DstRoot)


            # elif journalChouse == "5":
        #     print("5")
        # elif journalChouse == "6":
        #     print("6")
        # elif journalChouse == "7":
        #     print("7")
        # elif journalChouse == "8":
        #     print("8")
        # elif journalChouse == "9":
        #     print("9")4
        # elif journalChouse == "10":
        #     print("10")
        # elif journalChouse == "11":
        #     print("11")
        # elif journalChouse == "12":
        #     print("12")
        # elif journalChouse == "13":
        #     print("13")
        # elif journalChouse == "14":
        #     print("14")
        # elif journalChouse == "15":


        # 下载成功后，判断程序是否需要继续执行
        if not checknum:
            print("下载--失败：，失败原因：")
            # 询问是否需要继续使用
            switch = input("是否继续采集y/n?：")

            if switch=="n":
                # webbrowser
                break
            elif switch =="y":
                continue
            elif switch == "":
                print("未输入指示，程序结束")
                break
            else:
                print("输入指令错误，程序结束")
                break
        elif checknum:

            print("--------------下载完成--------------")
            print("　　　　　　　　　　　")
            # 询问是否需要继续使用
            switch = input("是否继续采集y/n?:")

            if switch == "n":
                break
            elif switch == "y":
                continue
            elif switch=="":
                print("未输入指示，程序结束")
                break
            else:
                print("输入指令错误，程序结束")
                break


if __name__ == "__main__":
    work()














