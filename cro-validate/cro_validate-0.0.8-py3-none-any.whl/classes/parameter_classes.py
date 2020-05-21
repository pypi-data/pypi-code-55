from cro_validate.classes.configuration_classes import Config


class Index(dict):
	def __getattr__(self, name):
		resolved = Config.parameter_name_resolver.resolve(self, name)
		if resolved is None:
			if not Config.parameter_name_resolver.is_nullable(self, name):
				raise Config.exception_factory.create_input_error(name, 'Unresolved name.')
			return None
		result = self[resolved]
		return result

	def __setattr__(self, name, value):
		self[name] = value

	def ensure(index):
		if index is None:
			return Index()
		return index

