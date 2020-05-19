from pyquicksql.utils import sql_enums, sql_enums, logger_enums, logger_errors

from pyquicksql.mysql import mysql_set, mysql_lookup, mysql_modify, mysql_remove

from pyquicksql.sqlite import sqlite_set,sqlite_lookup, sqlite_modify, sqlite_remove

class Connect:
	def __init__(self, server, database):
		'''
			(Server, Database) -> None
			initializes the class connect for all mysql database requests
		'''
		self.server = server
		self.database = database
		self.db_type = server.getName()
		self.db_ip = server.getIP()
		self.db_port = server.getPort()
	def getAccount(self):
		'''
			(None) -> (tuple)
			the getter function for the account credentials used to connect
			
			@returns the user account details as a tuple in the form:
					= (
						0: username,
						1: password,
					)
		'''
		account = server.getAccount()
		return (account[0], account[1]) #(username, password)
	def lookup(self, unknown_column, known_colum, known_element):
		'''
			(Connect, string, string, string) -> (string)
			looksup the table element specificied by the paramaters
			
			@paramaters the passed db_type matches Name.MYSQL or Name.SQLITE
			@returns the string element matching the paramaters
			@exception returns an empty string ''
		'''
		if ( self.db_type == sql_enums.Name.MYSQL ):
			return mysql_lookup.retreive(self.server, self.database, unknown_column, known_colum, known_element)
		elif ( self.db_type == sql_enums.Name.SQLITE ):
			return sqlite_lookup.retreive(self.server, self.database, unknown_column, known_colum, known_element)
	def push(self, columns, elements):
		'''
			(Connect, list of strings, list of strings) -> (boolean)
			pushes the 
			
			@paramaters the passed db_type matches Name.MYSQL or Name.SQLITE
			@returns True if the connection and push was successful
			@exception returns False if the element was NOT pushed
		'''
		if ( self.db_type == sql_enums.Name.MYSQL ):
			return mysql_set.commit(self.server, self.database, columns, elements)
		elif ( self.db_type == sql_enums.Name.SQLITE ):
			return sqlite_set.commit(self.server, self.database, columns, elements)
	def swap(self, column, element, identifiers, identifier_elements):
		'''
			(Connect, ) -> (boolean)
			
			@paramaters the passed db_type matches Name.MYSQL or Name.SQLITE
			@returns True if the elements were swapped in the SQL table
			@exception returns False if the elements were not swapped
		'''
		if ( self.db_type == sql_enums.Name.MYSQL ):
			return mysql_modify.commit(self.server, self.database, column, element, identifiers, identifier_elements)
		elif ( self.db_type == sql_enums.Name.SQLITE ):
			return sqlite_modify.commit(self.server, self.database, column, element, identifiers, identifier_elements)
	def remove(self, column, element):
		'''
			(Connect, ) -> (string)
			
			@paramaters the passed db_type matches Name.MYSQL or Name.SQLITE
			@returns True if the 
		'''
		if ( self.db_type == sql_enums.Name.MYSQL ):
			return mysql_remove.commit(self.server, self.database, column, element)
		elif ( self.db_type == sql_enums.Name.SQLITE ):
			return sqlite_remove.commit(self.server, self.database, column, element)
	def __eq__(self, other):
		'''
			(Connect) -> (boolean)
			@returns true if the two connection classes make requests
					 to the same server (does not compare accounts)
		'''
		#check if the sockets conenct to the same database server
		if this.db_ip != other.db_ip:
			return false;
		#check if the sockets connect to the same port on the server
		if this.db_port != other.db_port:
			return false;
	def __repr__(self):
		'''
			(Connect) -> (string)
			@returns the a string representation of the Connect class
			
		'''
		account = server.getAccount()
		return f'Connect({self.db_ip}, {self.db_port}, {account[0]}, {account[1]})'
	def __str__(self):
		'''
			(Connect) -> (string)
			@returns the a visualy apealing string representation of the Connect class
		'''
		username = server.getAccount()[0]
		return f'MySQL Connection on {self.db_ip}:{self.db_port} using user {username}'
		
		