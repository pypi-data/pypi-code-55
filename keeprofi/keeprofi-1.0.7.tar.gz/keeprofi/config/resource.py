
import json
from pathlib import PosixPath

import keeprofi

class Resource(metaclass = keeprofi.Singleton):

	def __init__(self):
		self.path.parent.mkdir(
			parents = True,
			exist_ok = True
		)
		self._dict = self.load()
		self._file = self.path.open('w')
		self._init_setter()

	def load(self):
		settings = self.defaults

		if (self.path.is_file()):
			with self.path.open() as f:
				try:
					settings = json.load(f)
				except Exception as e:
					pass

		return settings

	def _init_setter(self):
		def setattr(name, value):
			self._dict[name] = value

		self.__setattr = setattr

	@property
	def defaults(self):
		return {}

	@property
	def path(self) -> PosixPath:
		pass

	def __getattr__(self, name):
		if (name in self._dict):
			return self._dict[name]
		elif (name in self.defaults):
			return self.defaults[name]

		raise AttributeError(name)

	def __setattr__(self, name, value):
		self.__setattr(name, value)

	def __setattr(self, name, value):
		self.__dict__[name] = value

	def __delattr__(self, name):
		if (name in self._dict):
			del self._dict[name]
		else:
			raise AttributeError(name)

	def save(self):
		self._file.seek(0)
		self._file.truncate()
		json.dump(self._dict, self._file, indent='\t')

	def __del__(self):
		self.save()
		self._file.close()
