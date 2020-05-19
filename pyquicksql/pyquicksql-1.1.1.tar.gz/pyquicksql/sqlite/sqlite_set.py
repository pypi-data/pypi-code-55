from pyquicksql.utils.sql_errors import *
from pyquicksql.utils.sql_enums import *
import sqlite3

def commit(data_required, data_specific, columns, elements):
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
	'''
	connection = sql.connect(
		host = data_required.getIP(),
		port = data_required.getPort(),
		user = data_required.getAccount()[0],
		passwd = data_required.getAccount()[1],
		autocommit = (data_specific.getAutocommit() == 'True'),
		db = data_specific.getName(),
	)
	
	#check to see if the information exists
	check = query_lookup.retreive(data_required, data_specific, column, column, element)
	if (check == ''): #if not, input the values like a new entry
		#in the table 'user_lookup' enter a new row of data acording to the respective
		#colums of id (user-id) and ipaddr(the ip-address that is requesting to be
		#associated globaly with that user-id amongst all users in the networks)
		s = f"INSERT INTO {data_specific.getTable()} VALUES ({','.join(columns)}) VALUES ('{', '.join(elements)}');"
	else: #else, make modifications to already existing data for the associated ip
		#IF THE ID ALREADY EXISTS (We would arrise problems if we have repeated data
		#in the sql table so we need to AVOID THIS AT ALL COSTS) aka. where we find
		#the same ip-address' row in the database update the old user-id with the new
		#one requested by the user
		return False

	try:
		with connection.cursor() as cursor:
			#the above code defines the type of request made to the sql server, depending
			#on whether the ipaddress has an associated id or not, hence we execute it now
			cursor.execute(s)
			#while no changes are being made, make sure that the connection to
			#the sql server is closed and not left hanging (unforseen errors)
			cursor.close()
	except:
		raise ElementAlreadyExists()
		return False
	finally:
		#in the event the code is run safley and without bugs or errors; it is safe to
		#assume and return to the main logical flow that the appropriate requested data
		#has been added or modified on the servers sql database
		return True