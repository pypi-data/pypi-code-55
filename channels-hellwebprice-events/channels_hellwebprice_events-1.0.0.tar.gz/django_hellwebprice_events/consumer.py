from .conf import settings
from .event_manager import dispatch
from channels_presence.models import Room
from channels_redis.core import RedisChannelLayer
import random

import string

from importlib import import_module

from django.urls.resolvers import RoutePattern

from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


try:
	channel_keys = import_module(settings.BROADCAST_ROUTES).urlpatterns
except:
	channel_keys = {}


class WSConsumer(JsonWebsocketConsumer):

	async def all_group_discard(self, channel):
		random_string = ''.join([random.choice(string.ascii_letters) for n in range(12)])
		async with channel_layer.connection(channel_layer.consistent_hash(random_string)) as connection:
			cur = b'0'
			while cur:
				cur, keys = await connection.scan(cur, match=channel_layer._group_key('*').decode('utf-8'))
			for key in keys:
				await connection.zrem(key, channel)

	def connect(self):
		self.accept()

	def disconnect(self, code):
		async_to_sync(self.all_group_discard)(self.channel_name)

	def receive_json(self, content):
		if 'event' in content:
			event = content.pop('event')
			if event == 'subscribe':
				if 'channel' in content:
					self.subscribe(content['channel'])
			elif event == 'unsubscribe':
				if 'channel' in content:
					self.unsubscribe(content['channel'])
			else:
				self.dispatch_event(event, content)

	def subscribe(self, channel):
		match = None
		for channel_key in channel_keys.keys():
			match = RoutePattern(channel_key).match(channel)
			if match:
				data = [self.scope['user']]
				result = channel_keys[channel_key](*data, **match[2])
				if result:
					if isinstance(result, bool):
						self.group_add(channel)
					else:
						self.group_add(channel, result)
				return None
		self.group_add(channel)

	def group_add(self, channel, result=None):
		if result:
			async_to_sync(self.channel_layer.group_send)(
				channel,
				{
					'type': 'user_connect',
					'user': result,
							'channel': channel
				}
			)
		async_to_sync(self.channel_layer.group_add)(
			channel,
			self.channel_name
		)
		Room.objects.add(channel, self.channel_name, self.scope['user'])

	def unsubscribe(self, channel):
		async_to_sync(self.channel_layer.group_discard)(
			channel,
			self.channel_name
		)
		Room.objects.remove(channel, self.channel_name)
		for channel_key in channel_keys.keys():
			match = RoutePattern(channel_key).match(channel)
			if match:
				data = [self.scope['user']]
				result = channel_keys[channel_key](*data, **match[2])
				if not isinstance(result, bool):
					async_to_sync(self.channel_layer.group_send)(
						channel,
						{
							'type': 'user_disconnect',
							'user': result,
									'channel': channel
						}
					)

	def dispatch_event(self, event, data):
		dispatch(event, data, self.scope['user'])

	def event(self, content):
		self.send_json(content)

	def user_connect(self, content):
		self.send_json(content)

	def user_disconnect(self, content):
		self.send_json(content)
