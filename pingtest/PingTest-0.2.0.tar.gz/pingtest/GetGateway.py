from subprocess import Popen, PIPE
import shlex
import re

def GatewayCheck():

    pingbit = "route -n"
    args = shlex.split(pingbit)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #print(str(out))
    #print(str(out[7]))

    matchgw = re.findall("\d+.\d+.\d+.\d",str(out))
    #print('MATCH = ' + str(matchgw[1]))

    return matchgw[1]

def main():

    gatewayip = GatewayCheck()
    #print("Gateway IP is =" + gatewayip)

if __name__ == '__main__':
    main()
