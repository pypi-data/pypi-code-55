##########################################
#	Known Encounterable Errors
##########################################

class ElementNotFound(Exception):
	def __init__(self, SQLElements):
		Exception.__init__(self, f"Database Error: could not find an element with the given paramaters: {SQLElements}")
		self.SQLElements = SQLElements
	
class ElementAlreadyExists(Exception):
	def __init__(self, SQLElements):
		Exception.__init__(self, "Database Error: while attempting to push to the database, one was found with the params: {SQLElements}")
		self.SQLElements = SQLElements

##########################################
#	Ambigous SQL Errors
##########################################	

class ConnectionError(Exception):
	def __init__(self, SQLElements):
		Exception.__init__(self, "Database Error: there was an error while atempting to modify a set of data")
		self.SQLElements = SQLElements