import botocore.exceptions
import sys
"""Error handler class"""

class ServerError(Exception):
	"""Base Class for all other application exceptions"""

class AWSPermissionError(ServerError):
	"""Raised when AWS throws Permission error"""

class AWSRequestError(ServerError):
    """Raised when any of the AWS Request fails"""

def classify_error(logger, err, msg, extra=None):
	"""Classify the error to Permission or Request Processing Error"""

	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename

	if isinstance(err, botocore.exceptions.ClientError):

		message = 'Exception ( {}:{}, "{}" ): {}'.format(filename, lineno, msg, exc_obj)

		if err.response['Error']['Code'] == 'AuthFailure':
			logger.exception(f'AWS Authentication failed. Please configure credentials using "awsaudit --configure".', extra=extra)
			exit()
		elif err.response['Error']['Code'] == 'LimitExceededException':
			logger.exception(f'API call limit exceeded. Please try again some time.', extra=extra)
		elif err.response['Error']['Code'] == 'AccessDenied' or \
				err.response['Error']['Code'] == 'AccessDeniedException' or \
				err.response['Error']['Code'] == 'UnauthorizedOperation' or \
				err.response['Error']['Code'] == 'Client.UnauthorizedOperation':
			logger.exception(f'Insufficient permissions. Please verify the credentials and the permission associated with the user.', extra=extra)
			logger.info(message, extra=extra)			
			return AWSPermissionError(message)

		else:
			logger.exception(message, extra=extra)
			return AWSRequestError(message)
	else:
		message = 'Exception ( {}:{} ): {}'.format(filename, lineno, exc_obj)
		logger.exception(message, extra=extra)
		return ServerError(message)
