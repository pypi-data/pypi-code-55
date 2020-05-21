import json
from .Basic import Basic

class Json(Basic):

	def __init__(self, params):
		"""
		Possible fields are: [
			'msg',
			'levelno', 'levelname',
			'module',
			'pathname',
			'filename',
			'lineno',
			'funcName',
			'exc_info', 'exc_text',
			'stack_info',
			'created', 'msecs', 'relativeCreated',
			'thread', 'threadName',
			'process', 'processName',
			'signature', 'timestamp', 'levelLetters', 'fileLine'
		]
		"""
		super().__init__(params)

		defaultFields = {"signature", "timestamp", "levelno", "fileLine", "msg",
		                 "process", "processName", "thread", "threadName"}

		self.fields = params.get("fields", defaultFields) | params.get("extraFields", set())


	def stringify(self, record):
		subRecord = {f: record.__dict__[f] for f in self.fields}
		subRecord.update(self.context)
		subRecord = {key: subRecord[key] for key in sorted(subRecord.keys())}
		return json.dumps(subRecord, ensure_ascii = False)

	@staticmethod
	def extractSignature(line):
		return json.loads(line)["signature"]

