'''
Perform database opeartions on contact list and outgoing mail schedule data
'''
# Import libraries
import numpy as np
import pandas as pd
import mysql.connector

# Define global variables
DATABASE = 'tmc_lbs'
QUERY = 'SELECT first_name, email FROM staff WHERE first_name NOT IN (\'Nasi\', \'Joy\', \'Lauren\', \'Lucy\', \'Rakshita\') AND senority = \'SVP\''
TEST_QUERY = 'SELECT first_name, email FROM staff WHERE first_name = \'Yifei\''
PASSWORD = input('Please Enter Your Password\n')
TEST_MODE = False

def query(database = DATABASE, query = QUERY, password = PASSWORD, test_mode = TEST_MODE, test_query = TEST_QUERY):
	'''Query the sql database for the whole dataset'''
	cnx = mysql.connector.connect(user = 'root', database = database, password = password)
	if TEST_MODE:
		df = pd.io.sql.read_sql(test_query, con = cnx, index_col = None)
	else:
		df = pd.io.sql.read_sql(query, con = cnx, index_col = None)
	cnx.close()
	return df

