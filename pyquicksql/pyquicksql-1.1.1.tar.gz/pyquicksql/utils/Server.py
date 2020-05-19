class Server:
	def __init__(self, _name, _ip, _port, _username, _password):
		'''
			(Name, string, int) -> None
			initializes a new database class to be inputed into a connect class
			@paramaters a Name enum (MYSQL, SQLITE) must be at least specified
			@exception the default type will be set to MYSQL as it is the more popular choice
		'''
		self._name = _name
		self._ip = _ip
		self._port = _port
		self._username = _username
		self._password = _password
	def getName(self):
		'''
			(Server) -> (Name)
			the getter function for the enum type of the server
		'''
		return self._name
	def getIP(self):
		'''
			(Server) -> (string)
			the getter function for the ip string of the connection
		'''
		return self._ip
	def getPort(self):
		'''
			(Server) -> (int)
			the getter function for the port of the connection
		'''
		return self._port
	def getAccount(self):
		'''
			(Server) -> (tuple)
			the getter function for the account (username, password) of the server
		'''
		return ( self._username, self._password )
	def setName(self, new_name):
		'''
			(Server, Name) -> None
			@params new_name must be of enum type Name
			@exception if the params arn't follow no change will be made
		'''
		if ( self._name == Name.MYSQL or self._name == Name.SQLITE ):
			self._name = new_name
	def setIP(self, new_ip):
		'''
			(Server, string) -> None
			@params new_ip must be of type string to rep. the ip
			@exception the ip will not be changed
		'''
		if ( isinstance(new_ip, str) ):
			self._ip = new_ip
	def setPort(self, new_port):
		'''
			(Server, int) -> None
			@params new_port must be of type int to rep. the port
			@exception the port will not be changed
		'''
		if ( isinstance(new_port, int) ):
			self._port = new_port
	def __eq__(self, other):
		'''
			(Server) -> (boolean)
			compares the current class to other on a basis of the Name enum type, ip, and port
		'''
		if ( self._name != other._name ):
			return False
		if ( self._ip != other._ip ):
			return False
		if ( self._port != other._port ):
			return False
	def __repr__(self):
		'''
			(Server) -> (string)
			Returns a string representation of the Database class structure
		'''
		return f'Server({self.name}, {self.ip}, {self.port})'
	def __str__(self):
		'''
			(Server) -> (string)
			Returns the a visualy apealing string representation of the Database.
		'''
		return f'{self.name} -> {self.ip}:{self.port}'