import re
import sqlite3

class env_C2960L:
    def __init__(self,file):
        db = sqlite3.connect('env_pmdb')
        self.file = file
        read_file = open(self.file,'r')
        #print(read_file)
        read_file_list  = read_file.readlines()
        #print(read_file_list)
        list_psu_capture = []
        list_fan = ['-']
        list_fan_cond_cp = ['-']
        list_temp = []
        list_temp_cond = []
        list_psu = []
        list_psu_cond = []
        psu_line_start = 0
        psu_line_end = 0
        count_line=0
        for i in read_file_list:
            if re.findall('^hostname (.*)',i):
                regex_devicename = re.findall('^hostname (.*)',i)
                devicename = regex_devicename[0]
                #print(devicename)
            if re.findall('^.*SYSTEM (TEMPERATURE) is .*',i):
                regex_temp = re.findall('^.*SYSTEM (TEMPERATURE) is .*',i)
                temp = regex_temp[0]
                list_temp.append(temp)
                #print(temp)
            if re.findall('^.*SYSTEM TEMPERATURE is (.*)', i):
                regex_temp_cond = re.findall('^.*SYSTEM TEMPERATURE is (.*)', i)
                temp_cond = regex_temp_cond[0]
                list_temp_cond.append(temp_cond)
                #print(temp_cond)
            if re.findall('^.*PID: (Built-in)',i):
                regex_psu = re.findall('^.*PID: (Built-in)',i)
                psu = regex_psu[0]
                list_psu.append(psu)
                #print(temp)
            if re.findall('^.*Power Supply Status: (.*)', i):
                regex_psu_cond = re.findall('^.*Power Supply Status: (.*)', i)
                psu_cond = regex_psu_cond[0]
                list_psu_cond.append(psu_cond)
                #print(temp_cond)
        print('device '+devicename)
        print(list_fan)
        print(list_fan_cond_cp)
        print(list_temp)
        print(list_temp_cond)
        print(list_psu)
        print(list_psu_cond)
        

        #connect DB
        cursor = db.cursor()
        count_sql = 0
        for psu in list_psu:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Power Supply',psu,list_psu_cond[count_sql],))
            count_sql+=1

        count_sql = 0
        for fan in list_fan:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Fan',fan,list_fan_cond_cp[count_sql],))
            count_sql+=1

        count_sql = 0
        for temp in list_temp:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                      VALUES(?,?,?,?)''', (devicename,'Temperature',temp,list_temp_cond[count_sql],))
            count_sql+=1

        db.commit()             
        db.close()
       

