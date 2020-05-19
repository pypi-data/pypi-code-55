from enum import Enum

class Name(Enum):
	MYSQL = 1
	SQLITE = 2

class Status(Enum):
	CONNECTED = 1 #the message is being sent
	DISCONECTED = 2 #the message was dropped by the server
	DELAYED = 3 #the message has gone on for a suspiciously long time
	DROPPED = 4 #the connection was dropped by the program

class Message(Enum):
	UNSECURE = 1 #No encryption, no SQL injection check
	ENCRYPTED = 2 #encrypted, No SQL injection check
	SECURE = 3 # not encrypted, SQL injection check
	VERY_SECURE = 4 #encrypted, SQL injection check