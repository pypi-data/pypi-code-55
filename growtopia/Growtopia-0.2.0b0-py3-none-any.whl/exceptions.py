class Error(Exception):
    """This is only a sample or base exception, ignore this"""

class InvalidGrowtopiaPath(Error):
	"""If the Growtopia Path is invalid or its a file, then raise this"""
class WrongCredential(Error):
	"""If the credential is wrong, raise this"""
class InvalidGrowtopiaVersion(Error):
	"""Raised when user put letter 'V' or anything else instead of
	floating numbers
	"""
class InvalidIntValue(Error):
	"""Raise this when user input something invalid that expected
	to be int
	"""
class InvalidFloatValue(Error):
	"""Raise this when user input something invalid that expected
	to be float
	"""
class InvalidPacketType(Error):
	"""Raise this when there is no packet type available in the list
	"""
class OutOfRange(Error):
	"""This is raised when you've reached the most craziest crazy
	level in the universe (There is no unlimited range here! NEVER)
	"""
class NetworkError(Error):
	"""This is raised when your internet connection goes slow
	and disappear when your connection is 1TB/s+
	"""
class ENetError(Error):
	"""This error raised when something happens to the ENet setup
	"""
class EventNotExist(Error):
	"""Raised when selected event did not exist in the list. To check
	the existing events, do print(Growtopia.Player.Events)
	"""