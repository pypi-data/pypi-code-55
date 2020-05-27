import sqlite3
import re



class cisco_asa:
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
            elif re.findall('^Name:.*DESCR: "(.*ASA\s+\S+).*"',line):
                device_model = re.findall('^Name:.*DESCR: "(.*ASA\s+\S+).*"',line)
                device_model = device_model[0]                
            #get ios version
            elif re.findall('^System image file is "(.*)"',line):
                ios_version = re.findall('^System image file is "(.*)"',line)
                ios_version = ios_version[0]
            #get configuration register
            elif re.findall('^Configuration register is (.*)',line):
                confreg = re.findall('^Configuration register is (.*)',line)
                confreg = confreg[0]
            #SOFTWARE TABLE SUMMARY
            elif re.findall('^ASA Version (.*)',line):
                version = re.findall('^ASA Version (.*)',line)
                version = version[0]
        
        for line in read_file_list:
            #get uptime
            if re.findall(device_name+'\s+up\s+(.*)',line):
                uptime = re.findall(device_name+'\s+up\s+(.*)',line)
                uptime = uptime[0]
        
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
            if re.findall('^CPU utilization for 5 seconds = (\d+)',line):
                cpu_break = True
                cpu = re.findall('^CPU utilization for 5 seconds = (\d+)',line)
                cpu = cpu[0]
                #print('cpu')
                #print(cpu)
                
                #cpu interrupt
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
            if re.findall('^Total memory:\s+(\S+)',line):
                memory_break = True
                memory_total = re.findall('^Total memory:\s+(\S+)',line)
                memory_total = memory_total[0]
            #Memory Used
            if re.findall('^Used memory:\s+(\S+)',line):
                memory_used = re.findall('^Used memory:\s+(\S+)',line)
                memory_used = memory_used[0]
                #memory percentage

            #break loop
            if memory_break == True and re.findall('.*#',line):
                break
        
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
        
        #No Memory Top Three
        memory_top_three = ('-')
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

        
        