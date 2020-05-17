#!/usr/bin/env python3
"""
Gimp Image Pipe Format

The gih format is use to store a series of brushes, and some extra info
for how to use them.
"""
import argparse
from binaryiotools import IO
from .GimpGbrBrush import GimpGbrBrush


class GimpGihBrushSet:
	"""
	Gimp Image Pipe Format

	The gih format is use to store a series of brushes, and some extra info
	for how to use them.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/gih.txt
	"""
	def __init__(self, filename=None):
		self.filename = None
		self.name = ''
		self.params = {}
		self.brushes = []
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
		self.name = io.textLine
		secondLine = io.textLine.split(' ')
		self.params = {}
		numBrushes = int(secondLine[0])
		# everything that's left is a gimp-image-pipe-parameters parasite
		for i in range(1, len(secondLine)):
			param = secondLine[i].split(':', 1)
			self.params[param[0].strip()] = param[1].strip()
		self.brushes = []
		for _ in range(numBrushes):
			b = GimpGbrBrush()
			io.index = b.decode_(
			io.data,
			io.index) # TODO: broken.  For some reson there is extra data between brushes!
			self.brushes.append(b)
		return io.index

	def encode_(self):
		"""
		encode this object to a byte array
		"""
		io = IO()
		io.textLine = self.name
		# add the second line of data
		secondLine = [str(len(self.brushes))]
		for key in self.params:
			secondLine.append(key + ':' + str(self.params[key]))
		io.textLine = ' '.join(secondLine)
		# add the brushes
		for brush in self.brushes:
			io.addBytes(brush.encode_())
		return io.data

	def save(self, toFilename=None):
		"""
		save this gimp image to a file
		"""
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
		for k, v in list(self.params.items()):
			ret.append(k + ': ' + str(v))
		for i in range(len(self.brushes)):
			ret.append('Brush ' + str(i))
			ret.append(self.brushes[i].__repr__(indent + '\t'))
		return ('\n' + indent).join(ret)


if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("GimpGihBrushSet.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	group.add_argument("--show", action="store",
	help="show the brush image (n or * for all layers)")
	group.add_argument("--save", action="store",
	help="save out the brush set (n,out-file.png)")
	args = parser.parse_args()

	gimpGihBrushSet = GimpGihBrushSet(args.xcfdocument)

	if args.dump:
		print(gimpGihBrushSet)
	if args.show:
		if args.show == '*':
			for iterationM in range(len(gimpGihBrushSet.brushes)):
				gimpGihBrushSet.brushes[iterationM].image.show()
		else:
			gimpGihBrushSet.brushes[int(args.show)].image.show()
	if args.save:
		indexM, filenameM = args.save.split(',', 1)
		if filenameM.find('*') < 0:
			filenameM = '*.'.join(filenameM.split('.', 1))
		if indexM == '*':
			for iterationM in range(len(gimpGihBrushSet.brushes)):
				fn2 = filenameM.replace('*', str(iterationM))
				gimpGihBrushSet.brushes[iterationM].image.save(fn2)
		else:
			fn2 = filenameM.replace('*', iterationM)
			gimpGihBrushSet.brushes[int(indexM)].image.save(fn2)
