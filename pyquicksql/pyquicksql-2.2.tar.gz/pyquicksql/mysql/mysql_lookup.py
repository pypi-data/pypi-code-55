from pyquicksql.utils.sql_errors import *
from pyquicksql.utils.sql_enums import *

import pymysql as sql

def retreive(data_required, data_specific, unknown_column, known_colum, known_element):
	'''
		(list of strings, list of strings, string, string, string) -> (string)
		@conditions valid data_required and data_specific list of strings must be passed as
					arguments to the fucntion in acordance to the outlines bellow. Furthermore,
					a valid know/unknown column and known_data must be entered as arguments to
					the function.
		@returns the data associated with the unknown_column that is found within the row of the
				 known colum and known data.
		@exception if invalid input was encountered, the function will return False with the assumption
				   there is a failure to acknowledge or follow the outlines by the docstrings above
				
			*** SHARED AMONGST VARIOUS DATABASE CALLS : ONE SERVER (MOST LIKELY) ***
			data_required = [ =
				0 : IP ADDRESS OF DATABASE
				1 : PORT OF DATABASE
				2 : USERNAME FOR DB ACESS
				3 : PASSWORD FOR DB ACESS
			]
		
			*** NOT SPECIFIC TO VARIOUS CALLS : HIGH LIKELYHOOD FOR VARIATIONS AMONGST CALLS ***
			data_specific = [
				0 : AUTOCOMMIT (BOOL)
				1 : DB NAME
				2 : DB TABLE NAME
			]
	'''
	connection = sql.connect(
		host = data_required.getIP(),
		port = data_required.getPort(),
		user = data_required.getAccount()[0],
		passwd = data_required.getAccount()[1],
		autocommit = (data_specific.getAutocommit() == 'True'),
		db = data_specific.getName(),
	)
	try:
		with connection.cursor() as cursor:
			#from the table user_lookup, find the data entry where the colum is
			#'ipaddr' representing ip addresses on the database, and retreive the
			#associated user-id found in the row of the given ip-address
			s = f"SELECT {unknown_column} FROM {data_specific.getTable()} WHERE {known_colum} = \'{known_element}\';"
			cursor.execute(s)
			data = cursor.fetchone() #fetch the ipaddress associated with the userid **DO NOT REMOVE**
			#while no changes are being made, make sure that the connection to
			#the sql server is closed and not left hanging (unforseen errors)
			connection.close()
	except:
		raise ElementNotFound()
		return '' #in the case of a total crash, still return an empty string
	finally:
		#we are subscripting a list of two pieces of data, though in the case of an error, there may be
		#a return type of None, incase the except is bypassed return an empty string representing that
		#no id could be associated, otherwise subscript the id-address which is the only useful data
		try:
			return data[0]
		except:
			return ''