VERSION='0.0.3'

import configparser
import os
from os.path import expanduser
cfg= configparser.ConfigParser()
config_path=expanduser('~/.tclib')
cfg.read(config_path)
def save_config():
	sav_file=config_path+'.tmp'
	cfg.write(open(sav_file,'w'))
	os.replace(sav_file,config_path)
 
def download(url,path,checksum=None):
	import urllib.request
	import hashlib
	try:
		h=hashlib.sha256(open(path,'rb').read()).hexdigest()
		if checksum is not None and (checksum==h or checksum=='any'):
			return
	except:
		pass
	urllib.request.urlretrieve(url, path)
	if checksum is not None and checksum!='any':
		if hashlib.sha256(open(path,'rb').read()).hexdigest()!=checksum:
			raise Exception('Checksum failed')
def ifttt_config():
	global cfg
	print('Event name:')
	event=input()
	print('apikey:')
	apikey=input()
	cfg['ifttt']={'event':event,'apikey':apikey}
	save_config()

def ifttt(message):
	import requests
	c=cfg['ifttt']
	event,apikey=c['event'],c['apikey']
	requests.post('https://maker.ifttt.com/trigger/{}/with/key/{}'.format(event,apikey), data={"value1":message})

def telegram_config():
	global cfg
	print('chat id:')
	cid=input()
	print('apikey:')
	apikey=input()
	cfg['telegram']={'cid':cid,'apikey':apikey}
	save_config()

def telegram(message):
	import requests
	c=cfg['telegram']
	cid,apikey=c['cid'],c['apikey']
	requests.post('https://api.telegram.org/bot{}/sendMessage'.format(apikey), data={"chat_id":cid,'text':message})
