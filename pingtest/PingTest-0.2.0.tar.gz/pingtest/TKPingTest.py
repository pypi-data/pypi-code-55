import os
import re
from subprocess import Popen, PIPE
import shlex
import time
import datetime
import logging

from pingtest.GetDNS import DnsCheck
from pingtest.GetGateway import GatewayCheck

responselist = []
respomsems = []
responsetimedate = []
hostlist = []

import mysql.connector

def CheckHost(hostcheck):

  #response = os.system("ping -c 1 " + hostcheck)

  pingbit = "ping -D -c 1 " + hostcheck
  args = shlex.split(pingbit)
  proc = Popen(args, stdout=PIPE, stderr=PIPE)
  out, err = proc.communicate()
  exitcode = proc.returncode
  #print(str(out))

  matchms = re.findall("time=\d+.\d+",str(out))
  #print('MATCH = ' + str(matchms))

  #and then check the response...
  if exitcode == 0:
    #print(hostcheck, 'is up!')
    responselist.append("green")

    # Get response times from stdout
    matchms = re.findall("time=\d+.\d+\s\S\S",str(out))
    #print('Match ms = ' + str(matchms))
    respomsems.append(matchms[0])


    # Get date/time stampe from stdout
    #matchtdget= re.findall("\d{10}",str(out))
    #matchtdget = datetime.datetime.now().timestamp()
    #matchtd = datetime.datetime.fromtimestamp(int(matchtdget)).strftime('%Y-%m-%d %H:%M:%S')
    #print('*********************** Match time/date = ' + str(matchtd))
    #print(time.ctime(int(matchtd[0])))
    #print(time.gmtime(int(matchtd[0])))
    #print("LLLLLLLLLLLLOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKK")
    #print(matchtd)
    #responsetimedate.append(time.ctime(int(matchtd[0])))
    #responsetimedate.append(matchtd)

  else:
    #print(hostcheck, 'is down!')
    responselist.append("red")
    respomsems.append("0")

  matchtdget = datetime.datetime.now().timestamp()
  matchtd = datetime.datetime.fromtimestamp(int(matchtdget)).strftime('%Y-%m-%d %H:%M:%S')
  print('*********************** Match time/date = ' + str(matchtd))
  responsetimedate.append(matchtd)




def PingTest():

    responselist[:] = []
    respomsems[:] = []
    responsetimedate[:] = []
    hostlist[:] = []

    dnsip = DnsCheck()
    #print("RETURNED = "+dnsip)
    hostlist.append(dnsip)

    gatewayip = GatewayCheck()
    logging.debug("RETURNED = "+gatewayip)
    print("RETURNED = "+gatewayip)
    hostlist.append(gatewayip)

    hostlist.append("8.8.8.8")
    hostlist.append("www.google.com")

    hostlist.append("1.1.1.1")
    hostlist.append("www.alpineinsight.co.uk")
#    hostlist.append("www.apple.com")

    #print(hostlist)

    for hostcheck in hostlist:
        #print(hostcheck)
        CheckHost(hostcheck)


    #mydb = mysql.connector.connect(
    #    host="localhost",
    #   user="colin",
    #    passwd="colin")


    #mycursor = mydb.cursor()
    #mycursor.execute("SHOW DATABASES")
    #for x in mycursor:
    #    print(x)


    for x in range(0, len(hostlist)):
        #print("HHHHHHHHHHHHHHHHHHOOOOOOOOOOOOSSSSSSSSSSTTTTTTTTTTTT")
        #print(hostlist[x])
        mydb = mysql.connector.connect(
            host="localhost",
            user="colin",
            passwd="colin",
            database="colin")
        mycursor = mydb.cursor()
        #print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")tt
        #print(str(respomsems))
        if responselist[x] == "green":
            justms = re.findall("\d+.\d",str(respomsems[x]))
        else:
            justms = respomsems[x]
        print(justms)
        print("****JUSTMS**********"+str(justms))
        #if not justms:
        #    justms.append('NULL')

        print(justms)
        #sql = "INSERT INTO pingtest(hostname,testdatetime,responsetime,status) VALUES  (%s,STR_TO_DATE(%s,'%Y-%m-%d %H:%i:%S'),%s,%s)"
        sql = "INSERT INTO pingtest(hostname,testdatetime,responsetime,status) VALUES  (%s,%s,%s,%s)"
        print(hostlist[x])
        print(responsetimedate[x])
        print(justms[0])
        print(responselist[x])
        print(len(hostlist))
        val = (hostlist[x],responsetimedate[x],justms[0],responselist[x])
        mycursor.execute(sql, val)
        mydb.commit()



    return(responselist, hostlist, respomsems, responsetimedate)


