import logging
import os
from base64 import urlsafe_b64encode, b64decode, urlsafe_b64decode
import json
from google.cloud import pubsub

#stage = os.environ.get('stage', 'dev')
#logging.debug("Stage: {}".format(stage))


def createPublisher(project_id, stage, topic):
	""" Gets publisher object and event type object for a
		given topic

		Args:
			topic (STRING): target topic
		Returns:
			publi	publisher.get_topic(event_type)
	logging.info('Using pub/sub topic {} {}'.format(project, topic))sher (OBJECT): A handle to publish messages to the topic
								(See GCP documentation)
			event_type (OBJECT): A handle for the type of events that can
								be published (See GCP Documentation)
	"""
	publisher = pubsub.PublisherClient()
	topic = "{}_{}".format(topic, stage)
	#project = os.environ.get('PROJECT', 'calcium-complex-272115')
	event_type = publisher.topic_path(project_id, topic)

	publisher.get_topic(event_type)
	logging.info('Using pub/sub topic {} {}'.format(project_id, topic))

	return publisher, event_type


def encodeMessage(data):
	""" encodes message with b64encode

		Args:
			data (DICT): Dictionary to be encoded

		Returns:
			STRING: encoded dictionary
	"""
	return urlsafe_b64encode(bytearray(json.dumps(data), 'utf8'))


def publishMessage(publisher, topic_path, data):
	""" Publishes message to pubsub

		Args:
			publisher (OBJECT): A handle to publish messages to the topic
								(See GCP documentation)
			topic_path (STRING): target topic
			data (STRING): Message to be published
		Returns:
			STRING: encoded dictionary
	"""
	event_data = encodeMessage(data)
	publisher.publish(topic_path, event_data)


def decodeMessage(event):
	""" dencodes message with b64encode
		Args:
			event (STRING): String to be decoded
		Returns:
			DICT: dencoded data
	"""
	try:
		data = b64decode(event).decode('utf-8')
		data = urlsafe_b64decode(data).decode('utf-8')
	except:
		data = event.decode('utf-8')
	return json.loads(data)
