import sqlite3
import re

from netoprmgr.device_templates.cisco.cisco_None import cisco_None
from netoprmgr.device_templates.cisco.cisco_1905 import cisco_1905
from netoprmgr.device_templates.cisco.cisco_1921 import cisco_1921
from netoprmgr.device_templates.cisco.cisco_1941 import cisco_1941
from netoprmgr.device_templates.cisco.cisco_2801 import cisco_2801
from netoprmgr.device_templates.cisco.cisco_2811 import cisco_2811
from netoprmgr.device_templates.cisco.cisco_2821 import cisco_2821
from netoprmgr.device_templates.cisco.cisco_2901 import cisco_2901
from netoprmgr.device_templates.cisco.cisco_2911 import cisco_2911
from netoprmgr.device_templates.cisco.cisco_C3750X import cisco_C3750X
from netoprmgr.device_templates.cisco.cisco_C4500X import cisco_C4500X
from netoprmgr.device_templates.cisco.cisco_C4506 import cisco_C4506
from netoprmgr.device_templates.cisco.cisco_C4507R import cisco_C4507R
from netoprmgr.device_templates.cisco.cisco_C4507RE import cisco_C4507RE
from netoprmgr.device_templates.cisco.cisco_C4900M import cisco_C4900M
from netoprmgr.device_templates.cisco.cisco_C6504 import cisco_C6504
from netoprmgr.device_templates.cisco.cisco_C6506 import cisco_C6506
from netoprmgr.device_templates.cisco.cisco_C2960 import cisco_C2960
from netoprmgr.device_templates.cisco.cisco_C2960C import cisco_C2960C
from netoprmgr.device_templates.cisco.cisco_C2960CX import cisco_C2960CX
from netoprmgr.device_templates.cisco.cisco_C2960L import cisco_C2960L
from netoprmgr.device_templates.cisco.cisco_C2960S import cisco_C2960S
from netoprmgr.device_templates.cisco.cisco_C2960X import cisco_C2960X
from netoprmgr.device_templates.cisco.cisco_C2960XR import cisco_C2960XR
from netoprmgr.device_templates.cisco.cisco_C3560 import cisco_C3560
from netoprmgr.device_templates.cisco.cisco_C3560C import cisco_C3560C
from netoprmgr.device_templates.cisco.cisco_C3560CG import cisco_C3560CG
from netoprmgr.device_templates.cisco.cisco_C3560CX import cisco_C3560CX
from netoprmgr.device_templates.cisco.cisco_C3560G import cisco_C3560G
from netoprmgr.device_templates.cisco.cisco_C3560V2 import cisco_C3560V2
from netoprmgr.device_templates.cisco.cisco_C3560X import cisco_C3560X
from netoprmgr.device_templates.cisco.cisco_C3650 import cisco_C3650
from netoprmgr.device_templates.cisco.cisco_C3750 import cisco_C3750
from netoprmgr.device_templates.cisco.cisco_C3750E import cisco_C3750E
from netoprmgr.device_templates.cisco.cisco_C3750G import cisco_C3750G
from netoprmgr.device_templates.cisco.cisco_C3750V2 import cisco_C3750V2
from netoprmgr.device_templates.cisco.cisco_C3850P import cisco_C3850P
from netoprmgr.device_templates.cisco.cisco_C3850S import cisco_C3850S
from netoprmgr.device_templates.cisco.cisco_C3850T import cisco_C3850T
from netoprmgr.device_templates.cisco.cisco_C3850TS import cisco_C3850TS
from netoprmgr.device_templates.cisco.cisco_C3850XS import cisco_C3850XS
from netoprmgr.device_templates.cisco.cisco_C6509 import cisco_C6509
from netoprmgr.device_templates.cisco.cisco_C6513 import cisco_C6513
from netoprmgr.device_templates.cisco.cisco_C6807 import cisco_C6807
from netoprmgr.device_templates.cisco.cisco_C6880 import cisco_C6880
from netoprmgr.device_templates.cisco.cisco_C9200L import cisco_C9200L
from netoprmgr.device_templates.cisco.cisco_C9300 import cisco_C9300
from netoprmgr.device_templates.cisco.cisco_C9500 import cisco_C9500
from netoprmgr.device_templates.cisco.cisco_2921 import cisco_2921
from netoprmgr.device_templates.cisco.cisco_2951 import cisco_2951
from netoprmgr.device_templates.cisco.cisco_3825 import cisco_3825
from netoprmgr.device_templates.cisco.cisco_3845 import cisco_3845
from netoprmgr.device_templates.cisco.cisco_3925 import cisco_3925
from netoprmgr.device_templates.cisco.cisco_3945 import cisco_3945
from netoprmgr.device_templates.cisco.cisco_ASA5505 import cisco_ASA5505
from netoprmgr.device_templates.cisco.cisco_ASA5508 import cisco_ASA5508
from netoprmgr.device_templates.cisco.cisco_ASA5512 import cisco_ASA5512
from netoprmgr.device_templates.cisco.cisco_ASA5515 import cisco_ASA5515
from netoprmgr.device_templates.cisco.cisco_ASA5520 import cisco_ASA5520
from netoprmgr.device_templates.cisco.cisco_ISR4451 import cisco_ISR4451
from netoprmgr.device_templates.cisco.cisco_ISR4331 import cisco_ISR4331
from netoprmgr.device_templates.cisco.cisco_ISR4351 import cisco_ISR4351
from netoprmgr.device_templates.cisco.cisco_ISR4321 import cisco_ISR4321
from netoprmgr.device_templates.cisco.cisco_ASR1002 import cisco_ASR1002

class new_file_identification:
    def __init__(self,files):
        self.files=files

    def new_file_identification(self):
        #destroy table summarytable
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE swsumtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE swtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE hwsumtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE hwcardtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE cpusumtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE memsumtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE envtable''')
            db.commit()
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE logtable''')
            db.commit()
            db.close()
        except:
            pass
        #open db connection to table summary table
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE swsumtable(id INTEGER PRIMARY KEY, version TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE swtable(id INTEGER PRIMARY KEY, devicename TEXT,
                model TEXT, iosversion TEXT, uptime TEXT, confreg TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE hwsumtable(id INTEGER PRIMARY KEY, model TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE hwcardtable(id INTEGER PRIMARY KEY, devicename TEXT,
                model TEXT, card TEXT, slot TEXT, sn TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE cpusumtable(id INTEGER PRIMARY KEY, devicename TEXT,
                model TEXT, total TEXT, process TEXT, interrupt TEXT, status TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE memsumtable(id INTEGER PRIMARY KEY, devicename TEXT,
                model TEXT, utils TEXT, topproc TEXT, status TEXT)                    
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE envtable(id INTEGER PRIMARY KEY, devicename TEXT,
                                system TEXT, item TEXT, status TEXT)
            ''')
            db.close()
        except:
            pass
        try:
            db = sqlite3.connect('pmdb')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE logtable(id INTEGER PRIMARY KEY, devicename TEXT, model TEXT, script TEXT)
            ''')
            db.close()
        except:
            pass

        for file in self.files:
            try:
                print('')
                print('Processing File :')
                print(file)
                try:
                    read_file = open(file, 'r')
                    read_file_list = read_file.readlines()
                except:
                    read_file = open(file, 'r', encoding='latin-1')
                    read_file_list = read_file.readlines()
                
                for i in read_file_list:
                    if re.findall('.*PID:.*C3750X',i):
                        print('Execute cisco_C3750X')
                        cisco_C3750X(file)
                        xcek='disable'
                        break
                    elif re.findall('.*DESCR:.*C4500X',i):
                        print('Execute cisco_C4500X')
                        cisco_C4500X(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C4506',i):
                        print('Execute cisco_C4506')
                        cisco_C4506(file)
                        xcek='disable'
                        break
                    elif re.findall('^PID:\s+\S+4507R[+]E',i):
                        print('Execute cisco_C4507RE')
                        cisco_C4507RE(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C4507R',i):
                        print('Execute cisco_C4507R')
                        cisco_C4507R(file)
                        xcek='disable'
                        break
                    elif re.findall('.*DESCR:.*C4900M',i):
                        print('Execute cisco_C4900M')
                        cisco_C4900M(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6504',i):
                        print('Execute cisco_C6504')
                        cisco_C6504(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6506',i):
                        print('Execute cisco_C6506')
                        cisco_C6506(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960CX-\d+PC-L',i):
                        print ('Executing with C2960CX')
                        cisco_C2960CX(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960C-\d+\S+-L',i):
                        print ('Executing with C2960C')
                        cisco_C2960C(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960L-\d+TS-LL',i):
                        print ('Executing with C2960L')
                        cisco_C2960L(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960S-\d+TD-L',i):
                        print ('Executing with C2960S')
                        cisco_C2960S(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960XR-\d+TS-I',i):
                        print ('Executing with C2960XR')
                        cisco_C2960XR(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960X-\d+LPS-L',i):
                        print ('Executing with C2960X')
                        cisco_C2960X(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+2960',i):
                        print ('Executing with C2960')
                        cisco_C2960(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560CG-\d+TC-S',i):
                        print ('Executing with C3560CG')
                        cisco_C3560CG(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560CX-\d+PC-S',i):
                        print ('Executing with C3560CX')
                        cisco_C3560CX(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560C-\d+PC-S',i):
                        print ('Executing with C3560C')
                        cisco_C3560C(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560G-\d+PS-S',i):
                        print ('Executing with C3560G')
                        cisco_C3560G(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560V2-\d+PS-S',i):
                        print ('Executing with C3560V2')
                        cisco_C3560V2(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560X-\d+P-S',i):
                        print ('Executing with C3560X')
                        cisco_C3560X(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3560-\d+PS-S',i):
                        print ('Executing with C3560')
                        cisco_C3560(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+C3650-\d+',i):
                        print ('Executing with C3650')
                        cisco_C3650(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3750E-\d+TD-S',i):
                        print ('Executing with C3750E')
                        cisco_C3750E(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3750G-\d+TS-S\d+U',i):
                        print ('Executing with C3750G')
                        cisco_C3750G(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3750V2-\d+PS-S',i):
                        print ('Executing with C3750V2')
                        cisco_C3750V2(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3850-\d+P',i):
                        print ('Executing with C3850P')
                        cisco_C3850P(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3850-\d+S',i):
                        print ('Executing with C3850S')
                        cisco_C3850S(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3850-\d+T-S',i):
                        print ('Executing with C3850TS')
                        cisco_C3850TS(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3850-\d+T',i):
                        print ('Executing with C3850T')
                        cisco_C3850T(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+\S+3850-\d+XS',i):
                        print ('Executing with C3850XS')
                        cisco_C3850XS(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6509',i):
                        print('Executing with C6509')
                        cisco_C6509(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6513',i):
                        print('Executing with C6513')
                        cisco_C6513(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6807',i):
                        print('Executing with C6807')
                        cisco_C6807(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C6880',i):
                        print('Executing with C6880')
                        cisco_C6880(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C9200L',i):
                        print('Executing with C9200L')
                        cisco_C9200L(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C9300',i):
                        print('Executing with C9300')
                        cisco_C9300(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*C9500',i):
                        print('Executing with C9500')
                        cisco_C9500(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO2921',i):
                        print('Executing with CISCO2921')
                        cisco_2921(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO2951',i):
                        print('Executing with CISCO2951')
                        cisco_2951(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO3825',i):
                        print('Executing with CISCO3825')
                        cisco_3825(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO3845',i):
                        print('Executing with CISCO3845')
                        cisco_3845(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO3925',i):
                        print('Executing with CISCO3925')
                        cisco_3925(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*CISCO3945',i):
                        print('Executing with CISCO3945')
                        cisco_3945(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASA5505',i):
                        print('Executing with ASA5505')
                        cisco_ASA5505(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASA5508',i):
                        print('Executing with ASA5508')
                        cisco_ASA5508(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO1905',i):
                        print('Executing with 1905')
                        cisco_1905(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO1921',i):
                        print('Executing with 1921')
                        cisco_1921(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO1941',i):
                        print('Executing with 1941')
                        cisco_1941(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO2801',i):
                        print('Executing with 2801')
                        cisco_2801(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO2811',i):
                        print('Executing with 2811')
                        cisco_2811(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO2821',i):
                        print('Executing with 2821')
                        cisco_2821(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO2901',i):
                        print('Executing with 2901')
                        cisco_2901(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:\s+CISCO2911',i):
                        print('Executing with 2911')
                        cisco_2911(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASA5512',i):
                        print('Executing with ASA5512')
                        cisco_ASA5512(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASA5515',i):
                        print('Executing with ASA5515')
                        cisco_ASA5515(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASA5520',i):
                        print('Executing with ASA5520')
                        cisco_ASA5520(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ISR4451',i):
                        print('Executing with ISR4451')
                        cisco_ISR4451(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ISR4331',i):
                        print('Executing with ISR4331')
                        cisco_ISR4331(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ISR4351',i):
                        print('Executing with ISR4351')
                        cisco_ISR4351(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ISR4321',i):
                        print('Executing with ISR4321')
                        cisco_ISR4321(file)
                        xcek='disable'
                        break
                    elif re.findall('.*PID:.*ASR1002',i):
                        print('Executing with ASR1002')
                        cisco_ASR1002(file)
                        xcek='disable'
                        break
                    
                    else:
                        xcek='enable'
                    
                if xcek=='enable':
                    print('Executing None')
                    cisco_None(file)
                    
            #except NameError:
                #raise
            except:
                pass
