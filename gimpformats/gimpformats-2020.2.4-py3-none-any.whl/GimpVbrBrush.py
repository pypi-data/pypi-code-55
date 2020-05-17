#!/usr/bin/env python3
"""
Pure python implementation of the gimp vbr brush format
"""

import argparse

class GimpVbrBrush:
	"""
	Pure python implementation of the gimp vbr brush format

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/vbr.txt
	"""

	BRUSH_SHAPES = ["circle", "square", "diamond"]

	def __init__(self, filename=None):
		self.version = 1.0
		self.name = ''
		self.spacing = 0
		self.radius = 50
		self.hardness = 1
		self.aspectRatio = 1
		self.angle = 0
		self.brushShape = None # one of the strings in self.BRUSH_SHAPES
		self.spikes = None
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
			f = open(filename, 'r')
		data = f.read()
		f.close()
		self.decode_(data)

	@property
	def image(self):
		"""
		this parametric brush converted to a useable PIL image
		"""
		raise NotImplementedError() # TODO:

	def decode_(self, data):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		"""
		data = [s.strip() for s in data.split('\n')]
		if data[0] != "GIMP-VBR":
			raise Exception('File format error.  Magic value mismatch.')
		self.version = float(data[1])
		if self.version == 1.0:
			self.name = data[2] # max len 255 bytes
			self.spacing = float(data[3])
			self.radius = float(data[4])
			self.hardness = float(data[5])
			self.aspectRatio = float(data[6])
			self.angle = float(data[7])
		elif self.version == 1.5:
			self.name = data[2] # max len 255 bytes
			self.brushShape = data[3] # one of the strings in self.BRUSH_SHAPES
			self.spacing = float(data[4])
			self.radius = float(data[5])
			self.spikes = float(data[6])
			self.hardness = float(data[7])
			self.aspectRatio = float(data[8])
			self.angle = float(data[9])
		else:
			raise Exception('Unknown version ' + str(self.version))

	def encode_(self):
		"""
		encode to a raw data stream
		"""
		data = []
		data.append("GIMP-VBR")
		data.append(str(self.version))
		if self.version == 1.0:
			data.append(str(self.name))
			data.append(str(self.spacing))
			data.append(str(self.radius))
			data.append(str(self.hardness))
			data.append(str(self.aspectRatio))
			data.append(str(self.angle))
		elif self.version == 1.5:
			data.append(str(self.name))
			data.append(str(self.brushShape))
			data.append(str(self.spacing))
			data.append(str(self.radius))
			data.append(str(self.spikes))
			data.append(str(self.hardness))
			data.append(str(self.aspectRatio))
			data.append(str(self.angle))
		return ('\n'.join(data) + '\n').encode('utf-8')

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
		if toExtension is not None and toExtension != 'vbr':
			asImage = True
		if asImage:
			self.image.save(toFilename)
		else:
			if not hasattr(toFilename, 'write'):
				f = open(toFilename, 'wb')
			f.write(self.encode_())

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		if self.filename is not None:
			ret.append('Filename: ' + self.filename)
		ret.append('Name: ' + str(self.name))
		ret.append('Version: ' + str(self.version))
		ret.append('Spacing: ' + str(self.spacing))
		ret.append('Radius: ' + str(self.radius))
		ret.append('Hardness: ' + str(self.hardness))
		ret.append('Aspect ratio: ' + str(self.aspectRatio))
		ret.append('Angle: ' + str(self.angle))
		ret.append('Brush Shape: ' + str(self.brushShape))
		ret.append('Spikes: ' + str(self.spikes))
		return '\n'.join(ret)

	def __eq__(self, other):
		"""
		perform a comparison
		"""
		if other.name != self.name:
			return False
		if other.version != self.version:
			return False
		if other.spacing != self.spacing:
			return False
		if other.radius != self.radius:
			return False
		if other.hardness != self.hardness:
			return False
		if other.aspectRatio != self.aspectRatio:
			return False
		if other.angle != self.angle:
			return False
		if other.brushShape != self.brushShape:
			return False
		if other.spikes != self.spikes:
			return False
		return True


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("gimpVbrBrush.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	parser.add_argument("--dump", action="store_true",
	help="dump info about this file")
	args = parser.parse_args()

	gimpVbrBrush = GimpVbrBrush(args.xcfdocument)

	if args.dump:
		print(gimpVbrBrush)
