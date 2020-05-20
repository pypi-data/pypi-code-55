class Server:
	def __init__(self):
		try:
			data = requests.post('https://growtopiagame.com/growtopia/server_data.php').text
		except:
			raise NetworkError("Sadly, you can't establish the connection between us (by growtopiagame.com)")
		# "'server|209.59.191.76\r\nport|17091\rtype|1\r\n#maint|Server is under maintenance. We will be back online shortly. Thank you for your patience!\r\nbeta_server|beta.growtopiagame.com\r\nbeta_port|27003\r\r\nbeta_type|1\r\nmeta|115.178.223.44\r\nRTENDMARKERBS1001\r\n'"
		
		data = JSONFromPacketData(data)
		
		self.address = Address("0.0.0.0", 1337) # Always use 1337 for something cool ;)
		self.host = Host(self.address, 1024, 10, 0, 0)
		
		if self.host is not True:
			raise NetworkError("Fail when attempts to make a host")
		
		cf = self.host.compress_with_range_coder(self.host)
		if cf is not 0:
			raise ENetError("Compressing ENet host failed")
		
		
		############### REAL SERVER ####################
		self.realServer = Host(None, 1, 2, 0, 0)
		if self.realServer is not True:
			raise NetworkError("Failed to make a connection client")
		
		c = self.realServer.compress_with_range_coder(self.realServer)
		if c is not 0:
			raise ENetError("Compressing ENet host failed")
		
		self.realServer.flush(enet.realServer)
		#return true
	
	def __repr__(self):
		return '<GrowtopiaServer at '+str(id(self))+'>'
	
	def quit(self):
		