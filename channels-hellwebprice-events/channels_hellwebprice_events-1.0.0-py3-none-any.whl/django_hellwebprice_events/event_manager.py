from importlib import import_module

from django_hellwebprice_events.conf import settings
EVENTS = import_module(settings.BROADCAST_EVENTS)

def dispatch(event, data, user):
	try:
		event = getattr(EVENTS, event)(data)
		if event._access(user):
			event._dispatch()
	except:
		pass