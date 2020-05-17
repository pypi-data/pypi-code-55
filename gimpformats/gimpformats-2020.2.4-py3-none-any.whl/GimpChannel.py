"""
Represents a single channel or mask in a gimp image
"""

from binaryiotools import IO
from .GimpIOBase import GimpIOBase
from .GimpImageHierarchy import GimpImageHierarchy


class GimpChannel(GimpIOBase):
	"""
	Represents a single channel or mask in a gimp image
	"""
	def __init__(self, parent, name='', image=None):
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self.name = name
		self._imageHierarchy = None
		self._imageHierarchyPtr = None
		if image is not None: # this is last because image can reset values
			self.image = image
		self._data = None

	def decode_(self, data, index=0):
		"""
		decode a byte buffer

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		io = IO(data, index)
		#print 'Decoding channel at',index
		self.width = io.u32
		self.height = io.u32
		self.name = io.sz754
		self._propertiesDecode_(io)
		self._imageHierarchyPtr = self._pointerDecode_(io)
		self._data = io.data
		return io.index

	def encode_(self):
		"""
		encode this object to a byte buffer
		"""
		io = IO()
		io.u32 = self.width
		io.u32 = self.height
		io.sz754 = self.name
		io.addBytes(self._propertiesEncode_())
		ih = self._imageHierarchyPtr
		if ih is None:
			ih = 0
		io.addBytes(self._pointerEncode_(ih))
		return io.data

	@property
	def image(self):
		"""
		get a final, compiled image
		"""
		return self.imageHierarchy.image

	@image.setter
	def image(self, image):
		"""
		get a final, compiled image
		"""
		self.width = image.width
		self.height = image.height
		if not self.name and isinstance(image, str):
			# try to use a filename as the name
			self.name = image.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
		self._imageHierarchy = GimpImageHierarchy(self, image)

	def _forceFullyLoaded(self):
		"""
		make sure everything is fully loaded from the file
		"""
		_ = self.image # make sure the image is loaded so we can delete the hierarchy nonsense
		self._imageHierarchyPtr = None
		self._data = None

	@property
	def imageHierarchy(self):
		"""
		Get the image hierarchy

		This is mainly used for decoding the image, so
		not much use to you.
		"""
		if self._imageHierarchy is None:
			self._imageHierarchy = GimpImageHierarchy(self)
			self._imageHierarchy.decode_(self._data, self._imageHierarchyPtr)
		return self._imageHierarchy

	def __repr__(self, indent=''):
		"""
		Get a textual representation of this object
		"""
		ret = []
		ret.append('Name: ' + str(self.name))
		ret.append('Size: ' + str(self.width) + ' x ' + str(self.height))
		ret.append(GimpIOBase.__repr__(self, indent))
		return indent + (('\n' + indent).join(ret))
