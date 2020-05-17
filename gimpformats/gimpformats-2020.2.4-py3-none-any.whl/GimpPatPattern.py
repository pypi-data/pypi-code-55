#!/usr/bin/env python3
"""
Pure python implementation of a gimp pattern file
"""
import argparse
import PIL.Image
from binaryiotools import IO


class GimpPatPattern:
	"""
	Pure python implementation of a gimp pattern file

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/pat.txt
	"""

	COLOR_MODES = [None, 'L', 'LA', 'RGB', 'RGBA']

	def __init__(self, filename=None):
		self.filename = None
		self.version = 1
		self.width = 0
		self.height = 0
		self.bpp = 4
		self.mode = self.COLOR_MODES[self.bpp]
		self.name = ''
		self._rawImage = None
		self._image = None
		if filename is not None:
			self.load(filename)

	def load(self, filename):
		"""
		load a gimp file

		:param filename: can be a file name or a file-like object
		"""
		if hasattr(filename, 'read'):
			self.filename = filename.name
			f = filename
		else:
			self.filename = filename
			f = open(filename, 'rb')
		data = f.read()
		f.close()
		self.decode_(data)

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index)
		headerSize = io.u32
		self.version = io.u32
		self.width = io.u32
		self.height = io.u32
		self.bpp = io.u32
		self.mode = self.COLOR_MODES[self.bpp]
		magic = io.getBytes(4)
		if magic.decode('ascii') != 'GPAT':
			raise Exception('File format error.  Magic value mismatch.')
		nameLen = headerSize - io.index
		self.name = io.getBytes(nameLen).decode('UTF-8')
		self._rawImage = io.getBytes(self.width * self.height * self.bpp)
		self._image = None

	def encode_(self):
		"""
		encode to a byte buffer
		"""
		io = IO()
		io.u32 = 24 + len(self.name)
		io.u32 = self.version
		io.u32 = self.width
		io.u32 = self.height
		io.u32 = len(self.image.mode)
		io.addBytes('GPAT')
		io.addBytes(self.name.encode('utf-8'))
		if self._rawImage is None:
			rawImage = self.image.tobytes(encoder_name='raw')
		else:
			rawImage = self._rawImage
		io.addBytes(rawImage)
		return io.data

	@property
	def size(self):
		"""
		the size of the pattern
		"""
		return (self.width, self.height)

	@property
	def image(self):
		"""
		get a final, compiled image
		"""
		if self._image is None:
			if self._rawImage is None:
				return None
			self._image = PIL.Image.frombytes(self.mode,
			self.size,
			self._rawImage,
			decoder_name='raw')
		return self._image

	@image.setter
	def image(self, image):
		self._image = image
		self._rawImage = None

	def save(self, toFilename=None, toExtension=None):
		"""
		save this gimp image to a file
		"""
		asImage = False
		if toExtension is None:
			if toFilename is not None:
				toExtension = toFilename.rsplit('.', 1)
				if len(toExtension) > 1:
					toExtension = toExtension[-1]
				else:
					toExtension = None
		if toExtension is not None and toExtension != 'pat':
			asImage = True
		if asImage:
			self.image.save(toFilename)
		else:
			if not hasattr(toFilename, 'write'):
				f = open(toFilename, 'wb')
			f.write(self.encode_())
			f.close()

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		if self.filename is not None:
			ret.append('Filename: ' + self.filename)
		ret.append('Name: ' + str(self.name))
		ret.append('Version: ' + str(self.version))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append('BPP: ' + str(self.bpp))
		ret.append('Mode: ' + str(self.mode))
		return '\n'.join(ret)


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("GimpPatPattern.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	group.add_argument("--show", action="store_true",
	help="show the image")
	group.add_argument("--save", action="store",
	help="save out the image")
	args = parser.parse_args()

	gimpPatPattern = GimpPatPattern(args.xcfdocument)

	if args.dump:
		print(gimpPatPattern)
	if args.show:
		gimpPatPattern.image.show()
	if args.save:
		gimpPatPattern.image.save(args.save)
