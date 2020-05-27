import sqlite3
import re



class cisco_3945:
    def __init__(self,file):
        #variable constructor
        self.file = file
        #read all things in file
        read_file = open(self.file,'r')
        read_file_list  = read_file.readlines()
        for line in read_file_list:
            #SOFTWARE TABLE
            #get device name
            if re.findall('^hostname (.*)',line):
                devicename = re.findall('^hostname (.*)',line)
                devicename = devicename[0]
            #get device model
            elif re.findall('Cisco\s+(\S+)\s+.*with\s+\S+\s+bytes\s+\S+\s+memory',line):
                model = re.findall('Cisco\s+(\S+)\s+.*with\s+\S+\s+bytes\s+\S+\s+memory',line)
                model = model[0]                
            #get ios version
            elif re.findall('^System image file is "(.*)"',line):
                iosversion = re.findall('^System image file is "(.*)"',line)
                iosversion = iosversion[0]
            #get uptime
            elif re.findall('^.*uptime is (.*)',line):
                uptime = re.findall('^.*uptime is (.*)',line)
                uptime = uptime[0]
            #get configuration register
            elif re.findall('^Configuration register is (.*)',line):
                confreg = re.findall('^Configuration register is (.*)',line)
                confreg = confreg[0]
            #SOFTWARE TABLE SUMMARY
            elif re.findall('^Cisco IOS.*, C3900.*Version (.*),',line):
                version = re.findall('^Cisco IOS.*, C3900.*Version (.*),',line)
                version = version[0]
        
        list_card = []
        list_serial_number = []
        hardware_break = False
        for line in read_file_list:
            #HARDWARE
            #card PID
            if re.findall('^PID: (.*),.*,',line):
                hardware_break = True
                card = re.findall('^PID: (.*),.*,',line)
                card = card[0]
                list_card.append(card)
            #card serial number
            if re.findall('^PID: .*,.*,.*SN: (.*)',line):
                serial_number = re.findall('^PID: .*,.*,.*SN: (.*)',line)
                serial_number = serial_number[0]
                list_serial_number.append(serial_number)
            #break loop
            if hardware_break == True and re.findall('.*#',line):
                break
        
        cpu_break = False
        for line in read_file_list:
            #CPU
            #cpu
            if re.findall('^CPU utilization for five seconds: (.*)%\/.*%;.*;',line):
                cpu_break = True
                process = re.findall('^CPU utilization for five seconds: (.*)%\/.*%;.*;',line)
                process = process[0]
                #print('cpu')
                #print(cpu)
            #cpu interrupt
            if re.findall('^CPU utilization for five seconds: .*\/(.*)%;.*;',line):
                interrupt = re.findall('^CPU utilization for five seconds: .*\/(.*)%;.*;',line)
                interrupt = interrupt[0]
                #cpu total
                total = int(process) + int(interrupt)
                #cpu status
                if total<21 :
                    status='Low'
                elif total<81 :
                    status='Medium'
                else:
                    status='High'
                total=str(total)
            #break loop
            if cpu_break == True and re.findall('.*#',line):
                break
        
        memory_break = False
        for line in read_file_list:
            #MEMORY
            #Memory Total
            if re.findall('^Processor Pool Total:\s+(\d+)\s+Used:\s+\d+',line):
                memory_break = True
                memory_total = re.findall('^Processor Pool Total:\s+(\d+)\s+Used:\s+\d+',line)
                memory_total = memory_total[0]
            #Memory Used
            if re.findall('^Processor Pool Total:\s+\d+\s+Used:\s+(\d+)',line):
                memory_used = re.findall('^Processor Pool Total:\s+\d+\s+Used:\s+(\d+)',line)
                memory_used = memory_used[0]
                #memory percentage
                memory_percentage = (int(memory_used)/int(memory_total))*100
                #memory status
                if float(memory_percentage)<21 :
                    memory_status='Low'
                elif float(memory_percentage)<81 :
                    memory_status='Medium'
                else:
                    memory_status='High'
                memory_percentage=re.findall('(^.{5})*',str(memory_percentage))
                utils=memory_percentage[0]
            #break loop
            if memory_break == True and re.findall('.*#',line):
                break
        #sorting memory
        list_memory = []
        list_memory_sorted = []
        memory_sorted_break = False
        memory_sorted_add_list = False
        for line in read_file_list:
            #make conditional statement to let program start append to list, and get ready to break loop
            if re.findall('.*PID\s+TTY\s+Allocated\s+Freed\s+Holding\s+Getbufs\s+Retbufs\s+Process',line):
                memory_sorted_break = True
                memory_sorted_add_list = True
            #append value to list
            if memory_sorted_break == True:
                if re.findall('.*PID\s+TTY\s+Allocated\s+Freed\s+Holding\s+Getbufs\s+Retbufs\s+Process',line):
                    pass
                elif '-' in line:
                    pass
                else:
                    list_memory.append(line)
            #break loop
            if memory_sorted_break == True and re.findall('.*#',line):
                break
            elif memory_sorted_break == True and re.findall('^\s*$',line):
                break
        #create new list that only contain memory allocated and name application that using it
        for i in list_memory:
            try:
                #print(i.split()[7])
                #print(i.split()[2])
                list_memory_sorted.append(i.split()[2]+' '+i.split()[7])
            except:
                pass
        #sort memory with allocated as key
        list_memory_sorted.sort(reverse=True,key = lambda x: int(x.split()[0]))
        #print('Memory Top Three')
        topproc = (list_memory_sorted[0].split()[1]+'\n'+list_memory_sorted[1].split()[1]+'\n'+list_memory_sorted[2].split()[1])
        #print(memory_top_three)

        #get environment
        list_psu_capture = []
        list_fan = []
        list_fan_cond_cp = []
        list_temp = []
        list_temp_cond = []
        list_psu = []
        list_psu_cond = []
        psu_line_start = 0
        psu_line_end = 0
        count_line=0
        for i in read_file_list:
            if re.findall('^\s+(Fan\s+\d+)\s+\S+',i):
                regex_fan = re.findall('^\s+(Fan\s+\d+)\s+\S+',i)
                fan = regex_fan[0]
                list_fan.append(fan)
                #print(fan)
            if re.findall('^\s+Fan\s+\d+\s+(\S+),', i):
                regex_fan_cond = re.findall('^\s+Fan\s+\d+\s+(\S+),', i)
                fan_cond = regex_fan_cond[0]
                list_fan_cond_cp.append(fan_cond)
                #print(fan_cond)
            if re.findall('^(.*temperature):\s+\S+\S+\s+\S+\s+\S+',i):
                regex_temp = re.findall('^(.*temperature):\s+\S+\S+\s+\S+\s+\S+',i)
                temp = regex_temp[0]
                list_temp.append(temp)
                #print(temp)
            if re.findall('^.*temperature:\s+\S+\S+\s+\S+\s+(\S+)', i):
                regex_temp_cond = re.findall('^.*temperature:\s+\S+\S+\s+\S+\s+(\S+)', i)
                temp_cond = regex_temp_cond[0]
                list_temp_cond.append(temp_cond)
                #print(temp_cond)
            if re.findall('^(.*Power Supply\s+\S+\s+\S+).*Status:\s+\S+',i):
                regex_psu = re.findall('^(.*Power Supply\s+\S+\s+\S+).*Status:\s+\S+',i)
                psu = regex_psu[0]
                list_psu.append(psu)
                #print(temp)
            if re.findall('^.*Power Supply\s+\S+\s+\S+.*Status:\s+(\S+)', i):
                regex_psu_cond = re.findall('^.*Power Supply\s+\S+\s+\S+.*Status:\s+(\S+)', i)
                psu_cond = regex_psu_cond[0]
                list_psu_cond.append(psu_cond)
                #print(temp_cond)
            


        #open db connection
        db = sqlite3.connect('pmdb')
        cursor = db.cursor()
        #db software
        try:
            cursor.execute('''INSERT INTO swsumtable(version)
                    VALUES(?)''', (version,))
        except:
            cursor.execute('''INSERT INTO swsumtable(version)
                    VALUES(?)''', (self.file+'-'+'error',))
        try:
            cursor.execute('''INSERT INTO swtable(devicename, model, iosversion, uptime, confreg)
                    VALUES(?,?,?,?,?)''', (devicename, model, iosversion, uptime, confreg,))
        except:
            cursor.execute('''INSERT INTO swtable(devicename, model, iosversion, uptime, confreg)
                    VALUES(?,?,?,?,?)''', (self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error',))
        #db hardware
        try:
            cursor.execute('''INSERT INTO hwsumtable(model)
                    VALUES(?)''', (model,))
            count_sql = 0
        except:
            cursor.execute('''INSERT INTO hwsumtable(model)
                    VALUES(?)''', (self.file+'-'+'error',))
            count_sql = 0
        try:
            for card in list_card:
                cursor.execute('''INSERT INTO hwcardtable(devicename, model, card, sn)
                        VALUES(?,?,?,?)''', (devicename,model,card,list_serial_number[count_sql],))    
                count_sql+=1
        except:
            for card in list_card:
                cursor.execute('''INSERT INTO hwcardtable(devicename, model, card, sn)
                        VALUES(?,?,?,?)''', (self.file+'-'+'error',self.file+'-'+'error',self.file+'-'+'error',self.file+'-'+'error',))    
                count_sql+=1
        #db process cpu and memory
        try:
            cursor.execute('''INSERT INTO cpusumtable(devicename, model, total, process, interrupt, status)
                    VALUES(?,?,?,?,?,?)''', (devicename, model, total, process, interrupt, status,))
        except:
            cursor.execute('''INSERT INTO cpusumtable(devicename, model, total, process, interrupt, status)
                    VALUES(?,?,?,?,?,?)''', (self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error',))            
        try:
            cursor.execute('''INSERT INTO memsumtable(devicename, model, utils, topproc, status)
                    VALUES(?,?,?,?,?)''', (devicename, model, utils, topproc, status,))
        except:
            cursor.execute('''INSERT INTO memsumtable(devicename, model, utils, topproc, status)
                    VALUES(?,?,?,?,?)''', (self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error', self.file+'-'+'error',))
        #db environment
        try:
            count_sql = 0
            for psu in list_psu:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (devicename,'Power Supply',psu,list_psu_cond[count_sql],))
                count_sql+=1
        except:
            count_sql = 0
            for psu in list_psu:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (self.file+'-'+'error','Power Supply',self.file+'-'+'error',))
                count_sql+=1
        try:
            count_sql = 0
            for fan in list_fan:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (devicename,'Fan',fan,list_fan_cond_cp[count_sql],))
                count_sql+=1
        except:
            count_sql = 0
            for fan in list_fan:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (self.file+'-'+'error','Fan',self.file+'-'+'error',self.file+'-'+'error',))
                count_sql+=1
        try:
            count_sql = 0
            for temp in list_temp:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (devicename,'Temperature',temp,list_temp_cond[count_sql],))
                count_sql+=1
        except:
            count_sql = 0
            for temp in list_temp:
                cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                        VALUES(?,?,?,?)''', (self.file+'-'+'error','Temperature',self.file+'-'+'error',self.file+'-'+'error',))
                count_sql+=1
       #LOG Checking
        try:
            cursor.execute('''INSERT INTO logtable(devicename, model, script)
                    VALUES(?,?,?)''', (devicename, model,self.__class__.__name__,))
        except:
            cursor.execute('''INSERT INTO swtable(devicename, model, script)
                    VALUES(?,?,?)''', (self.file+'-'+'error', self.file+'-'+'error',self.file+'-'+'error',))
        db.commit()             
        db.close()  