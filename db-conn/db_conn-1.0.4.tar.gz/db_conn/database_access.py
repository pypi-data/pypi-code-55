import json


def get_database_access(path=None):
    """
    Put a json file at your home directory:
    "~/access_information.json"
    {
        "database_name": {
            "host": "database-db.host.net",
            "user": "user",
            "password": "1234",
            "database": "database_name",
            "port": 5432
        },
    }
    Parameters
    ----------
    :path: recieves access_information.json path
    """
    
    database_file_name = '~/access_information.json' if path == None else path
    with open(database_file_name, "r") as database_file:
        database_access = json.load(database_file)
    return database_access
