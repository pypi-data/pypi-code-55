##########################################
#		Generic Logger Errors
##########################################

class DirectoryNotFound(Exception):
	def __init__(self, directory):
		Exception.__init__(self, f"Logger Error: the file in _directory is error-prone\nProvided with: {directory}")
		self.directory = directory

class LogNotFound(Exception):
	def __init__(self, directory):
		Exception.__init__(self, f"Logger Error: the log element requested in _directory does not exist\nProvided with: {directory}")
		self.directory = directory
		
##########################################
#		Logger Markup Errors
##########################################

class MarkupSyntaxError(Exception):
	def __init__(self, text):
		Exception.__init__(self, f"Markup Language Error: the provided text does not follow the logger syntax : {text}")