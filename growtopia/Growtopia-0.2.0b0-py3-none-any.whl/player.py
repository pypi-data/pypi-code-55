from pyautogui import *
from functools import update_wrapper

def setupmethod(f):
	"""Wraps a method so that it performs a check in debug mode if the
	first request was already handled.
	"""

	def wrapper_func(self, *args, **kwargs):
		#if self.debug and self._got_first_request:
			#raise AssertionError(
				#"A setup function was called after the "
				#"first request was handled.  This usually indicates a bug "
				#"in the application where a module was not imported "
				#"and decorators or other functionality was called too late.\n"
				#"To fix this make sure to import all your view modules, "
				#"database models and everything related at a central place "
				#"before the application starts serving requests."
			#)
		return f(self, *args, **kwargs)

	return update_wrapper(wrapper_func, f)

class Player:
	def __init__(self, username, password, headless=False):
		# Position
		self.X = 0.00
		self.Y = 0.00
			
		# Status and Profile
		self.level = 0
		self.world = ""
		self.username = ""
		self.guildName = ""
		self.expression = ""
		self.trading = False
		self.hasGuild = False
		self.isMod = False
			
		# Network
		self.peer = Peer()
		self.mac = ""
		self.token = ""
		self.rtid = ""
		self.slowNet = False
		self.netId = 0
		self.ping = 0 # in microsecond
	
	def __repr__(self):
		return f'<Player {self.username}>'
	
	def login():
		"""
		Feeling comfortable enough? Logon to the Growtopia world now!
		This method is designed NOT TO pass the captcha and NOT TO pass AAP
		
		What is AAP?
		Its just a simple Account Advanced Protection, it doesn't protects you at all.
		
		How do i pass the AAP then?
		.login() then go to your email and confirm to bypass AAP, run the .login() command again.
		
		How to pass the captcha?
		Lol.
		"""
		pass # TODO
	
	def chat():
		"""
		This method need a contributor.
		[CREDITS: YOUR_GROW_ID]
		Contribute now!
		"""
		pass # TODO
	
	def command():
		"""
		This method need a contributor.
		[CREDITS: YOUR_GROW_ID]
		Contribute now!
		"""
		pass # TODO
	
	def respawn():
		"""
		Respawn your Growtopian, lol. (Maybe you stuck at platform trap?)
		"""
	
	def punch(x, y):
		"""
		Punch at the absolute X and Y axis
		
		[x] [2] [3] [4] [5] -> X axis
		[4] [~] [~] [~] [~]
		[3] [~] >_< [~] [~]
		[2] [~] [~] [~] [~]
		[1] [~] [~] [~] [~]
		 ^ Y axis
		
		Will raise, OutOfRange exception if you're "crazy" like me.
		"""
	
	def on(self,eventName):
		"""A decorator that makes your function executed whenever the
		given eventName triggered.
		
		obj eventName	: An object that you should get one from Growtopia.Player.Events
		
		example code:
		
		>>> myPlayer = Growtopia.Player(username, password)
		>>> @myPlayer.on(Growtopia.Player.Events.punch)
		... def onPunch():
		... 	print("The player punching!")
		>>> myPlayer.punch(4,3)
		The player punching!
		"""
		
		def decorator(function):
			raise EventNotExist("The selected event did not exist. (Try \"Growtopia.Player.Events.all()\" to list the available events)")
			self.__p.__evtL(eventName, function)
			return function
		return decorator
	
	#def help():
	#	pass
	
	# This class listen to requested events
	class __p:
		"""Private class to listen events
		"""
		def __init__(self):
			self.parent = super()
			self.events = super().Events
		
		@setupmethod
		def __evtL(self, evnt, f):
			#self = self
			try:
				self.__levtlist.append({event: evnt, function: f})
			except NameError:
				self.__levtlist = list()
				self.__levtlist.append({event: evnt, function: f})
	
	class Events:
		"""A collection of events that can only be useful for Growtopia.Player.on decorator
		"""
		def __init__(self):
			# Classes
			self.parent = super()
		
			# Player State
			self.move = "move"
			self.jump = "jump"
			self.place = "place"
			self.punch = "punch"
			self.plant = "plant"
			self.enterDoor = "enterDoor"
			self.punched = "punched"
			self.drop = "drop"
			self.receiveItem = "receiveItem"
			self.receiveGem = "receiveGem"
			
			# Requests
			self.tradeRequest = "tradeRequest"
			self.friendRequest = "friendRequest"
			self.accessRequest = "accessRequest"
			self.guildRequest = "guildRequest"
			self.apperenticeRequest = "apperenticeRequest"
			
			# Chats
			self.chat = "chat"
			self.broadcast = "broadcast"
			self.superBroadcast = "superBroadcast"
			self.superDuperBroadcast = "superDuperBroadcast"
			self.receiveBroadcast = "receiveBroadcast"
			self.receiveSuperBroadcast = "receiveSuperBroadcast"
			self.receiveSuperDuperBroadcast = "receiveSuperDuperBroadcast"
			
		
		def all(self):
			return self.__dict__
		
		def trigger(self, evnt, silent=True):
			"""Manually trigger event instantly. This is used for the main event trigger
			method
			"""
			self.__temp = False
			if evnt in self.all():
				f = self.parent.__p.__dict__
				for key in self.parent.__p.__dict__:
					if key == evnt:
						f[key]() # Execute the function
						self.__temp == True
			
			if self.__temp is not True:
				raise EventNotExist("The triggered event doesn't exist")
			
			del self.__temp