
class Singleton(type):
	_instances = {}

	def get(cls, *args, **kwargs):
		if cls not in Singleton._instances:
			Singleton._instances[cls] = super(Singleton, cls) \
				.__call__(*args, **kwargs)

		return Singleton._instances[cls]
