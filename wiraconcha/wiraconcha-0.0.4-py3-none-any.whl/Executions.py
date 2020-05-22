import os
import sys
import logging
import json

import bigQuery_helper
import pubsub_helper



class Execution():
	"""
	A class used to represent a BigQuery job Execution

	Attributes
	----------
	jobObject : OBJECT
				The object returned from the BigQuery execution command
	key : STRING
			The respective key in the build dictionary (Also the table name)
	master_sql : STRING
			The SQL statement exectued
	datasets : LIST of STRING
			A list of the datasets where the table (key) is present
	publisher: OBJECT
			The publisher client for a pubsub topic
	topic_path:
			The target topic for errors in the execution of a job

	Methods
	-------
	assign_jobObject(self, jobObject)
		assigns jobObject

	assign_key(self, key)
		assigns key

	assign_master_sql(self, master_sql)
		assigns master_sql

	assign_datasets(self, datasets)
		assigns datasets

	wait_running(self)
		Waits for BigQuery job to finish executing

	evaluateJob(self)
		Checks for errors in the BigQuery jobObject. Sends any
			found errors to the DeadQ via pubsub

	start_job(self)
		Starts a BigQuery job by running the master_sql
	"""

	def __init__(self, jobObject=None,
						key=None,
						master_sql=None,
						datasets=None,
						publisher=None,
						topic_path=None):
		self.jobObject = jobObject
		self.key = key
		self.master_sql = master_sql
		self.datasets = datasets
		self.publisher = publisher
		self.topic_path = topic_path
		logging.info("Execution object {key} created")

	def assign_jobObject(self, jobObject):
		# assigns jobObject
		self.jobObject = jobObject

	def assign_key(self, key):
		# assigns key
		self.key = key

	def assign_master_sql(self, master_sql):
		# assigns master_sql
		self.master_sql = master_sql

	def assign_datasets(self, datasets):
		# assigns datasets
		self.datasets = datasets

	def assign_publlisher(self, publisher):
		# assigns publisher
		self.publisher = publisher

	def assign_topic_path(self, topic_path):
		# assigns topic_path
		self.topic_path = topic_path

	def wait_running(self):
		""" Waits for BigQuery job to finish executing
		Args:
		Returns:
		"""
		logging.debug("Waiting for {}".format(self.key))
		self.jobObject = bigQuery_helper.checkQuery(self.jobObject)

	def evaluateJob(self):
		""" Checks for errors in the BigQuery jobObject. Sends any
			found errors to the DeadQ via pubsub.

		Args:

		Returns:
			INT: 0 or 1 to indicate if the query was
				 executed without/with error
		"""
		def write_data(error):
			""" Writte error event to pubsub
			Args: error (STRING): a string containing the error message
			Returns:
			"""
			logging.critical("Error with table {}".format(self.key))
			data = {
					"table": self.key,
					"datasets": self.datasets,
					"error": json.dumps(error),
					"sql": self.master_sql}
			pubsub_helper.publishMessage(self.publisher, self.topic_path, data)
			logging.critical("Published to {} event_data: {}".format(self.topic_path,
																		data))

		try:
			self.wait_running()
			if self.jobObject.error_result:
				write_data(self.jobObject.error_result)
				output = 1
			else:
				logging.info("Table {} Successful".format(self.key))
				output = 0
		except Exception as e:
			write_data(e.__str__())
			output = 1


		return output, self.jobObject

	

	def start_job(self):
		""" Starts a BigQuery job by running the master_sql
		Args:
		Returns:
		"""
		if self.master_sql is None:
			logging.critical("master_sql in None")
			raise Exception
		self.jobObject = bigQuery_helper.startQuery(self.master_sql)
		logging.info("Job Started")
