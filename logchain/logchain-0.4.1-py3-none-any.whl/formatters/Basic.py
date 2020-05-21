import logging
from datetime import datetime, timezone
from types import SimpleNamespace

import hashlib
import hmac


class Basic(logging.Formatter):
	"""
	Base model for all custom formatters.
	"""
	def __init__(self, params):

		self.secret = params["secret"]
		self.prevLine = params["seed"]

		format = params.get("format", "%(timestamp)s %(levelLetters)s %(fileLine)-15s %(funcName)-15s %(message)-60s |%(signature)s")
		# Have a check for presence of signature ?
		logging.Formatter.__init__(self, fmt = format)
		tsParams = {"fmt": "iso", "utc": False, "precision": "milliseconds"}
		tsParams.update(params.get("timestamp", {}))
		self.timestamp = SimpleNamespace(**tsParams)
		self.context = {}


	def format(self, record):
		"""
		Shared method where the block-chain part is coded.
		"""
		record.signature = Basic.sign(self.prevLine, self.secret)
		record.levelLetters = record.levelname[:4]
		record.fileLine = record.filename  + ':' + str(record.lineno)
		record.timestamp = self.makeTimestamp(record)

		logLine = self.stringify(record)
		self.prevLine = logLine
		return logLine


	def makeTimestamp(self, record):
		"""
		Because formatTime called internally by logging.Formatter.format,
		we prefer a custom timestamp generation + an explicit `timestamp` name.
		We can customize the timezone, the decimal separator and number of digits.
		"""
		ts = datetime.fromtimestamp(record.created)

		if self.timestamp.utc:
			ts = ts.astimezone(tz = timezone.utc).replace(tzinfo = None)

		if self.timestamp.fmt == "iso":
			return ts.isoformat(sep = ' ', timespec = self.timestamp.precision)
		else:
			# Custom format can have a precision to the microseconds.
			aTrunc = None
			if self.timestamp.fmt.endswith("%f") and self.timestamp.precision == "milliseconds":
				aTrunc = -3

			return ts.strftime(self.timestamp.fmt)[:aTrunc]


	def stringify(self, record):
		"""
		Specific method to transform the recod to string.
		"""
		return logging.Formatter.format(self, record)

	@staticmethod
	def sign(iMessageStr, iSecretStr, iLength = 16):
		"""
		Generates a truncated signature of the input message.
		@param iLength: controls the size of the signature, set it to None for full length.
		"""
		msg = bytes(iMessageStr, "utf-8")
		key = bytes(iSecretStr,  "utf-8")
		return hmac.new(key, msg, hashlib.sha256).hexdigest()[:iLength]

	@staticmethod
	def extractSignature(line):
		return line[line.rindex('|') + 1:]

	def setField(self, **kwargs):
		# Keep previous for scoped restoration
		previousCtx = {**self.context}
		self.context.update(kwargs)

		# Purge None values
		self.context = {k:v for k,v in self.context.items() if v is not None}
		return previousCtx
