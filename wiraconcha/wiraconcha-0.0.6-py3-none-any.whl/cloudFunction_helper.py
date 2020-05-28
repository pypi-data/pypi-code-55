import logging
import sys
import os


def setupLogger():
	""" properly sets up the logger depending on if the code is running
		on a cloud function or locally

		Args:
		Returns:
	"""
	function_identity = os.environ.get('FUNCTION_IDENTITY', 'local')
	root = logging.getLogger()
	root.setLevel(logging.INFO)
	root.info("function_identity: {}".format(function_identity))
	if function_identity == 'local':

		logging.StreamHandler(sys.stdout)


if __name__ == '__main__':
	setupLogger()
