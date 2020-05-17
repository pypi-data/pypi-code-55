#!/usr/bin/env python3
"""
Pure python implementation of the gimp xcf file format

Currently supports:
	Loading xcf files
	Getting image hierarchy and info
	Getting image for each layer (PIL image)
Currently not supporting:
	Saving
	Programatically alter documents (add layer, etc)
	Rendering a final, compositied image
"""
import argparse
import copy

import PIL.ImageGrab
from PIL import Image
from blendmodes.blend import blendLayers, BlendType
from binaryiotools import IO
from .GimpIOBase import GimpIOBase
from .GimpImageHierarchy import GimpImageHierarchy
from .GimpPrecision import Precision
from .GimpLayer import GimpLayer
from .GimpChannel import GimpChannel

class GimpDocument(GimpIOBase):
	"""
	Pure python implementation of the gimp file format

	Has a series of attributes including the following:
	self._layers = None
	self._layerPtr = []
	self._channels = []
	self._channelPtr = []
	self.version = None
	self.width = 0
	self.height = 0
	self.baseColorMode = 0
	self.precision = None # Precision object
	self._data = None

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/xcf.txt
	"""
	def __init__(self, fileName=None):
		GimpIOBase.__init__(self, self)
		self._layers = []
		self._layerPtr = []
		self._channels = []
		self._channelPtr = []
		self.version = 11 # This is the most recent version
		self.width = 0
		self.height = 0
		self.baseColorMode = 0
		self.precision = None # Precision object
		self._data = None
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName):
		"""
		Load a gimp xcf and decode the file. See decode for more on this
		process

		:param filename: can be a file name or a file-like object
		"""
		if hasattr(fileName, 'read'):
			self.filename = fileName.name
			f = fileName
		else:
			self.filename = fileName
			f = open(fileName, 'rb')
		data = f.read()
		f.close()
		self.decode_(data)

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		Steps:
		Create a new IO buffer (array of binary values)
		Check that the file is a valid gimp xcf
		Grab the file version
		Grab other attributes as outlined in the spec
		Get precision data using the class and io buffer
		List of properties
		Get the layers and add the pointers to them
		Get the channels and add the pointers to them
		Return the offset

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		# Create a new IO buffer (array of binary values)
		io = IO(data, index)
		# Check that the file is a valid gimp xcf
		if io.getBytes(9) != "gimp xcf ".encode('ascii'):
			raise Exception('Not a valid GIMP file')
		# Grab the file version
		version = io.cString
		if version == 'file':
			self.version = 0
		else:
			self.version = int(version[1:])
		# Grab other attributes as outlined in the spec
		self.width = io.u32
		self.height = io.u32
		self.baseColorMode = io.u32
		# Get precision data using the class and io buffer
		self.precision = Precision()
		self.precision.decode_(self.version, io)
		# List of properties
		self._propertiesDecode_(io)
		self._layerPtr = []
		self._layers = []
		# Get the layers and add the pointers to them
		while True:
			ptr = self._pointerDecode_(io)
			if ptr == 0:
				break
			self._layerPtr.append(ptr)
			l = GimpLayer(self)
			l.decode_(io.data, ptr)
			self._layers.append(l)
		# Get the channels and add the pointers to them
		self._channelPtr = []
		self._channels = []
		while True:
			ptr = self._pointerDecode_(io)
			if ptr == 0:
				break
			self._channelPtr.append(ptr)
			c = GimpChannel(self)
			c.decode_(io.data, ptr)
			self._channels.append(c)
		# Return the offset
		return io.index

	def encode_(self):
		"""
		encode to a byte array

		Steps:
		Create a new IO buffer (array of binary values)
		The file is a valid gimp xcf
		Set the file version
		Set other attributes as outlined in the spec
		Set precision data using the class and io buffer
		List of properties
		Set the layers and add the pointers to them
		Set the channels and add the pointers to them
		Return the data

		"""
		# Create a new IO buffer (array of binary values)
		io = IO()
		# The file is a valid gimp xcf
		io.addBytes("gimp xcf ")
		# Set the file version
		io.addBytes("v{0:03d}".format(self.version) + '\0')
		# Set other attributes as outlined in the spec
		io.u32 = self.width
		io.u32 = self.height
		io.u32 = self.baseColorMode
		# Set precision data using the class and io buffer
		if self.precision is None:
			self.precision = Precision()
		self.precision.encode_(self.version, io)
		# List of properties
		io.addBytes(self._propertiesEncode_())
		dataAreaIdx = io.index + self._POINTER_SIZE_ * (len(self.layers) + len(self._channels))
		dataAreaIo = IO()
		# Set the layers and add the pointers to them
		for l in self.layers:
			io.pointer = dataAreaIdx + dataAreaIo.index
			dataAreaIo.addBytes(l.encode_())
		# Set the channels and add the pointers to them
		for channel in self._channels:
			io.pointer = dataAreaIdx + dataAreaIo.index
			dataAreaIo.addBytes(channel.encode_())
		io.addBytes(dataAreaIo)
		# Return the data
		return io.data

	def _forceFullyLoaded(self):
		"""
		make sure everything is fully loaded from the file
		"""
		for l in self.layers:
			l._forceFullyLoaded()
		for chan in self._channels:
			chan._forceFullyLoaded()
		# no longer try to get the data from file
		self._layerPtr = None
		self._channelPtr = None
		self._data = None

	@property
	def layers(self):
		"""
		Decode the image's layers if necessary

		TODO: need to do the same thing with self.Channels
		"""
		if len(self._layers) == 0:
			self._layers = []
			for ptr in self._layerPtr:
				l = GimpLayer(self)
				l.decode_(self._data, ptr)
				self._layers.append(l)
			# add a reference back to this object so it doesn't go away while array is in use
			self._layers.parent = self
			# override some internal methods so we can do more with them
			self._layers._actualDelitem_ = self._layers.__delitem__
			self._layers.__delitem__ = self.deleteLayer
			self._layers._actualSetitem_ = self._layers.__delitem__
			self._layers.__setitem__ = self.setLayer
		return self._layers

	def getLayer(self, index):
		"""
		return a given layer
		"""
		return self.layers[index]

	def setLayer(self, _index, _l):
		"""
		assign to a given layer
		"""
		self._forceFullyLoaded()
		self._layerPtr = None # no longer try to use the pointers to get data
		#self.layers._actualSetitem(index, l)

	def newLayer(self, name, image, index=-1):
		"""
		create a new layer based on a PIL image

		:param name: a name for the new layer
		:param index: where to insert the new layer (default=top)
		:return: newly created GimpLayer object
		"""
		l = GimpLayer(self, name, image)
		l.imageHierarchy = GimpImageHierarchy(self, image=image)
		self.insertLayer(l, index)
		return l

	def newLayerFromClipboard(self, name='pasted', index=-1):
		"""
		Create a new image from the system clipboard.

		:param name: a name for the new layer (default="pasted")
		:param index: where to insert the new layer (default=top)
		:return: newly created GimpLayer object

		NOTE: requires pillow PIL implementation
		NOTE: only works on OSX and Windows
		"""
		image = PIL.ImageGrab.grabclipboard()
		return self.newLayer(name, image, index)

	def addLayer(self, l):
		"""
		append a layer object to the document

		:param layer: the new layer to append
		"""
		self.insertLayer(l, -1)

	def appendLayer(self, l):
		"""
		append a layer object to the document

		:param layer: the new layer to append
		"""
		self.insertLayer(l, -1)

	def insertLayer(self, l, index=-1):
		"""
		insert a layer object at a specific position

		:param layer: the new layer to insert
		:param index: where to insert the new layer (default=top)
		"""
		self._layers.insert(index, l)

	def deleteLayer(self, index):
		"""
		delete a layer
		"""
		self.__delitem__(index)

	# make this class act like this class is an array of layers
	def __len__(self):
		return len(self.layers)

	def __getitem__(self, index):
		return self.layers[index]

	def __setitem__(self, index, l):
		self.setLayer(index, l)

	def __delitem__(self, index):
		self.deleteLayer(index)

	def __inc__(self, amt):
		self.appendLayer(amt)
		return self

	@property
	def image(self):
		"""
		get a final, compiled image
		"""
		# We need to preprocess the layers to sort them into a list of layers
		# and groups. Where a group is a list of layers

		# Example Layers [layer, layer, group, layer]
		# Example Group [Layer(Group), [layer, layer, ...]]
		layers = self.layers[:] # Copy the attribute rather than write to it
		layersOut = []
		index = 0
		while index < len(layers):
			layerOrGroup = layers[index]
			if layerOrGroup.isGroup:
				elem = [layerOrGroup, []]
				index += 1
				while layers[index].itemPath is not None:
					layerCopy = copy.deepcopy(layers[index])
					layerCopy.xOffset -= layerOrGroup.xOffset
					layerCopy.yOffset -= layerOrGroup.yOffset
					elem[1].append(layerCopy)
					layers.pop(index)
				layersOut.append(elem)
			else:
				layersOut.append(layerOrGroup)
				index += 1
		return flattenAll(layersOut, (self.width, self.height))

	def save(self, toFilename=None):
		"""
		save this gimp image to a file
		"""
		self._forceFullyLoaded()
		if toFilename is None:
			toFilename = self.filename
		if not hasattr(toFilename, 'write'):
			f = open(toFilename, 'wb')
		f.write(self.encode_())

	def saveNew(self, toFilename=None):
		"""
		save a new gimp image to a file
		"""
		if toFilename is None:
			toFilename = self.filename
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
		ret.append('Version: ' + str(self.version))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append('Base Color Mode: ' + self.COLOR_MODES[self.baseColorMode])
		ret.append('Precision: ' + str(self.precision))
		ret.append(GimpIOBase.__repr__(self))
		if self._layerPtr:
			ret.append('Layers: ')
			for l in self.layers:
				ret.append(l.__repr__('\t'))
		if self._channelPtr:
			ret.append('Channels: ')
			for ch in self._channels:
				ret.append(ch.__repr__('\t'))
		return '\n'.join(ret)

def blendModeLookup(blendmode, blendLookup, default=BlendType.NORMAL):
	""" Get the blendmode from a lookup table """
	if blendmode not in blendLookup:
		print("WARNING " + str(blendmode) + " is not currently supported!")
		return default
	return blendLookup[blendmode]

def rasterImageOffset(image, size, offsets=(0, 0)):
	""" Rasterise an image with offset to a given size"""
	imageOffset = Image.new("RGBA", size)
	imageOffset.paste(image.convert("RGBA"), offsets, image.convert("RGBA"))
	return imageOffset

def flattenLayerOrGroup(layerOrGroup, imageDimensions, flattenedSoFar=None,
ignoreHidden=True):
	"""Flatten a layer or group on to an image of what has already been
	flattened
	Args:
		layerOrGroup (Layer|Group): A layer or a group of layers
		imageDimensions ((int, int)): size of the image
		flattenedSoFar (PIL.Image, optional): the image of what has already
		been flattened. Defaults to None.
		ignoreHidden (bool, optional): ignore layers that are hidden. Defaults
		to True.
	Returns:
		PIL.Image: Flattened image
	"""
	blendLookup = {0: BlendType.NORMAL, 3: BlendType.MULTIPLY,
	4: BlendType.SCREEN, 5: BlendType.OVERLAY, 6: BlendType.DIFFERENCE,
	7: BlendType.ADDITIVE, 8: BlendType.NEGATION, 9: BlendType.DARKEN,
	10: BlendType.LIGHTEN, 11: BlendType.HUE, 12: BlendType.SATURATION,
	13: BlendType.COLOUR, 14: BlendType.LUMINOSITY, 15: BlendType.DIVIDE,
	16: BlendType.COLOURDODGE, 17: BlendType.COLOURBURN,
	18: BlendType.HARDLIGHT, 19: BlendType.SOFTLIGHT, 20: BlendType.GRAINEXTRACT,
	21: BlendType.GRAINMERGE, 23: BlendType.OVERLAY, 24: BlendType.HUE,
	25: BlendType.SATURATION, 26: BlendType.COLOUR, 27: BlendType.LUMINOSITY,
	28: BlendType.NORMAL, 30: BlendType.MULTIPLY, 31: BlendType.SCREEN,
	32: BlendType.DIFFERENCE, 33: BlendType.ADDITIVE, 34: BlendType.NEGATION,
	35: BlendType.DARKEN, 36: BlendType.LIGHTEN, 37: BlendType.HUE,
	38: BlendType.SATURATION, 39: BlendType.COLOUR, 40: BlendType.LUMINOSITY,
	41: BlendType.DIVIDE, 42: BlendType.COLOURDODGE,
	43: BlendType.COLOURBURN, 44: BlendType.HARDLIGHT, 45: BlendType.SOFTLIGHT,
	46: BlendType.GRAINEXTRACT, 47: BlendType.GRAINMERGE,
	48: BlendType.VIVIDLIGHT, 49: BlendType.PINLIGHT, 52: BlendType.EXCLUSION}

	if isinstance(layerOrGroup, list):
		if ignoreHidden and not layerOrGroup[0].visible:
			foregroundRaster = Image.new("RGBA", imageDimensions)
		else: # A group is a list of layers
			# (see flattenAll)
			foregroundRaster = rasterImageOffset(flattenAll(layerOrGroup[1],
			imageDimensions, ignoreHidden), imageDimensions, (layerOrGroup[0].xOffset,
			layerOrGroup[0].yOffset))
		if flattenedSoFar is None:
			return foregroundRaster
		return blendLayers(flattenedSoFar, foregroundRaster,
		blendModeLookup(layerOrGroup[0].blendMode, blendLookup),
		layerOrGroup[0].opacity)

	if ignoreHidden and not layerOrGroup.visible:
		foregroundRaster = Image.new("RGBA", imageDimensions)
	else:
		# Get a raster image and apply blending
		foregroundRaster = rasterImageOffset(layerOrGroup.image, imageDimensions,
		(layerOrGroup.xOffset, layerOrGroup.yOffset))
	if flattenedSoFar is None:
		return foregroundRaster
	return blendLayers(flattenedSoFar, foregroundRaster,
	blendModeLookup(layerOrGroup.blendMode, blendLookup),
	layerOrGroup.opacity)


def flattenAll(layers, imageDimensions, ignoreHidden=True):
	"""Flatten a list of layers and groups

	Note the bottom layer is at the end of the list

	Args:
		layers ([Layer|Group]): A list of layers and groups
		imageDimensions ((int, int)): size of the image
		been flattened. Defaults to None.
		ignoreHidden (bool, optional): ignore layers that are hidden. Defaults
		to True.
	Returns:
		PIL.Image: Flattened image
	"""
	end = len(layers) - 1
	flattenedSoFar = flattenLayerOrGroup(layers[end], imageDimensions, ignoreHidden=ignoreHidden)
	for l in range(end - 1, -1, -1):
		flattenedSoFar = flattenLayerOrGroup(layers[l], imageDimensions,
		flattenedSoFar=flattenedSoFar, ignoreHidden=ignoreHidden)
	return flattenedSoFar



### ARGPARSE STUFF ###

if __name__ == '__main__':
	""" CLI Entry Point """
	parser = argparse.ArgumentParser("GimpGbrBrush.py")
	parser.add_argument("xcfdocument", action="store",
	help="xcf file to act on")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--dump", action="store_true",
	help="dump info about this file")
	group.add_argument("--showLayer", action="store_true",
	help="show layer(s) (use * for all)")
	group.add_argument("--saveLayer", action="store_true",
	help="save layer(s) out to file")
	group.add_argument("--save", action="store",
	help="save out the brush image")
	args = parser.parse_args()

	gimpDocument = GimpDocument(args.xcfdocument)

	if args.dump:
		print(gimpDocument)
	if args.showLayer:
		if args.showLayer == '*':
			for layer in range(len(gimpDocument.layers)):
				im = gimpDocument.layers[layer].image
				showLayer(im, layer)
		else:
			im = gimpDocument.layers[int(args.showLayer)].image
			showLayer(im, int(args.showLayer))
	if args.saveLayer:
		layer = args.saveLayer.split(',', 1)
		if len(layer) > 1:
			filename = layer[1]
		else:
			filename = 'layer *.png'
		layer = args.saveLayer[0]
		if layer == '*':
			if filename.find('*') < 0:
				filename = '.'.join(filename.split('.', 1).insert(1, '*'))
			for n in range(len(gimpDocument.layers)):
				saveLayer(gimpDocument, n, filename)
		else:
			saveLayer(gimpDocument, int(layer), filename)
	if args.save:
		gimpDocument.save(args.save)


def showLayer(image, l):
	""" show a layer """
	if image is None:
		print('No image for layer', l)
	else:
		print('Showing layer', l)
		image.show()


def saveLayer(gimpDoc, l, fileName):
	""" save a layer """
	iteration = gimpDoc.layers[l].image
	if iteration is None:
		print('No image for layer', l)
	else:
		fn2 = fileName.replace('*', str(l))
		print('saving layer', fn2)
		iteration.save(fn2)
