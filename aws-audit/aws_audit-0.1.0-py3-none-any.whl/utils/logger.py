# Set environment (LAMBDA_APP_ENV variable) before importing logger.py
# For e.g.:
# import os
# os.environ['LAMBDA_APP_ENV'] = 'debug'

import logging
import sys
import os

class Logger():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel("ERROR") #DEBUG

		# Add logging handler to print the log statement to standard output device
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('[%(asctime)s] p%(process)s %(levelname)s - %(message)s','%m-%d %H:%M:%S')

		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

	def debug(self, msg, *args, extra=None, **kwargs):
		"""
		Log 'msg % args' with severity 'DEBUG'.

		To pass additional context, use keyword argument extra with a json value, e.g.

		logger.debug("Begin processing %s", "AWS request")
		"""
		if extra is None:
			self.logger.debug(msg, *args, extra={}, **kwargs)

		else:
			self.logger.debug(msg, *args, extra=extra, **kwargs)

	def info(self, msg, *args, extra=None, **kwargs):
		"""
		Log 'msg % args' with severity 'INFO'.

		To pass additional context, use keyword argument extra with
		a json value, e.g.

		logger.info("Begin processing %s", "AWS request")
		"""
		if extra is None:
			self.logger.info(msg, *args, extra={}, **kwargs)

		else:
			self.logger.info(msg, *args, extra=extra, **kwargs)

	def warning(self, msg, *args, extra=None, **kwargs):
		"""
		Log 'msg % args' with severity 'WARNING'.

		To pass additional context, use keyword argument extra with
		a json value, e.g.

		logger.warning("Begin processing %s", "AWS request")
		"""
		if extra is None:
			self.logger.warning(msg, *args, extra={}, **kwargs)

		else:
			self.logger.warning(msg, *args, extra=extra, **kwargs)

	def error(self, msg, *args, extra=None, **kwargs):
		"""
		Log 'msg % args' with severity 'ERROR'.

		To pass additional context, use keyword argument extra with
		a json value, e.g.

		logger.error("Begin processing %s", "AWS request" )
		"""
		if extra is None:
			self.logger.error(msg, *args, extra={}, **kwargs)

		else:
			self.logger.error(msg, *args, extra=extra, **kwargs)

	def exception(self, msg, *args, extra=None, exc_info=False, **kwargs):
		"""
		Log 'msg % args' with severity 'EXCEPTION'.

		To pass additional context, use keyword argument extra with
		a json value, e.g.

		logger.exception("Begin processing %s", "AWS request" )
		"""
		if extra is None:
			self.logger.exception(msg, *args, extra={}, exc_info=exc_info, **kwargs)

		else:
			self.logger.exception(msg, *args, extra=extra, exc_info=exc_info, **kwargs)

	def critical(self, msg, *args, extra=None, **kwargs):
		"""
		Log 'msg % args' with severity 'CRITICAL'.

		To pass additional context, use keyword argument extra with
		a json value, e.g.

		logger.critical("Begin processing %s", "AWS request" )
		"""
		if extra is None:
			self.logger.critical(msg, *args, extra={}, **kwargs)

		else:
			self.logger.critical(msg, *args, extra=extra, **kwargs)


log_client = None


def get_logger():
	global log_client

	"""Call this method just once. To create a new logger."""
	log_client = Logger() if not log_client else log_client

	return log_client
