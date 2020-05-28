import logging
import time
import os
from google.cloud import bigquery
from google.cloud import pubsub
import gcp_helper


gcp_helper.setupLogger()
stage = os.environ.get('stage', 'local')
project_id = gcp_helper.get_project_id()
client = bigquery.Client(project=project_id)
destDataset = "empack_raw"
destDataset_test = "test_destination"


class fake_datasets():
	def __init__(self, error):
		self.error_result = error


def mapDatasets(datasets, mapColumns=False, filterKeys=None):
	""" Maps the  contained tables, and contained
		columns for the datesets given in projects' BigQuery.

	Args:
		datasets (LIST of STRING): A list of the dataset which
									are to be mapped
		mapColumns (BOOL): A boolean flag that indicates if
							the columns of every tables
							should be mapped or not
		filterKeys (LIST of STRING): A list of substrings,
									one of which must be included in
									the table name for the table to be
									included in the final dictionary. If
									no filterKeys are pass all tables are
									included.

	Returns:
		DICT: {"table_id": {
							"datasets": A list of names of datasets that contain this table,
							"columns": A list of lists. Each containing column names of this
										for it's respective dataset
							}}
	"""

	def targetTable(table_id, filterKeys):
		""" Determines if any of the substrings are present in the
			table_id

		Args:
			table_id (STRING): Name of table
			cfilterKeys (LIST of STRING): List of substrings

		Returns:
			BOOL: True - minimum of one substring is present in
							the table id or filterKeys is None
				False - No substrings are present in the table id
		"""
		if filterKeys is None:
			return True
		for substring in filterKeys:
			if substring in table_id:
				return True
		return False

	build = {}

	if datasets:
		for dataset in datasets:
			tables = list(client.list_tables(dataset.dataset_id))
			if tables:
				for table in tables:
					if targetTable(table.table_id, filterKeys):
						if table.table_id in build.keys():
							build[table.table_id]['datasets'].append(dataset.dataset_id)
						else:
							build[table.table_id] = {'datasets': [],
													'columns': []}
							build[table.table_id]['datasets'].append(dataset.dataset_id)
						if mapColumns:
							columns = [column.name for column in
										list(client.get_table(table).schema)]
							build[table.table_id]['columns'].append(columns)
					else:
						logging.debug("Skipping table {}".format(table.table_id))
			else:
				logging.debug("No tables found in dataset {}".format(dataset.dataset_id))
	else:
		logging.debug("No datasets found")

	return build


def buildDict(filterKeys=None, mapColumns=False, targetDatasets=None):
	""" Maps the dataset names, contained tables, and contained
		columns in the projects BigQuery.

	Args:
		filterKeys (LIST of STRING): A list of substrings,
									one of which must be included in
									the table name for the table to be
									included in the final dictionary. If
									no filterKeys are pass all tables are
									included.
		mapColumns (BOOL): A boolean flag that indicates if
							the columns of every tables
							should be mapped or not
		targetDatasets (LIST of STRING): list of dataset which are to be mapped


	Returns:
		DICT: {"table_id": {
							"datasets": A list of names of datasets that contain this table,
							"columns": A list of lists. Each containing column names of this
										for it's respective dataset,
							"masterCol": A list containing all the column names present amgonst
										instances of this table in various datasets
							}}
	"""

	def identifyCols(build):
		""" Condenses lists of lists of column names into one list containing every
			unique column name

			Args:
				Build DICT: {"table_id": {
								"datasets": A list of names of datasets that contain this table,
								"columns": A list of lists. Each containing column names of this
											for it's respective dataset
							}}

			Returns:
				DICT: {"table_id": {
									"datasets": A list of names of datasets that contain this table,
									"columns": A list of lists. Each containing column names of this
												for it's respective dataset,
									"masterCol": A list containing all the column names present amgonst
												instances of this table in various datasets
									}}
		"""
		def allColumns(colLists):
			master_list = []
			master_low = []
			for formatted_list in colLists:
				lows = [name.lower() for name in formatted_list]
				for name_low, name_formatted in zip(lows, formatted_list):
					if name_low not in master_low and name_low != 'agent':
						master_list.append(name_formatted)
						master_low.append(name_low)
			return master_list

		for key in build.keys():
			cols = allColumns(build[key]['columns'])
			build[key]['masterCol'] = cols

		return build

	start = time.time()
	datasets = list(client.list_datasets())
	if targetDatasets:
		datasets = [dataset for dataset in datasets
						if dataset.dataset_id in targetDatasets]
	if stage == 'test':
		datasets = [dataset for dataset in datasets if 'test' in dataset.dataset_id]
	logging.info("Building Dict with {} datasets".format(len(datasets)))
	logging.info("Datasets: {}".format([dataset.dataset_id for
										dataset in datasets]))

	build = mapDatasets(datasets, mapColumns, filterKeys)
	if mapColumns:
		build = identifyCols(build)

	logging.info("The function buildDict \
					needed {} seconds to complete".format(
														round(time.time() - start),
														0))

	return build


def deleteTable(dataset_id, table_id):
	""" Deletes a table from BigQuery

	Args:
		dataset_id (STRING): Name of dataset
		table_id (STRING): Name of table


	Returns:
		BOOL: True - Delete successful
			False - Delete not successful
	"""
	try:
		table_ref = client.dataset(dataset_id).table(table_id)
		client.delete_table(table_ref, not_found_ok=True)
		result = "Deleted table '{}.{}'.".format(dataset_id, table_id)
		return True, result
	except Exception as e:
		return False, e


def clearDatasets(datasets):
	""" Removes all tables in datasets

	Args:
		datasets (LIST of STRING): List containing names of datasets to be cleared

	Returns:
		None
	"""
	for dataset in datasets:
		tables = list(client.list_tables(dataset.dataset_id))
		for table in tables:
			table_ref = client.dataset(dataset.dataset_id).table(table.table_id)
			client.delete_table(table_ref)


def listDatasets():
	""" Returns a list of the names of all the datasets in the projects BigQuery

	Args:

	Returns:
		datasets (LIST of STRING): List containing names of datasets
	"""
	datasets = list(client.list_datasets())
	return datasets


def createDataset(name):
	""" Creates a new dataset in BigQuery if it does not
		already exists

	Args:
		name (STRING): Name of the new dataset

	Returns:
	"""
	current_sets = [dataset.dataset_id for dataset in listDatasets()]
	if name not in current_sets:
		dataset = bigquery.Dataset(f"{project_id}.{name}")
		dataset = client.create_dataset(dataset)  # Make an API request.
		logging.info(f"Created dataset {client.project}.{dataset.dataset_id}")
	else:
		logging.info(f"Dataset {name} already exists")


def buildSQL(key, build):
	""" Creates a SQL query that will UNION ALL the various instances of the table

	Args:
		key (STRING): table name (key to build dictionary)
		build (DICT): {"table_id": {
							"datasets": A list of names of datasets that contain this table,
							"columns": A list of lists. Each containing column names of this
										for it's respective dataset,
							"masterCol": A list containing all the column names present amgonst
										instances of this table in various datasets
							}}


	Returns:
		STRING: An SQL query that will UNION ALL the tables in various
				datasets defined in the build dictionary
	"""
	def buildFields(masterCols, columns):
		""" For each entry in masterCols the function returns a string to be added
			to the master query. In the case where the column exists in the particular
			dataset the function add the name and a comma. In the case where the column
			does not exists in the particular dataset the function add a NULL as __ so
			that the value NULL appears in the final table

			Args:
				masterCol (STRING): A list containing all the column names present amgonst
									instances of this table in various datasets
			Returns:
				STRING: A string containing all the column names correctly formatted for
						the final sql query
		"""
		sql = ''
		for c in masterCols:
			if c in columns:
				sql += '{},\n'.format(c)
			else:
				sql += "NULL as {},\n".format(c)
		return sql[:-2]

	viewName = key.replace('_V0', '')
	dataset = destDataset_test if 'test' in key else destDataset
	master_sql = "CREATE OR REPLACE TABLE `{}.{}.{}` AS \n".format(project_id,
																	dataset,
																	viewName)
	for i, agent in enumerate(build[key]['datasets']):
		fields = buildFields(build[key]['masterCol'],
						build[key]['columns'][i])
		sql_shell = "SELECT \n{},\n'{}' as Agent \nFROM `{}.{}.{}`"
		sql = sql_shell.format(fields, agent, project_id, agent, key)
		master_sql += sql + '\nUNION ALL\n'

	master_sql = master_sql[:-11] + ';'
	logging.debug(master_sql)

	return master_sql


def executeQuery(master_sql):
	""" Executes Bigquery job and waits for it to finish

	Args:
		master_sql (STRING): SQL query
	Returns:
		jobObject (OBJECT): Object containing response from BigQuery
	"""
	try:
		jobObject = client.query(master_sql)
		while jobObject.running():
			time.sleep(1)
	except Exception as e:
		jobObject = fake_datasets(str(e))

	return jobObject


def startQuery(master_sql):
	""" Executes Bigquery job

	Args:
		master_sql (STRING): SQL query
	Returns:
		jobObject (OBJECT): Object containing response from BigQuery
	"""
	try:
		jobObject = client.query(master_sql)
	except Exception as e:
		jobObject = fake_datasets(str(e))

	return jobObject


def checkQuery(jobObject):
	""" Waits for job to finish running

	Args:
		jobObject (OBJECT): Object containing response from BigQuery
	Returns:
		jobObject (OBJECT): Object containing response from BigQuery
	"""
	while jobObject.running():
		time.sleep(1)
	return jobObject


def stream(table, rows_to_insert, unique_ids):
	""" Streams rows as an insert to BigQuery
	Args:
		table (STRING): Object containing response from BigQuery
		rows_to_insert (LIST of DICT): List of dictionaries containing table
										columns and their values to be written
	"""

	row_ids = []
	for row in rows_to_insert:
		idx = ''
		for col in unique_ids:
			idx += str(row[col]) + '_'
		row_ids.append(idx[:-1])
	logging.info("BigQuery Streaming indexIds/uniqueIds/row_ids: {}".format(row_ids))

	errors = client.insert_rows_json(table, rows_to_insert, row_ids=row_ids)
	if errors == []:
		return True
	else:
		raise Exception(errors)
		return False

def get_table(table):
	""" Returns table object
	Args:
		table (STRING): table name
	Returns:
		 (OBJECT): BigQuery object for table
	"""
	return client.get_table(table)
