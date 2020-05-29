""" This module defines all exergi functions within the AWS.postgreSQL module"""

def config(filePath: str ='database.ini', section: str ='postgresql')-> dict:
    """ The following config() function reads in the database.ini file and 
    returns the connection parameters as a dictionary. This function will be 
    imported in to the main python script. 
    
    This file was adapted from 
    http://www.postgresqltutorial.com/postgresql-python/connect/
    
    Arguments:
        - filePath      - Location of the "database.ini" required to initiate
                          connection
        - section       - Section of the "database.ini" file where the 
                          connection-parameters are stored
    Returns:
        - db            - All connection parameters in the specified filePath   
                          and section
    """

    from configparser import ConfigParser

    parser = ConfigParser()   # Create a parser
    parser.read(filePath)     # Read config file
    db = {} # Get section, default to postgresql
    
    # Checks to see if section (postgresql) parser exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    
    # Returns an error if a parameter is not listed in the initialization file
    else:
        raise Exception(f'Section {section} not found in the {filePath} file')
    return db

def checkPostgreSQLConnection(params: dict):
    """A function that checks connection settings and version of postgreSQL
    
    Arguments:
        - params        - Connection parameters from config file
    """

    import psycopg2

    try:
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        
        # Print PostgreSQL Connection properties
        print (connection.get_dsn_parameters(),"\n")  
        
        # Print PostgreSQL version
        cursor.execute("SELECT version();")           
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
        # Closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
def importDataFromPostgreSQL(sql_query: str,params: dict):
    """A function that takes in a PostgreSQL query and outputs a pandas database 
    
    Arguments:
        - sql_query     - SQL-query to run
        - params        - Connection parameters from config file
    Returns:
        - df            - DataFrame with Loaded Data
    """

    import psycopg2
    import pandas as pd

    try:
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        df = pd.read_sql_query(sql_query, connection)
        
        # Convert pandas dtype="object" columns to pd.StringDtype()
        for col in df.select_dtypes("object").columns:
            df[col] = df[col].astype(pd.StringDtype())
            
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return df