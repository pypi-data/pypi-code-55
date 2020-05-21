import sys
from . import *
if sys.argv[1]=='download':
	print(sys.argv)
	if len(sys.argv)==4:
		url,path=sys.argv[2:]
		download(url,path)
	else:
		url,path,check=sys.argv[2:]
		download(url,path,check)
if sys.argv[1]=='ifttt':
	cmd=sys.argv[2]
	if cmd=='config':
		ifttt_config()
	else:
		ifttt(cmd)
if sys.argv[1]=='telegram':
	cmd=sys.argv[2]
	if cmd=='config':
		telegram_config()
	else:
		telegram(cmd)
