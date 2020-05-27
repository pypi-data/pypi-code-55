
import asyncio
import desktop_notify.aio as aio

loop = asyncio.get_event_loop()

server = aio.Server('keeprofi')

class Notify(aio.Notify):

	def __init__(self, *args):
		super().__init__(*args)
		self.set_server(server)

	def show(self):
		loop.run_until_complete(super().show())
