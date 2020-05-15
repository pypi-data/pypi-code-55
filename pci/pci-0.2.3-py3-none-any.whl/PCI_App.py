#!/usr/bin/env python3
# coding=gbk
from tkinter import N, S, E, W
from tkinter.filedialog import askopenfilename
import os
# from pci_pinggu import readbasicparams, loadbasicparams, writefile
#from enodebfunction import Cell_info, Cell_info_list, Cell_estimate
from pci.enodebfunction import Cell_info, Cell_info_list, Cell_estimate
import pandas as pd
import numpy as np
# import pickle
import folium
from folium.plugins import MeasureControl
from folium.plugins import Draw
import webbrowser
from webbrowser import Chrome
from pathlib import Path
from random import randint
import tkinter as tk
import _thread as thread

""" 
# 说明: # 根据输入的站点或经纬度，PCI值，评估该点在工参同PCI组的小区或基站的距离，依次获取最小距离
# 输入：
#    1. 同频工参
#    2. 待评估站点信息，包括PCI组号，经纬度
#    3. 启动Chrome浏览器 URI
# 输出：
#    1. 同PCI的周边站点（30km以内)，标注有距离
#    2. 地图，待评估点，搜索功能（探索）
"""

def writefile(filename:str, map:folium.Map)->"tuple(filepath,bool)":
    try:
        filepath = filename #已经改成了全路径
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print("Remove file:"+filepath)
        except:
            print("Failed to remove existing file")
        map.save(filepath)
        print("Path:", filepath)
        print("Saved map to file successfully!")
        return filepath, True
    except:
        print("writefile:Something wrong!")
        return filepath, False

# 手动导入工参表，第一次使用时需要读取工参. 会覆盖掉已有的工参
def readbasicparams(filename:"CSV filename with specified format", outfilename:"saveas temp file for the sake of speed"="sheet.pkl")->"Any":
    try:
        csvfilepath = filename
        print("csvfilepath:", csvfilepath)
        pklfilepath = os.path.join(os.getcwd(), outfilename)
        # if os.path.exists(pklfilepath):
        #     os.remove(pklfilepath)
        #     print("remove old file: " + outfilename)
        try:
            sheet = pd.read_csv(csvfilepath, encoding='gbk')
            print("read csv file.")
        except:
            sheet = pd.read_excel(csvfilepath, encoding="gbk")
            print("read excel file.")
        # print("shape:",sheet.shape)
        # with open(pklfilepath, "wb") as f:
        #     pickle.dump(sheet, f)
        #     print("pickle dump", pklfilepath)
        # print("readbasicparams: Load file successful")
        return pklfilepath, sheet
    except:
        # print("readbasicparams: Something wrong!")
        raise Exception("readbasicparams: Something wrong!")

#加载工参，计划用于已经导入一次工参之后重复利用
def loadbasicparams(filepath):
    try:
        # pklfilepath = os.getcwd() + "\\" + filename
        pklfilepath = os.path.join(os.getcwd(), filename )
        # if not os.path.exists(filepath):
        #     raise Exception("Basic params file does not exist!")
        # else:
        #     with open(filepath, "rb") as f:
        #         sheet = pickle.load(f)
        #         print("load basic params file success")
        # return sheet
    except:
        print("Basic parmas file does not exist!!")
        return None

class Config:
    def __init__(self):
        self.fp_basicparam = ""
        self.fp_initbrowser = ""
        # self.fp_initcsvfile = os.getcwd()+"\\"+"PCI_Group_estimate_outputfile.csv"
        self.fp_initcsvfile = os.path.join(os.getcwd(), "PCI_Group_estimate_outputfile.csv")
        self.htmlpath = ""
        self.cells = Cell_info_list(name="default")
        self.sheet = pd.DataFrame(data=None)

    def getinitcsvfile(self):
        return self.fp_initcsvfile

    def appendcell(self, cellobject):
        self.cells.append(cellobject)

    def getcells(self):
        return self.cells

    def gethtmlpath(self):
        return self.htmlpath
		
    def sethtmlpath(self, fp):
        self.htmlpath = fp

    def setsheet(self, df):
        self.sheet = df

    def getsheet(self):
        return self.sheet

    def setbasicparam(self, fp):
        self.fp_basicparam = fp

    def setinitbrowser(self, fp):
        self.fp_initbrowser = fp

    def getbasicparam(self):
        return self.fp_basicparam

    def getinitbrowser(self):
        return self.fp_initbrowser

class Application:
    def __init__(self, root=None):
        self.root = root
        self.config = Config()
        # super().__init__(root)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # self.emptymenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="", menu=self.emptymenu)

        self.fmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="文件", menu=self.fmenu)
        self.fmenu.add_command(label="导入工参", command=self.callback_importbasic)
        self.fmenu.add_separator()
        self.fmenu.add_command(label="设置默认浏览器(推荐谷歌)", command=self.callback_setbrowser)
        self.fmenu.add_separator()
        # self.fmenu.add_command(label="退出", command=root.quit())

        # self.hmenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="帮助", menu=self.hmenu)
        # self.hmenu.add_command(label="没有", command=self.callback_help)
        # self.hmenu.add_separator()

        self.frame = tk.Frame(master=root)
        self.frame.pack()
        self.frame_l = tk.Frame(master=self.frame)
        self.frame_l.grid(row=0, column=0, sticky=tk.N)
        self.frame_down = tk.Frame(master=self.frame)
        self.frame_down.grid(row=0, column=1, sticky=tk.N)

        self.label = tk.Label(master=self.frame_l, text=" 输入经纬度")
        self.label.grid(row=0, column=0, sticky=tk.W, pady=10)
        # v = StringVar(root, value='default text')
        # textvariable = v

        self.entry_loc = tk.Entry(master=self.frame_l)
        self.entry_loc.insert(tk.END, '23.1497,113.3206')
        self.entry_loc.grid(row=0, column=1, sticky=tk.W, pady=10)

        self.label2 = tk.Label(master=self.frame_l, text="输入PCI组号")
        self.label2.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.entry_pcig = tk.Entry(master=self.frame_l)
        self.entry_pcig.insert(tk.END, '输入范围: 0~167')
        self.entry_pcig.grid(row=2, column=1, sticky=tk.W, pady=10)

        self.outputmode = [("仅显示地图", 1), ("显示地图且保存为csv文件", 2)]
        self.value_rbtn = tk.IntVar()
        self.value_rbtn.set(1)
        for t, v in self.outputmode:
            self.rbtn = tk.Radiobutton(master=self.frame_l, text=t, variable=self.value_rbtn, value=v)
            self.rbtn.grid(row=4, column=v-1, sticky=tk.W, pady=10)

        self.btn_execute = tk.Button(master=self.frame_l, text="评估", command=self.callback_exe)
        self.btn_execute.grid(row=6, column=0, sticky=tk.W, pady=20)

    # def creatbasicdefinedFrame(self, columnsname)->"defined which column is lon, lat, pci, and etc.":
    #     subframe = Frame(self.root)



    def callback_importbasic_thread(self):
        for x in range(self.config.getsheet().shape[0]):
            try:
                r = self.config.getsheet().iloc[x, :]
                # print(r)
                cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
                                     lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'],
                                     cellname=r['cellname'])
                self.config.cells.append(cellinfo)
            except:
                # print("Something wrong when building cell object!")
                print("Please check your input item:", r)
                # pass


    def callback_importbasic(self):
        """"读取工参文件，并保存为副本方便使用"""
        print("Callback import basic")
        file_path = askopenfilename(title="选择指定格式的工参文件",
                                  filetypes=[('csv', "*.csv"),('Excel', "*.xlsx"), ("All Files", "*")],
                                  initialdir=os.getcwd())
        outfilepath, sheet = readbasicparams(file_path)
        # 读取工参，指定选框
        # print("工参预览：\n", sheet.head(n=5))
        # print("列名：\n", sheet.columns.values)

        self.config.setbasicparam(outfilepath)
        self.config.setsheet(sheet)
        print("start build cell info list!")
        for x in range(self.config.getsheet().shape[0]):
            try:
                r = self.config.getsheet().iloc[x, :]
                # print(r)
                cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
                                     lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'],
                                     cellname=r['cellname'])
                self.config.cells.append(cellinfo)
            except:
                # print("Something wrong when building cell object!")
                print("Please check your input item:", r)
                pass
        print("Finished import basic params")



    def callback_setbrowser(self):
        print("Callback setting browser")
        file_path = askopenfilename(title="选择浏览器启动文件（推荐设置为谷歌）",
                                    filetypes=[("exe","*exe")],
                                    initialdir=os.getcwd())
        self.config.setinitbrowser(file_path)
        #保存浏览器启动文件到指定文件
        print("Finished setting browser")

    def callback_help(self):
        print("Callback help doc")

    def callback_exe(self):
        print("Callback execute!")
        # print("loc:", self.entry_loc.get())
        # print("pcig", self.entry_pcig.get())
        # print("rbtn", self.value_rbtn.get())
        # 读取输入信息
        try:
            pcig = self.entry_pcig.get()
            pcig = int(pcig.strip())
            # print(type(pcig))
            loc = self.entry_loc.get()
            loc = tuple(map(lambda x: float(x.strip()), loc.split(",")))
            # print(loc)
            # print(type(loc))
            # print((loc[0], loc[1]))
            mode = self.value_rbtn.get()
            params = {"pcig":pcig,"loc":loc,"mode":mode}  #参数
            print("输入参数：", params)
            if (params['pcig'] not in range(0, 168)) or (params['loc'][0] < -90) or \
                    (params['loc'][0] > 90) or (params['loc'][1] < -180) or (params['loc'][1] > 180):
                raise Exception()
        except:
            print("Invalid input parameters!")
            # raise Exception()
            return None


        # step1 读取工参,构建工参对象
    # try:
    #     print("basic params",self.config.getbasicparam())
    #     sheet = loadbasicparams(self.config.getbasicparam())
    #     sheet = self.config.getsheet()
        # ValueError: The truth value of a DataFrame is ambiguous.Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # if not sheet:
        #     print("未导入读取工参")

        # 这一段不应该存在的，因为导入数据不会有频率字段，这里是为了调试方便
        # freq = '800M'  # 筛出800M小区
        # cell = sheet.loc[sheet["frequency"] == freq]

        cell = self.config.getsheet()
        if not cell.shape[0]:
            print("Empty basic parameters!")
            # raise Exception()
            return None

        # 构建小区工参对象
        # version 0.1.1已优化处理，在第一次导入参数时创建了
        # cells = Cell_info_list(name="default")
        # for x in range(cell.shape[0]):
        #     try:
        #         r = cell.iloc[x, :]
        #         # print(r)
        #         cellinfo = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']),
        #                 lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'], cellname=r['cellname'])
        #         cells.append(cellinfo)
        #     except:
        #         print("something wrong when building cellinfo list!")
        #         pass


        # step2 构建待评估点对象
        try:
            cell_esti = Cell_estimate(pcig=params['pcig'], loc=params['loc'], eci="XXXXX")  # type: object
            # cell_esti.getecidist(self.config.getcells()) #暂时用不到
            cell_esti.getaroudcell(self.config.getcells())
        except:
            print("Failed to building estimate point object!")
            # raise Exception()
            return None


        # Step3 生成地图
        try:
            disp = folium.Map(location=cell_esti.getloc(), zoom_start=11, control_scale=True)
            featuregroup = folium.FeatureGroup(name="周边站点")
            featuregroup_esti = folium.FeatureGroup(name="待评估点")
            estimatepoint = folium.Marker(location=cell_esti.getloc(),
                                          icon=folium.Icon(color='red', icon="home", angle=0),
                                          popup=folium.Popup(html=cell_esti.getcellinfo(), max_width=2000, show=True))
            estimatepoint.add_to(featuregroup_esti)
            featuregroup.add_to(disp)
            featuregroup_esti.add_to(disp)
            for aroudcell in cell_esti:
                # 为了可以在地图上明显地看到重叠站点，对位置信息增加了随机偏移，但是弹窗显示的经纬度是正确的
                # 第二版的偏移量不是随机了，而是根据扇区：第一扇区位置不改动，第二扇区经度增加，纬度减小；第三扇区经度和纬度均减小
                marker = folium.Marker(location=aroudcell.getlocwithoffset(alpha=1e-3),
                                       popup=folium.Popup(html=aroudcell.getcellinfo(), max_width=2000),
                                   icon=folium.Icon(color="green", icon="arrow-up", angle=aroudcell.getangle()))
                marker.add_to(featuregroup)
            folium.LayerControl().add_to(disp)
            # folium.LatLngPopup().add_to(disp)
            # folium.ClickForMarker(popup=None).add_to(disp)
            MeasureControl(position='topleft', activeColor="#FF0000", completedColor="#000000").add_to(disp)
            Draw(export=True, filename="XXXXXX.geojson", position="topleft", draw_options={'polyline': {'allowIntersection': False}}, edit_options={'poly': {'allowIntersection': False}}).add_to(disp)

            # 保存文件并打开
            # disp.save("demo.html", close_file=False)
            # 设置map保存路径
            #self.config.sethtmlpath(os.getcwd() + "\\" + "demo.html")
            self.config.sethtmlpath(os.path.join(os.getcwd(), "demo.html"))

            print(self.config.gethtmlpath())
            filepath, _ = writefile(self.config.gethtmlpath(), disp)
            print(filepath)
        except:
            print("Failed to create map file!")
            # raise Exception()
            return None

        # Step4:（1)指定浏览器，Chrome，（2）默认浏览器，通常是IE
        opensuccess = False
        if self.config.getinitbrowser():
            browser_path = self.config.getinitbrowser()
            webbrowser.register("User_defined", None, webbrowser.BackgroundBrowser(browser_path))
            webbrowser.get("User_defined").open(self.config.gethtmlpath(), new=1, autoraise=True)
            opensuccess = True
        else:
            webbrowser.open(self.config.gethtmlpath())
        #     webbrowser.register("chrome", Chrome('chrome'))
        #     webbrowser.open("demo.html")
        #     opensuccess = True
        # if not opensuccess:
        #     webbrowser.open("demo.html")

        # Step5: 保存结果文件
        if mode == 1:
            print("Do not need to save csv file")
        elif mode == 2:
            # output = pd.DataFrame(data=np.random.rand(16).reshape((2,-1)))
            # output.to_csv("outputfile.csv")
            cell_esti.savefile(self.config.getinitcsvfile())
            print("Saved csv file:", self.config.getinitcsvfile())

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200+10+10")
    root.title("PCI@广东电信综维优中心片区 Version0.2.1")
    root.minsize(400, 200)
    app = Application(root)
    root.mainloop()
