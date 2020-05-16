from tapi.translateapi import mainAPI
from sys import argv
s = ""
if len(argv)!=2:
	print("Arguments is not correct")
	exit(1)

for x in mainAPI(argv[1])['translateResult'][0]:
	s+=x['tgt']+' '

print(s)
