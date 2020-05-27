from cffi import FFI
from datetime import datetime

from pyquicksql.utils.logger_enums import Column
from pyquicksql.utils.logger_errors import *

'''
	the following code is a string parser for a bitstream received by a python socket
	@returns the server, database type, and further messages based on the respective req
	0, 1, 2, 3 as located in the bitstream b'[msg][req type][status][location/userid]'
	@example the bitsream b'<toString(server)<>toString(database)>!message!' is received
	by the function with the request type '0', the returned string will be parsed into the
	string representation of the server passed into the logger.
'''

class Logger:
	
	def __init__(self, _directory='default/general_logs.txt'):
		'''
			(Logger, string) -> None
			the initializer function for the Logger class
			
			@paramaters the _directory be a string to a propper folder
			@exception if no _directory string is given it will go to the
					   default logger location 'general/general_logs.txt'
		'''
		#create a new file with the given directory
		createDirectory = open(_directory, 'w+')
		createDirectory.close()
		
		self._directory = _directory
		self._logs = []
		self._commits = 0
	
	def parse(self, line, column):
		'''
			(string, Column) -> (string)
			parses the formated text: 
				'<toString(server)<>toString(database)>!message!'
			
			@paramaters the request (int argument) must be a valid
						integer between 0 and 2 representing the
						various pieces of data present within the
						bitsream:
							a) int 0 : the type of database server
							b) int 1 : the database, table, autocommit
							c) int 2 : the specific message of the log
			@returns the datatype associated with the integer provided
					 by the function argument
			@exception returns None type if an unsupported bitsream is
					   provided by the user
		'''
		ffi = FFI()
		lib = ffi.dlopen("data_markup/target/release/liblibdatamarkup.dylib")

		ffi.cdef('char* parse(const char *n, int);')
		
		try:
			request_val = ffi.new('char[]', bytes(line.decode(), 'utf-8'))
			stream_modified = ffi.string(lib.parse(request_val, column)).decode('utf-8')
			return stream_modified
		except Exception as e:
			raise MarkupSyntaxError(line)
	
	def getDirectory(self):
		'''
			(Logger) -> (string)
			the getter function for the directory of all the log files
			
			@returns the full directory in the format of a string
		'''
		return self._directory
	
	def getCommits(self):
		'''
			(Logger) -> (int)
			the getter function for the number of commited logs during the scripts runtime
			
			@returns an integer values >= 0 representing the number of commits during the session
		'''
		return self._commits
	
	def getLogs(self):
		'''
			(Logger) -> (list of strings)
			the getter function for the temporary variable for logs within the current session
			
			@returns a list of strings of length n representing the number of logs commited to the
					 folder during the current session (runtime of the script)
		'''
		return self._logs
	
	def copy(self):
		'''
			(Directory) -> (boolean)
			coppies the class file _directory logs to the class list var _logs
			
			@paramaters the _directory string is a real file with the correct path
			@exception the function will throw a DirectoryNotFoundError
		'''
		self._logs = []
		try:
			file_logs = open(self._directory, 'r')
			line = file_logs.readLine()
			while (line != ''):
				self._logs.append(line)
			file_logs.close()
		except:
			raise DirectoryNotFound(self._directory)

		file_logs.close()
		return True
	
	def log(self, server, database, message):
		'''
			(Directory, Server, Database, string) -> (boolean)
			logs the paramaters along with a time-stamp (datetime.now() function) with 
			the _directory text file as well as the _logs class file
			
			*WILL ALSO INCREMEMENT THE COMMIT COUNTER FOR THE LOG SESSIONS*
			
			@paramaters the _directory string is a real file with the correct path
			@exception the function will throw a DirectoryNotFoundError
		'''
		current_time = datetime.now()
		line = f'<{server}<>{database}>?{current_time}?!{message}!'
		try:
			file_logs = open(self._directory, 'a')
			file_logs.write(line)
			self._logs.append(line)
			self._commits += 1
			file_logs.close()
		except:
			raise DirectoryNotFound(self._directory)
		
		return True
	
	def index(self, n):
		'''
			(Directory, int) -> (string)
			indexes the class variable _logs and returns the associative string
			
			@paramaters n >= 0 and n <= length of the log file
			@returns the logged string at index n of the entire logs for a certain directory
			@exception if the index n is invalid, will return IndexError
		'''
		try:
			return self._logs[n]
		except:
			raise IndexError
	
	def lookup(self, column, element, start=0):
		'''
			(Directory, Column, string, int*optional*) -> (string)
			looks up the column element in the logs: RUNTIME (N)
			
			@paramaters Column must be a valid enum:
					1) SERVER
					2) DATABASE
					3) TIMESTAMP
					4) MESSAGE
			@returns the entire log of the first index
					 where the column and line match
			@exception if none is found, will throw LogNotFound
					   exception to the calling file
		'''
		for i in range( start, len(self._logs) ):
			element_parsed = self.parse(self._logs[i], column)
			if (self.parse(self._logs[i], column) == element ):
				return self._logs[i]
		raise LogNotFound(self._directory)
	
	def __retr__(self):
		'''
			(Directory) -> (list of strings)
			Returns a list of strings representing the entire log file from txt
		'''
		return self._logs
	
	def __str__(self):
		'''
			(Directory) -> (string)
			Returns the a visualy apealing string representation of the Logger
		'''
		return f'Logger: file=\'{self._directory}\', pushes=\'{self._commits}\''
			
		