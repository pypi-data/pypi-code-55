"""
Represents a single layer in a gimp image
"""

from binaryiotools import IO
from .GimpIOBase import GimpIOBase
from .GimpImageHierarchy import GimpImageHierarchy
from .GimpChannel import GimpChannel

class GimpLayer(GimpIOBase):
	"""
	Represents a single layer in a gimp image
	"""

	COLOR_MODES = [
	'RGB color without alpha', 'RGB color with alpha', 'Grayscale without alpha',
	'Grayscale with alpha', 'Indexed without alpha', 'Indexed with alpha']
	PIL_MODE_TO_LAYER_MODE = {'L': 2, 'LA': 3, 'RGB': 0, 'RGBA': 1}

	def __init__(self, parent, name=None, image=None):
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self.colorMode = 0
		self.name = name
		self._imageHierarchy = None
		self._imageHierarchyPtr = None
		self._mask = None
		self._maskPtr = None
		self._data = None
		if image is not None:
			self.image = image # done last as it resets some of the above defaults

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		Steps:
		Create a new IO buffer (array of binary values)
		Grab attributes as outlined in the spec
		List of properties
		Get the image hierarchy and mask pointers
		Return the offset

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		# Create a new IO buffer (array of binary values)
		io = IO(data, index)
		# Grab attributes as outlined in the spec
		self.width = io.u32
		self.height = io.u32
		self.colorMode = io.u32 # one of self.COLOR_MODES
		self.name = io.sz754
		# List of properties
		self._propertiesDecode_(io)
		# Get the image hierarchy and mask pointers
		self._imageHierarchyPtr = self._pointerDecode_(io)
		self._maskPtr = self._pointerDecode_(io)
		self._mask = None
		self._data = data
		# Return the offset
		return io.index

	def encode_(self):
		"""
		encode to byte array

		Steps:
		Create a new IO buffer (array of binary values)
		Set attributes as outlined in the spec
		List of properties
		Set the image hierarchy and mask pointers
		Return the data

		"""
		# Create a new IO buffer (array of binary values)
		dataAreaIO = IO()
		io = IO()
		# Set attributes as outlined in the spec
		io.u32 = self.width
		io.u32 = self.height
		io.u32 = self.colorMode
		io.sz754 = self.name
		# Layer properties
		io.addBytes(self._propertiesEncode_())
		# Pointer to the image heirachy structure
		dataAreaIndex = io.index + self._POINTER_SIZE_ * 2
		io.addBytes(self._pointerEncode_(dataAreaIndex))
		dataAreaIO.addBytes(self.imageHierarchy.encode_())
		#io.addBytes(self._pointerEncode_(dataAreaIndex))
		# Pointer to the layer mask
		if self.mask is not None:
			dataAreaIO.addBytes(self.mask.encode_())
		io.addBytes(self._pointerEncode_(dataAreaIndex + dataAreaIO.index))
		io.addBytes(dataAreaIO)
		# Return the data
		return io.data

	@property
	def mask(self):
		"""
		Get the layer mask
		"""
		if self._mask is None and self._maskPtr is not None and self._maskPtr != 0:
			self._mask = GimpChannel(self)
			self._mask.decode_(self._data, self._maskPtr)
		return self._mask

	@property
	def image(self):
		"""
		get the layer image

		NOTE: can return None!
		"""
		if self.imageHierarchy is None:
			return None
		return self.imageHierarchy.image

	@image.setter
	def image(self, image):
		"""
		set the layer image

		NOTE: resets layer width, height, and colorMode
		"""
		self.height = image.height
		self.width = image.width
		if image.mode not in self.PIL_MODE_TO_LAYER_MODE:
			raise NotImplementedError('No way of handlng PIL image mode "' + image.mode + '"')
		self.colorMode = self.PIL_MODE_TO_LAYER_MODE[image.mode]
		if not self.name and isinstance(image, str):
			# try to use a filename as the name
			self.name = image.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
		self._imageHierarchy = GimpImageHierarchy(self)
		self._imageHierarchy.image = image

	@property
	def imageHierarchy(self):
		"""
		Get the image hierarchy objects

		This is mainly needed for deciphering image, and therefore,
		of little use to you, the user.

		NOTE: can return None if it has been fully read into an image
		"""
		if self._imageHierarchy is None and self._imageHierarchyPtr > 0:
			self._imageHierarchy = GimpImageHierarchy(self)
			self._imageHierarchy.decode_(self._data, self._imageHierarchyPtr)
		return self._imageHierarchy

	@imageHierarchy.setter
	def imageHierarchy(self, imgHierarchy):
		""" set the image hierarchy """
		self._imageHierarchy = imgHierarchy


	def _forceFullyLoaded(self):
		"""
		make sure everything is fully loaded from the file
		"""
		if self.mask is not None:
			self.mask._forceFullyLoaded()
		_ = self.image # make sure the image is loaded so we can delete the hierarchy nonsense
		#self._imageHierarchy = None
		#self._data = None

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Name: ' + str(self.name))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append('colorMode: ' + self.COLOR_MODES[self.colorMode])
		ret.append(GimpIOBase.__repr__(self, indent))
		m = self.mask
		if m is not None:
			ret.append('Mask:')
			ret.append(m.__repr__(indent + '\t'))
		return indent + (('\n' + indent).join(ret))
