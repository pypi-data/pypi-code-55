from pyquicksql.utils.sql_errors import *
from pyquicksql.utils.sql_enums import *
import sqlite3 as sql

def commit(data_required, data_specific, unknown_data, known_data):
	'''
		(list of strings, list of strings, list of strings, list of strings) -> (boolean)
		@conditions valid data_required and data_specific list of strings must be passed as
					arguments to the fucntion in acordance to the outlines bellow. Furthermore,
					columns and elements must be of length 1 (one) and all doc-string types must
					be followed to ensure the function runs without bugs.
		@returns True if the elements were sucesfully appended to the columns of pre-existing rows,
				 otherwise if one of the elements is pre-existing, the elements have been appeneded
				 to the database without interuption.
		@exception if invalid input was encountered, the function will return False with the assumption
				   there is a failure to acknowledge or follow the outlines by the docstrings above
				
			*** SHARED AMONGST VARIOUS DATABASE CALLS : ONE SERVER (MOST LIKELY) ***
			data_required = [
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
			
			unknown_data = [
				0 : column
				1 : element
			]
			
			known_data = [
				0 : column
				1 : element
			]
			
			*** GENERIC SQL QUERY TO MODIFY THE DATA WITHIN THE LOCAL SERVERS DATABASE ***
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
			#the above code defines the type of request made to the sql server, depending
			#on whether the ipaddress has an associated id or not, hence we execute it now
			s = 'UPDATE \'{data_specific.getTable()}\' SET {unknown_data[0]} = \'{unknown_data[1]}\ WHERE {known_data[0]} = \'{known_data[1]}\';'
			cursor.execute(s)
			#while no changes are being made, make sure that the connection to
			#the sql server is closed and not left hanging (unforseen errors)
			cursor.close()
	except:
		raise ElementNotFound()
		return False
	finally:
		#in the event the code is run safley and without bugs or errors; it is safe to
		#assume and return to the main logical flow that the appropriate requested data
		#has been added or modified on the servers sql database
		return True