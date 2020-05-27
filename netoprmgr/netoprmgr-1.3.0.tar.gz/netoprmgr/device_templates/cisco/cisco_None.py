import sqlite3
import re



class cisco_None:
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
                #print(devicename)
            #get device model
            elif re.findall('^.isco\s+(\S+).*with.*bytes',line):
                model = re.findall('^.isco\s+(\S+).*with.*bytes',line)
                model = model[0]           
        #open db connection
        db = sqlite3.connect('pmdb')
        cursor = db.cursor()
        #LOG Checking
        try:
            cursor.execute('''INSERT INTO logtable(devicename, model, script)
                    VALUES(?,?,?)''', (devicename, model,self.__class__.__name__,))
        except:
            cursor.execute('''INSERT INTO logtable(devicename, model, script)
                    VALUES(?,?,?)''', (self.file+'-'+'error', self.file+'-'+'error',self.file+'-'+'error',))
        db.commit()             
        db.close()

        
        