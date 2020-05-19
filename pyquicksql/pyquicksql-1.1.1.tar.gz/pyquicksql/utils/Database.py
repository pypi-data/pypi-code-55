class Database:
	def __init__(self, _name, _table, _autocommit):
		'''
			(Name, string, int) -> None
			initializes a new database class to be inputed into a connect class
			
			@paramaters a Name enum (MYSQL, SQLITE) must be at least specified
			@exception the default type will be set to MYSQL as it is the more popular choice
			
			** The values cannot be changed, a new database should be create each time **
		'''
		self._name = _name
		self._table = _table
		self._autocommit = _autocommit
	def getName(self):
		'''
			(Database) -> (Name)
			the getter function for the database name string
		'''
		return self._name
	def getTable(self):
		'''
			(Database) -> (string)
			the getter function for the table name string
		'''
		return self._table
	def getAutocommit(self):
		'''
			(Database) -> (boolean)
			the getter function for the boolean value of the autocommit for the table
		'''
		return self._autocommit
	def __eq__(self, other):
		'''
			(Database) -> (boolean)
			compares the current class to other on a basis of the database and table string names
		'''
		if ( self._name != other._name ):
			return False
		if ( self._table != other._table ):
			return False
	def __repr__(self):
		'''
			(Database) -> (string)
			Returns a string representation of the Database class structure
		'''
		return f'Database({self._name}, {self._table}, {self._autocommit})'
	def __str__(self):
		'''
			(Database) -> (string)
			Returns the a visualy apealing string representation of the Database.
		'''
		return f'Database: {self._name} -> Table: {self._table} ({self._autocommit})'