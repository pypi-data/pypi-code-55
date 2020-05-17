from subprocess import Popen, PIPE
import shlex
import re
import datetime
import mysql.connector

def SpeedTest():

    speedbit = "speedtest"
    #args = shlex.split(pingbit)
    proc = Popen(speedbit, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #print(str(out))

    if exitcode == 0:
        downspeed = re.findall("Download: \d+.\d+ Mbit/s",str(out))
        print(downspeed)
        uploadspeed = re.findall("Upload: \d+.\d+ Mbit/s",str(out))
        print(uploadspeed)
        testserver = re.findall("Testing.*\d+.\d+.\d+.\d",str(out))
        print(testserver)
    else:
        downloadspeed = "0"
        uploadspeed = "0"
        testserver = "NOT AVAILABLE"


    mydb = mysql.connector.connect(
            host="localhost",
            user="colin",
            passwd="colin",
            database="colin")
    mycursor = mydb.cursor()
    now = datetime.datetime.utcnow()
    justds = re.findall("\d+.\d",str(downspeed))
    justus = re.findall("\d+.\d",str(uploadspeed))
    print(justds)
    print(justus)
    #print(justms)
    #sql = "INSERT INTO pingtest(hostname,testdatetime,responsetime,status) VALUES  (%s,STR_TO_DATE(%s,'%Y-%m-%d %H:%i:%S'),%s,%s)"
    sql = "INSERT INTO downloadtest(servername,testdatetime,downloadspeed,uploadspeed) VALUES  (%s,%s,%s,%s)"
    val = (testserver[0],now, justds[0],justus[0])
    mycursor.execute(sql, val)
    mydb.commit()

    return testserver[0], downspeed[0], uploadspeed[0]

def main():

    SpeedTest()

if __name__ == '__main__':
    main()
