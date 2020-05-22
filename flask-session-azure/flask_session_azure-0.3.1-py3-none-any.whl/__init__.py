def storage_account_interface(connection_str: str, table_name: str = "flasksession",
                              partition_key: str = "default_session", create_table_if_not_exists: bool = True):
    """
    Creates a Session object as replacement for the default flask session
    The Session uses Azure storage accounts or Azure cosmosDB with Table API as backend
    :param connection_str: Connection string to storage account or CosmosDb with Table-API
    :param table_name: the table name. Default is "flasksession". When overwriting this, follow the table name rules
        https://docs.microsoft.com/en-us/rest/api/storageservices/Understanding-the-Table-Service-Data-Model#table-names
    :param partition_key: the partition key within the table. Use a unique partition_key if applications share a table
    :param create_table_if_not_exists: set to False if you do not want this application to create a table for you
    :return: a Flask session manager
    """
    from flask_session_azure.storage_account_session import StorageAccountSessionInterface
    return StorageAccountSessionInterface(connection_str, table_name=table_name, partition_key=partition_key,
                                          create_table_if_not_exists=create_table_if_not_exists)
