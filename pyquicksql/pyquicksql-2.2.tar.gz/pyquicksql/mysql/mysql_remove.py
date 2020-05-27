from pyquicksql.utils.sql_errors import *
from pyquicksql.utils.sql_enums import *

from pyquicksql.mysql import mysql_lookup

import pymysql as sql

def commit(data_required, data_specific, column, element):
	'''
		(list of strings, list of strings, string, string) -> (boolean)
		@conditions valid data_required and data_specific list of strings must be passed as
					arguments to the fucntion in acordance to the outlines bellow. Furthermore,
					a valid column and element must be entered as arguments to the function.
		@returns True if the element was sucesfully removed form the specified column of a 
				 pre-existing row to the database without interuption.
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
	#we want to check to make sure the id is stored in the first place
	#otherwise it is pointless and inefficient to run through the sql
	#procedures for removing the id: aka. fail-safe for future bad programming
	#or steps not-taken into account when this is legacy code
	if (mysql_lookup.retreive(data_required, data_specific, column, column, element) == ''):
		return False
	
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
			#command is as follows: where we find that the ip-address which
			#the command is received from, delete that row and it's data from
			#the sql database: we want to offer the ability to remove all cached
			#data to keep anoniminity and user-privacy secured
			s = f"DELETE FROM {data_specific.getTable()} WHERE {column} = \'{element}\';"
			cursor.execute(s)
			connection.commit()
			#while no changes are being made, make sure that the connection to
			#the sql server is closed and not left hanging (unforseen errors)
			connection.close()
	except:
		raise ElementNotFound()
		return False
	finally:
		#in the event the code is run safley and without bugs or errors; it is safe to
		#assume and return to the main logical flow that the appropriate requested data
		#has been removed from the coresponding database table
		return True