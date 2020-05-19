"""
Given a ip address,this program change it.
Example:
        Input: address = "1.1.1.1"
        Output: "1[.]1[.]1[.]1"
        """


def defanging(ip):
    ip = ip.split('.')
    newIp = '[.]'.join(ip)
    return newIp


address = '192.168.10.1'
# address = input()
print(defanging(address))
