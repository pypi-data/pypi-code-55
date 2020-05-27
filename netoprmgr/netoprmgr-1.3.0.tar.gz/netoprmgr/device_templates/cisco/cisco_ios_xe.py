import sqlite3
import re



class cisco_ios_xe:
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
                device_name = re.findall('^hostname (.*)',line)
                device_name = device_name[0]
            #get device model
            elif re.findall('^cisco\s+(\S+).*processor.*with.*bytes',line):
                device_model = re.findall('^cisco\s+(\S+).*processor.*with.*bytes',line)
                device_model = device_model[0]                
            #get ios version
            elif re.findall('^System image file is "(.*)"',line):
                ios_version = re.findall('^System image file is "(.*)"',line)
                ios_version = ios_version[0]
            #get uptime
            elif re.findall('^.*uptime is (.*)',line):
                uptime = re.findall('^.*uptime is (.*)',line)
                uptime = uptime[0]
            #get configuration register
            elif re.findall('^Configuration register is (.*)',line):
                confreg = re.findall('^Configuration register is (.*)',line)
                confreg = confreg[0]
            #SOFTWARE TABLE SUMMARY
            elif re.findall('^.*Version (.*),',line):
                version = re.findall('^.*Version (.*),',line)
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
            if re.findall('.*CPU utilization for five seconds: .*;.*:(.*)%',line):
                cpu_break = True
                cpu = re.findall('.*CPU utilization for five seconds: .*;.*:(.*)%',line)
                cpu = cpu[0]
                #print('cpu')
                #print(cpu)
            #cpu interrupt
            if re.findall('.*CPU utilization for five seconds: .*;.*:(.*)%',line):
                #cpu_interrupt = re.findall('^CPU utilization for five seconds: .*\/(.*)%;.*;',line)
                cpu_interrupt = '0'
                #cpu total
                cpu_total = int(cpu) + int(cpu_interrupt)
                #cpu status
                if cpu_total<21 :
                    cpu_status='Low'
                elif cpu_total<81 :
                    cpu_status='Medium'
                else:
                    cpu_status='High'
                cpu_total=str(cpu_total)
            #break loop
            if cpu_break == True and re.findall('.*#',line):
                break
        
        memory_break = False
        for line in read_file_list:
            #MEMORY
            #Memory Total
            if re.findall('^Processor Pool Total:(.*)Used:.*Free:.*',line):
                memory_break = True
                memory_total = re.findall('^Processor Pool Total:(.*)Used:.*Free:.*',line)
                memory_total = memory_total[0]
            #Memory Used
            if re.findall('^Processor Pool Total:.*Used:(.*)Free:.*',line):
                memory_used = re.findall('^Processor Pool Total:.*Used:(.*)Free:.*',line)
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
                memory_percentage=memory_percentage[0]
            #break loop
            if memory_break == True and re.findall('.*#',line):
                break
        #sorting memory
        list_memory = []
        list_memory_sorted = []
        memory_sorted_break = False
        memory_sorted_add_list = False
        for enum, line in enumerate(read_file_list):
            #make conditional statement to let program start append to list, and get ready to break loop
            if re.findall('.*PID\s+Text\s+Data\s+Stack\s+Heap\s+RSS\s+Total\s+Process',line):
                memory_sorted_break = True
                memory_sorted_add_list = True
            #append value to list
            if memory_sorted_break == True:
                if re.findall('.*PID\s+Text\s+Data\s+Stack\s+Heap\s+RSS\s+Total\s+Process',line):
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
                list_memory_sorted.append(i.split()[6]+' '+i.split()[7])
            except:
                pass
        #sort memory with allocated as key
        list_memory_sorted.sort(reverse=True,key = lambda x: int(x.split()[0]))
        #print('Memory Top Three')
        memory_top_three = (list_memory_sorted[0].split()[1]+'\n'+list_memory_sorted[1].split()[1]+'\n'+list_memory_sorted[2].split()[1])
        #print(memory_top_three)

        #open db connection
        db = sqlite3.connect('pmdb')
        cursor = db.cursor()
        cursor.execute('''INSERT INTO summarytable(devicename, model, iosversion, uptime, confreg, version, cpu, cpu_interrupt, cpu_total, cpu_status, memory_percentage, memory_top_three, memory_status)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (device_name,device_model,ios_version,uptime,confreg,version,(cpu+'%'),(cpu_interrupt+'%'),cpu_total,cpu_status,memory_percentage,memory_top_three,memory_status,))
        count_sql = 0
        for card in list_card:
            cursor.execute('''INSERT INTO hardware(devicename, model, card, serial_number)
                      VALUES(?,?,?,?)''', (device_name,device_model,card,list_serial_number[count_sql],))
            count_sql+=1
        db.commit()             
        db.close()

        
        