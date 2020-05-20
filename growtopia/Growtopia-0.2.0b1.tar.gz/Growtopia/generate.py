import re, json

def Mac(): # v0.1.1 i guess
	"""
	Generate random MAC Address
	"""
	return ':'.join('%02x'%random.randrange(256) for _ in range(5))
		
def JSONFromPacketData(data): # v0.2.0
	"""
	Converts your Growtopia packet data to JSON automatically
	"""
	data = data.replace("^","")
	incomplete = re.split(r"\\r|\\n|(?=^$)", data)
	complete = dict()
	try:
		for a in incomplete:
			if a is '':
				pass
			else:
				u = a.split("|")
				try:
					complete[u[0]] = int(u[1])
				except:
					complete[u[0]] = u[1]
	except IndexError:
		pass # Reach the RT-END and such means done
	
	return complete

def PacketDataFromJSON(data): # v0.2.0
	"""
	Converts JSON Dictionary data to standart growtopia packet data
	"""
	try:
		data = json.loads(data)
	except json.decoder.JSONDecodeError:
		data = json.loads(data.replace("'", "\""))
	
	keys = list()
	values = list()
	completed = str()
	
	for i in data:
		keys.append(i)
		values.append(data[i])
	
	for key in keys:
		completed += key+"|"+str(data[key]) + '\n\r'
	
	return completed

def chatHistory():
	pass # TODO