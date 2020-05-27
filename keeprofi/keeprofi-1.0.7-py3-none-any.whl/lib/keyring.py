
import keyring
import datetime
import re

import keeprofi

class Keyring(metaclass = keeprofi.Singleton):

	def __init__(self):
		self.setting = keeprofi.Settings.get().remember_pass
		self.check_pass()

	def check_pass(self):
		if (isinstance(self.setting, str)):
			match = re.match(
				r'^(?:(\d+)W)?(?:(\d+)D)?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)??$',
				self.setting
			)
			td = datetime.timedelta(
				weeks   = int(match.group(1) or 0),
				days    = int(match.group(2) or 0),
				hours   = int(match.group(3) or 0),
				minutes = int(match.group(4) or 0),
				seconds = int(match.group(5) or 0)
			)
			now = datetime.datetime.now()
			passdt = datetime.datetime.fromtimestamp(
				self.cache.keyring_timestamp
			)

			if (now - passdt > td):
				self.delete_pass()


	def get_pass(self):
		return (
			lambda: None,
			lambda: keyring.get_password('keeprofi', 'kdb')
		)[bool(self.setting)]()

	def save_pass(self, password: str):
		if (self.setting):
			keyring.set_password('keeprofi', 'kdb', password)

			self.cache.keyring_timestamp = datetime.datetime.now().timestamp()

	def delete_pass(self):
		self.cache.keyring_timestamp = 0

		try:
			keyring.delete_password('keeprofi', 'kdb')
			return True
		except Exception as e:
			return False

	@property
	def cache(self):
		if (not hasattr(self, '_cache')):
			self._cache = keeprofi.Cache.get()

		return self._cache


