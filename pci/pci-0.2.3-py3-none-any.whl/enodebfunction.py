#!/usr/bin/env python3

from geopy.distance import great_circle
from random import randint, choice
import numpy as np
import pandas as pd

# 基站对象, 这里用来存放一个外部邻区表
class Enodeb:
    def __init__(self, *, enodebid:int, city:str =""):
        self.enodebid = enodebid
        self.city = city
#         extcell = {} #外部邻区的 eci
        self.externalcelleci = set() #保存外部邻区的 eci：放在这里的原因是想维持一个外部邻区表映射  本站enodebid -> 外部邻区eci
    def getlat(self) ->float:
        return self.latitude
    
    def getlon(self) ->float:
        return self.longitude

    def getloc(self)->"(lattitude, longitude)":
        return (self.latitude, self.longitude)
    
    def getenodebid(self) ->int:
        return self.enodebid
    
    def showproperties(self) ->None:
        print("Enodeb Ojbect")
        print("1. enodebid: "+str(self.enodebid))
        print("2. city: "+str(self.city))
        print("3. externalcelleci: " + str(self.externalcelleci))
     
# #添加外部小区ECI
    def appendexternalcelleci(self, eci:int) ->None:
        self.externalcelleci = self.externalcelleci.union(eci)


#小区对象列表，用于存放公参对象 
class Cell_info_list:
	def __init__(self, name="cellinfolist_default"):
		self.name = name
		self.info_list = []

	def append(self, cell_info):
		self.info_list.append(cell_info)
		
	def __getitem__(self, idx):
		return self.info_list[idx]

class Iter_Cell_estimate:
    def __init__(self, cells):
        self.stop = len(cells)
        self.cur = 0
        self.cells = cells
        # print("params:", self.stop, type(self.cells))
        # print("Iter_Cell_estimate __Init__")

    def __next__(self):
        if self.cur == self.stop:
            # print("StopIteration")
            raise StopIteration
        else:
            ret = self.cells[self.cur]
            # print("Next:", ret)
            self.cur += 1
        return ret

class Cell_estimate(Cell_info_list):
    def __init__(self, pcig:"pci group", loc: tuple, *, eci=None):
        self._pcig = pcig
        self._loc = loc
        self._eci = eci
        self._aroudcell_dist = {}
        self._aroudcell = []

    def __len__(self):
        # print("Cell_estimate: __len__")
        return len(self._aroudcell)

    def __iter__(self):
        # print("Cell_estimate: __iter__")
        return Iter_Cell_estimate(self._aroudcell)

    # def __getitem__(self, idx):
    #     print("*****************", idx)
    #     return self._aroudcell[idx]

    def savefile(self, outfilename="PCI_Group_estimate_outputfile.csv"):
        # lst = [self.city, self.enodebid, self.cellid, self.eci, self.cellname,
               # self.pci, self.longitude, self.latitude, self.getdist()]
        """主要步骤：将list转成pandas.dataframe
        输出同PCI组号的小区顺序，次序依照距离从近到远排列
        """
        rows = len(self._aroudcell)
        if rows == 0:
            print("empty file!")
            return False
        else:
            columnname = self._aroudcell[0].getcolumnsname()
        df = pd.DataFrame(data=None, index=range(0, rows), columns=columnname)

        for idx, cell in enumerate(self._aroudcell):
            df.iloc[idx,:] = cell.getlist()
            # print("saveing now")
        df.sort_values(by=columnname[-1], ascending=True).to_csv(outfilename, encoding='gbk', index=False)


    def getpcigroup(self):
        return self._pcig

    def geteci(self):
        return self._eci

    def getloc(self):
        return self._loc

    def getecidist(self, cells:"工参", largestdist:"1w km"=10000000)->"dictionary, eci:distance":
        if self._aroudcell_dist:
            return self._aroudcell_dist
        for cell in cells:
            if self._pcig == cell.getpcigroup():
                dist = round(great_circle(self.getloc(), cell.getloc()).meters)
                if dist == 0 and dist > largestdist: #除了本身和超过30km的都不记录
                    continue
                self._aroudcell_dist.update({cell.geteci():dist})
        return self._aroudcell_dist

    def getaroudcell(self, cells:"工参", largestdist:"1w km"=10000000)->"Cell_info object list which containing distance":
        if self._aroudcell:
            return self._aroudcell
        for cell in cells:
            if self._pcig == cell.getpcigroup():
                dist = round(great_circle(self.getloc(), cell.getloc()).meters)
                if dist > largestdist:
                    continue
                cell.setdist(dist)
                self._aroudcell.append(cell)
        return self._aroudcell

    def getcellinfo(self)->str:
        s = ''
        s += "待评估站点基本信息</br>"
        s += "<b>PCI group: "+str(self.getpcigroup())+"</b></br>"
        s += "Loc: "+str(self.getloc())+"</br>"
        return s

# 小区对象,用于存放公参
class Cell_info(Enodeb):
    def __init__(self, *, enodebid:int, cellid:int, pci:int, lon:float, lat:float, city:str ='', cellname:str ='') ->None:
        self.enodebid = enodebid
        self.cellid = cellid
        self.pci = pci
        self.longitude = lon
        self.latitude = lat
        self.eci = self.enodebid*256 + self.cellid
        self.city = city
        self.cellname = cellname
#         extcell = {} #dictionary external eci -> pci,  save external cell and corresponding pci

    def getcolumnsname(self):
        # columns = ["city", "enodebid", "cellid", "eci", "cellname", "pci", "latitude", "longitude", "distance"]
        columns = ["城市", "基站ID", "小区ID", "ECI", "小区名", "物理小区标识-PCI", "纬度", "经度", "与评估点的距离(米)"]
        return columns

    def getlist(self):
        lst = [self.city, self.enodebid, self.cellid, self.eci, self.cellname,
               self.pci, self.latitude, self.longitude, self.getdist()]
        return lst

    def getangle(self)->int:
        """根据PCI获取小区的方向角, 从第一方向角起依次为0，120，240；如果pci不存在，则设为15"""
        angles = [0, 120, 240, 15]
        pci = self.getpci()
        if pci:
            angle = angles[pci%3]
        else:
            angle = angles[-1]
        return angle

    def getcellinfo(self)->str:
        s = ""
        try:
            s += "<b>Dist: "+str(self.getdist())+"米</b></br>"
        except:
            pass
        s += "Enodebid: "+str(self.enodebid)+"</br>"
        s += "Cellid: "+str(self.cellid)+"</br>"
        s += "ECI: "+str(self.eci)+"</br>"
        s += "Cellname: "+str(self.cellname)+"</br>"
        s += "City: "+str(self.city)+"</br>"
        s += "<b>PCI group: "+str(self.getpcigroup())+"</b></br>"
        s += "PCI: "+str(self.getpci())+"</br>"
        s += "Loc: "+str(self.getloc())+"</br>"
        return s

    def getlocwithoffset(self, alpha=1e-4):
        offsets = [(0, 0), (-1*alpha, 1*alpha), (-1*alpha, -1*alpha)]
        if self.getpci():
            sel = self.getpci() % 3
            offset = offsets[sel]
        else:
            offset = (choice([-1,1])*alpha*randint(5,15), choice([-1,1])*alpha*randint(5,15))
        loc = self.getloc()
        return tuple(map(lambda x, y: x + y, loc, offset))

    def geteci(self):
        return self.eci

    def getpci(self):
        return self.pci
    
    def getpcigroup(self):
        return self.pci//3
		
#    def getlocbyeci(self, eci):
#        if self.geteci() == eci:
#		return self.getloc()
#        else:
#		return None

    def setdist(self, dist): #动态添加距离其他点的距离信息
        self._dist = dist

    def getdist(self): # 和setdist(self, dist)方法配套
        return self._dist
            
    def showproperties(self):
        print("Cell_info Ojbect")
        print("1. City: "+ str(self.city))
        print("2. Cell Name: "+str(self.cellname))
        print("3. ECI: "+ str(self.eci))
        print("4. EnodeB ID: " + str(self.enodebid))
        print("5. Cell ID: "+ str(self.cellid))
        print("6. (Latitude, Longitude): (" + str(self.latitude) + ", " + str(self.longitude) + ")")
        print("7. PCI: " + str(self.pci))
        # print("8. List extcell: " + str(self.extcell))

# 问题小区对象
class Cell_prob(Enodeb):
    def __init__(self, *, enodebid:int, cellid:int, pci:int, \
                 lon:float, lat:float, city:str = "" , cellname:str ="") ->None:
        self.enodebid = enodebid
        self.cellid = cellid
        self.pci = pci
        self.longitude = lon
        self.latitude = lat
        self.eci = self.enodebid*256 + self.cellid
        self.city = city
        self.cellname = cellname
        self.withinx = set() # save cell's within x km
        self.nearby = set() #save around cell's eci, both including cells withinx km and it's external cell
        self.pci_used = set() #pci corresponding nearby cells
        #self.pcigroup_remained = {} # pcigroup: latest distance
		#self.estimate = [] # PCI组

    def getwithinx(self):
        return self.withinx

    def getnearby(self):
        return self.nearby

    def geteci(self):
        return self.eci
        
    def showproperties(self):
        print("Cell_prob Ojbect")
        print("1. City: "+ str(self.city))
        print("2. Cell Name: "+str(self.cellname))
        print("3. ECI: "+ str(self.eci))
        print("4. EnodeB ID: " + str(self.enodebid))
        print("5. Cell ID: "+ str(self.cellid))
        print("6. (Latitude, Longitude): (" + str(self.latitude) + ", " + str(self.longitude) + ")")
        print("7. PCI: " + str(self.pci))
        print("8. List withinx: " + str(self.withinx))
        print("9. List nearby: " + str(self.nearby))
        print("10. List pci_used: " + str(self.pci_used)) 
    
    def appendcellwithinx(self, other, dist:"default: within 3000m"=3000) -> bool:
#         如果传入的工参小区对象ohter 是问题小区对象self小区周边 x km内，
#         如果withinx内还没有other的eci, 则添加到withinx字典内，并返回True
#         great_circle(newport_ri, cleveland_oh).meters
        point1 = (Enodeb.getlat(self), Enodeb.getlon(self))
        point2 = (Enodeb.getlat(other),Enodeb.getlon(other))
#         print("point1: " + str(point1))
#         print("point2: " + str(point2))
        juli = great_circle(point1, point2).meters
#         print("juli: " + str(juli))
        if juli <= dist:
            self.withinx.add(other.eci)                    
            return True
        else:
            return False
        
    def appendcellnearby(self, eecell:"ojbect list") ->None:
#         根据self.withinx内的每一个eci -> enodebid -> 外部邻区(eci, pci)
        enb = set()
        [enb.add(eci//256) for eci in self.withinx]
#         enb = [x for x in self.withinx]
        for enb_id in enb:
            for site in eecell:
#                 print(site.getenodebid())
                if site.getenodebid() == enb_id:
                    self.nearby.update(site.externalcelleci)

    def appendpci(self, eci_pci:dict) ->None:
        for eci in self.nearby:
            if eci_pci.get(eci):
                self.pci_used.add(eci_pci[eci])
                
    def getpcigroup_remained(self) ->set:
        total = set(range(0,168))
        used = set([p//3 for p in self.pci_used])
        remained = total - used
        #self.pcigroup_remained = remained
        return remained

    def getlatestdist(self, pcigroup:"PCI组号", cell_list:"同频小区工参列表", largestdist=30000)->"最近的距离":
        dist_lst = []
        for cell in cell_list:
            if pcigroup == cell.getpcigroup():
                dist = great_circle(self.getloc(), cell.getloc()).meters
                dist = round(dist)
                if dist == 0 and dist > largestdist: #除了本身和超过30km的都不记录
                    continue
                dist_lst.append(dist)
        return min(dist_lst)

    def getlatestdist_eachpcig(self, cell_list:"同频小区工参列表")->"{预留PCI组:最近距离}":
        dist_dict = {}
        for pcig in self.getpcigroup_remained():
            min_dist = self.getlatestdist(pcig, cell_list)
            dist_dict.update({pcig:min_dist})
        return dist_dict


if __name__ == "__main__":
    print("test part")
    import pandas as pd

    cellparam_pathfile = "中山L网工参2019-12-24(1).xlsx"
    sheet = pd.read_excel(cellparam_pathfile, sheet_name="cell", header=0)
    # 筛出800M小区
    cell = sheet.loc[sheet["frequency"] == '800M']
    print(cell.shape)
    cell.head()

    # 小区工参对象 List
    cell_list = Cell_info_list(name="L800M小区工参")
    for x in range(cell.shape[0]):
        r = cell.iloc[x, :]
        cellobject = Cell_info(enodebid=int(r['enodebid']), cellid=int(r['cellid']), pci=int(r['pci']), \
                               lon=float(r['longitude']), lat=float(r['latitude']), city=r['city'],
                               cellname=r['cellname'])
        cell_list.append(cellobject)

    cella = Cell_prob(enodebid=507530, cellid=18, pci=2, lon=113.25, lat=22.5949, city='ZS')
    cellb = Cell_prob(enodebid=504095, cellid=21, pci=2, lon=113.233,lat=22.5949, city='ZS')

    min_dist_a = cella.getlatestdist(3, cell_list)
    min_dist_b = cellb.getlatestdist(3, cell_list)
    print("min_dist:",min_dist_a, min_dist_b, min(min_dist_a,min_dist_b))