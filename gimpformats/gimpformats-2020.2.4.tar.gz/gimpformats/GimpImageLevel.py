#!/usr/bin/env python3
"""
Gets packed pixels from a gimp image

This represents a single level in an imageHierarchy
"""
import math
import zlib
import PIL.Image
from .GimpIOBase import IO, GimpIOBase


class GimpImageLevel(GimpIOBase):
	"""
	Gets packed pixels from a gimp image

	This represents a single level in an imageHierarchy
	"""
	def __init__(self, parent):
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self._tiles = None # tile PIL images
		self._image = None

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index)
		#print 'Decoding image level at',io.index
		self.width = io.u32
		self.height = io.u32
		if self.width != self.parent.width or self.height != self.parent.height:
			currentSize = '(' + str(self.width) + ',' + str(self.height) + ')'
			expectedSize = '(' + str(self.parent.width) + ',' + str(self.parent.height) + ')'
			msg = ' Usually this implies file corruption.'
			raise Exception('Image data size mismatch. ' + currentSize + '!=' + expectedSize + msg)
		self._tiles = []
		self._image = None
		for y in range(0, self.height, 64):
			for x in range(0, self.width, 64):
				ptr = self._pointerDecode_(io)
				size = (min(self.width - x, 64), min(self.height - y, 64))
				totalBytes = size[0] * size[1] * self.bpp
				if self.doc.compression == 0: # none
					data = io.data[ptr:ptr + totalBytes]
				elif self.doc.compression == 1: # RLE
					data = self._decodeRLE(io.data, size[0] * size[1], self.bpp, ptr)
				elif self.doc.compression == 2: # zip
					data = zlib.decompress(io.data[ptr:ptr + totalBytes +
					24]) # guess how many bytes are needed
				else:
					raise Exception('ERR: unsupported compression mode ' +
					str(self.doc.compression))
				subImage = PIL.Image.frombytes(self.mode, size, bytes(data), decoder_name='raw')
				self._tiles.append(subImage)
		_ = self._pointerDecode_(io) # list ends with nul character
		return io.index

	def encode_(self):
		"""
		encode this object to a byte buffer
		"""
		dataIO = IO()
		io = IO()
		io.u32 = self.width
		io.u32 = self.height
		dataIndex = io.index + self._POINTER_SIZE_ * (len(self.tiles) + 1)
		for tile in self.tiles:
			io.addBytes(self._pointerEncode_(dataIndex + dataIO.index))
			data = tile.tobytes()
			if self.doc.compression == 0: # none
				pass
			elif self.doc.compression == 1: # RLE
				data = self._encodeRLE(data, self.bpp)
				#raise Exception('RLE Compression is a work in progress!')
			elif self.doc.compression == 2: # zip
				data = zlib.compress(data)
			else:
				raise Exception('ERR: unsupported compression mode ' + str(self.doc.compression))
			dataIO.addBytes(data)
		io.addBytes(self._pointerEncode_(0))
		io.addBytes(dataIO.data)
		return io.data


	def _decodeRLE(self, data, pixels, bpp, index=0):
		"""
		decode RLE encoded image data
		"""
		ret = [[] for chan in range(bpp)]
		for chan in range(bpp):
			n = 0
			while n < pixels:
				opcode = data[index]
				index += 1
				if 0 <= opcode <= 126: # a short run of identical bytes
					val = data[index]
					index += 1
					for _ in range(opcode + 1):
						ret[chan].append(val)
						n += 1
				elif opcode == 127: # A long run of identical bytes
					m = data[index]
					index += 1
					b = data[index]
					index += 1
					val = data[index]
					index += 1
					amt = m * 256 + b
					for _ in range(amt):
						ret[chan].append(val)
						n += 1
				elif opcode == 128: # A long run of different bytes
					m = data[index]
					index += 1
					b = data[index]
					index += 1
					amt = m * 256 + b
					for _ in range(amt):
						val = data[index]
						index += 1
						ret[chan].append(val)
						n += 1
				elif 129 <= opcode <= 255: # a short run of different bytes
					amt = 256 - opcode
					for _ in range(amt):
						val = data[index]
						index += 1
						ret[chan].append(val)
						n += 1
				else:
					print('Unreachable branch', opcode)
					raise Exception()
		# flatten/weave the individual channels into one strream
		flat = bytearray()
		for i in range(pixels):
			for chan in range(bpp):
				flat.append(ret[chan][i])
		return flat

	def _encodeRLE(self, data, bpp):
		"""
		encode image to RLE image data
		"""
		def countSame(data, startIdx):
			"""
			count how many times bytes are identical
			"""
			idx = startIdx
			l = len(data)
			if idx >= l:
				return 0
			c = data[idx]
			idx = startIdx + 1
			while idx < l and data[idx] == c:
				idx += 1
			return idx - startIdx


		def countDifferent(data, startIdx):
			"""
			count how many times bytes are different
			"""
			idx = startIdx
			l = len(data)
			if idx >= l:
				return 1
			c = data[idx]
			idx = startIdx + 1
			while idx < (l - 1) and data[idx] != c:
				idx += 1
				c = data[idx]
			return idx - startIdx


		def rleEncodeChan(data):
			"""
			rle encode a single channel of data
			"""
			ret = []
			idx = 0
			while idx < len(data):
				nRepeats = countSame(data, 0)
				if nRepeats == 1: # different bytes
					nDifferences = countDifferent(data, 1)
					if nDifferences <= 127: # short run of different bytes
						ret.append(129 + nRepeats - 1)
						ret.append(data[idx])
						idx += nDifferences
					else: # long run of different bytes
						ret.append(128)
						ret.append(math.floor(nDifferences / 256.0))
						ret.append(nDifferences % 256)
						ret.append(data[idx])
						idx += nDifferences
				elif nRepeats <= 127: # short run of same bytes
					ret.append(nRepeats - 1)
					ret.append(data[idx])
					idx += nRepeats
				else: # long run of same bytes
					ret.append(127)
					ret.append(math.floor(nRepeats / 256.0))
					ret.append(nRepeats % 256)
					ret.append(data[idx])
					idx += nRepeats
			return ret

		# if there is only one channel, encode and return it directly
		if bpp == 1:
			return rleEncodeChan(data)
		# split into channels
		dataByChannel = []
		for chan in range(bpp):
			chanData = []
			for index in range(chan, bpp, len(data)):
				chanData.append(data[index])
			dataByChannel.append(chanData)
		# encode each channel
		for index in range(len(dataByChannel)): # iterate through 2d array
			dataByChannel[index] = rleEncodeChan(dataByChannel[index])
		# join and return
		return "".join("".join(str(x)) for x in dataByChannel)

	@property
	def bpp(self):
		""" get bpp """
		return self.parent.bpp

	@property
	def mode(self):
		""" get mode """
		MODES = [None, 'L', 'LA', 'RGB', 'RGBA']
		return MODES[self.bpp]

	@property
	def tiles(self):
		""" get tiles """
		if self._tiles is not None:
			return self._tiles
		if self.image is not None:
			return self._imgToTiles(self.image)
		return None

	def _imgToTiles(self, image):
		"""
		break an image into a series of tiles, each<=64x64
		"""
		ret = []
		for y in range(0, self.height, 64):
			for x in range(0, self.width, 64):
				bounds = (x, y, min(self.width - x, 64), min(self.height - y, 64))
				ret.append(image.crop(bounds))
		return ret

	@property
	def image(self):
		"""
		get a final, compiled image
		"""
		if self._image is None:
			self._image = PIL.Image.new(self.mode, (self.width, self.height), color=None)
			tileNum = 0
			for y in range(0, self.height, 64):
				for x in range(0, self.width, 64):
					subImage = self._tiles[tileNum]
					tileNum += 1
					self._image.paste(subImage, (x, y))
			#self._tiles = None
		return self._image

	@image.setter
	def image(self, image):
		self._image = image
		self._tiles = None
		self.width = image.width
		self.height = image.height
		self.tiles = None

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		return indent + (('\n' + indent).join(ret))
