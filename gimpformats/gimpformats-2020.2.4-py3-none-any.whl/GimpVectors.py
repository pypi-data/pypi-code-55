#!/usr/bin/env python3
"""
Stuff related to vectors/paths within a gimp document
"""
#from .GimpIOBase import GimpIOBase
from binaryiotools import IO
from .GimpParasites import GimpParasite

class GimpVector:
	"""
	A gimp brush stroke vector
	"""
	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.name = ''
		self.uniqueId = 0
		self.visible = True
		self.linked = False
		self.parasites = []
		self.strokes = []

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index, boolSize=32)
		self.name = io.sz754
		self.uniqueId = io.u32
		self.visible = io.bool
		self.linked = io.bool
		numParasites = io.u32
		numStrokes = io.u32
		for _ in range(numParasites):
			p = GimpParasite()
			io.index = p.decode_(io.data, io.index)
			self.parasites.append(p)
		for _ in range(numStrokes):
			gs = GimpStroke(self)
			io.index = gs.decode_(io.data, io.index)
			self.strokes.append(p)
		return io.index

	def encode_(self):
		"""
		encode to binary data
		"""
		io = IO(boolSize=32)
		io.sz754 = self.name
		io.u32 = self.uniqueId
		io.bool = self.visible
		io.bool = self.linked
		io.u32 = len(self.parasites)
		io.u32 = len(self.strokes)
		for p in self.parasites:
			io.addBytes(p.encode_())
		for gs in self.strokes:
			io.addBytes(gs.encode_())
		return io.data

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Name: ' + str(self.name))
		ret.append('Unique ID (tattoo): ' + str(self.uniqueId))
		ret.append('Visible: ' + str(self.visible))
		ret.append('Linked: ' + str(self.linked))
		if self.parasites:
			ret.append('Parasites: ')
			for item in self.parasites:
				ret.append(item.__repr__(indent + '\t'))
		if self.strokes:
			ret.append('Strokes: ')
			for item in self.strokes:
				ret.append(item.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))


class GimpStroke:
	"""
	A single stroke within a vector
	"""

	STROKE_TYPES = ['None', 'Bezier']

	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.strokeType = 1 # one of self.STROKE_TYPES
		self.closedShape = True
		self.points = []

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index, boolSize=32)
		self.strokeType = io.u32
		self.closedShape = io.bool
		numFloatsPerPoint = io.u32
		numPoints = io.u32
		for _ in range(numPoints):
			gp = GimpPoint(self)
			io.index = gp.decode_(io.data, io.index, numFloatsPerPoint)
			self.points.append(gp)
		return io.index

	def encode_(self):
		"""
		encode to binary data
		"""
		io = IO(boolSize=32)
		io.u32 = self.strokeType
		io.bool = self.closedShape
		#io.u32 = numFloatsPerPoint
		#io.u32 = numPoints
		for gp in self.points:
			io.addBytes(gp.encode_())
		return io.data

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Stroke Type: ' + self.STROKE_TYPES[self.strokeType])
		ret.append('Closed: ' + str(self.closedShape))
		ret.append('Points: ')
		for point in self.points:
			ret.append(point.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))


class GimpPoint:
	"""
	A single point within a stroke
	"""

	POINT_TYPES = ['Anchor', 'Bezier control point']

	def __init__(self, parent):
		#GimpIOBase.__init__(self, parent)
		self.x = 0
		self.y = 0
		self.pressure = 1.0
		self.xTilt = 0.5
		self.yTilt = 0.5
		self.wheel = 0.5
		self.pointType = 0

	def decode_(self, data, index=0, numFloatsPerPoint=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		:param numFloatsPerPoint: required so we know
			how many different brush dynamic measurements are
			inside each point
		"""
		io = IO(data, index, boolSize=32)
		self.pressure = 1.0
		self.xTilt = 0.5
		self.yTilt = 0.5
		self.wheel = 0.5
		self.pointType = io.u32
		if numFloatsPerPoint < 1:
			numFloatsPerPoint = (len(io.data) - io.index) / 4
		self.x = io.float
		self.y = io.float
		if numFloatsPerPoint > 2:
			self.pressure = io.float
			if numFloatsPerPoint > 3:
				self.xTilt = io.float
				if numFloatsPerPoint > 4:
					self.yTilt = io.float
					if numFloatsPerPoint > 5:
						self.wheel = io.float
		return io.index

	def encode_(self):
		"""
		encode to binary data
		"""
		io = IO(boolSize=32)
		io.u32 = self.pointType
		io.float = self.x
		io.float = self.y
		if self.pressure is not None:
			io.float = self.pressure
			if self.xTilt is not None:
				io.float = self.xTilt
				if self.yTilt is not None:
					io.float = self.yTilt
					if self.wheel is not None:
						io.float = self.wheel
		return io.data

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Location: (' + str(self.x) + ',' + str(self.y) + ')')
		ret.append('Pressure: ' + str(self.pressure))
		ret.append('Location: (' + str(self.xTilt) + ',' + str(self.yTilt) + ')')
		ret.append('Wheel: ' + str(self.wheel))
		return indent + (('\n' + indent).join(ret))
