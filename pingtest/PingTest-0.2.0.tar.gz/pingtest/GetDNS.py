from subprocess import Popen, PIPE
import shlex
import re

def DnsCheck():

    pingbit = "systemd-resolve --status --no-pager "
    args = shlex.split(pingbit)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #print(str(out))

    matchms = re.findall("DNS Servers.*\d+.\d+.\d+.\d",str(out))

    if len(matchms) == 0:
        matchsplit = ["OK" , "NO DNS - "]
    else:
        print('MATCH = ' + str(matchms[0]))
        #matchsplit = re.split(r'\:',str(matchms[0]))
        ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        matchsplit = re.findall(ipPattern,str(matchms[0]))
        print('MATCH split = ' + str(matchsplit))

    return matchsplit[0]

def main():

    dnsip = DnsCheck()
    print("DNS IP is =" + dnsip)
    print("DID THIS WORK " + str(findIP))



if __name__ == '__main__':
    main()
