from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class Event:

	def __init__(self, data):
		for item in data.items():
			if hasattr(self, item[0]):
				setattr(self, item[0], item[1])

	def _broadcast_on(self):
		return []

	def _get_public_attrs(self):
		return tuple(name for name in dir(self) if not name.startswith('_'))

	def _broadcast_as(self):
		return self.__class__.__name__

	def _access(self, user):
		return True

	def _dispatch(self):
		channels = self._broadcast_on()
		attrs = self._get_public_attrs()

		data = dict()

		for attr in attrs:
			data[attr] = getattr(self, attr)

		data['type'] = 'event'
		data['event'] = self._broadcast_as()

		for channel in channels:
			data['channel'] = channel
			async_to_sync(channel_layer.group_send)(
				channel,
				data
			)