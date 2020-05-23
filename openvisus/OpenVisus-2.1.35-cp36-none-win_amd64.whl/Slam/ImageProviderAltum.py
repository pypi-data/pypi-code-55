
from OpenVisus.Slam import *
import tifffile

# this is needed to find micasense module
import sys,os,platform
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import micasense
import micasense.utils 
import micasense.metadata
import micasense.plotutils
import micasense.image 
import micasense.imageutils
import micasense.panel 
import micasense.capture 

# /////////////////////////////////////////////////////////////////////////////////////////////////////
# see https://github.com/micasense/imageprocessing/blob/master/Alignment.ipynb
class ImageProviderAltum(ImageProvider):
	
	# example: IMG_0089_1.TIF  / IMG_0089_2.TIF / IMG_0089_2.TIF ... (6 channels)
	def getGroupId(self,filename):
		filename=os.path.basename(filename)
		v=os.path.splitext(filename)[0].split("_")
		if len(v)<2 or not v[-2].isdigit(): return ""
		return v[-2]

	# generateImage
	def generateImage(self,img):
		# NOTE: here I m skipping the 6th channel (thermal) because it has different size
		# TODO add support for different resolution channels
		multi = [numpy.array(tifffile.imread(filename)) for filename in img.filenames[:4]] 
		multi = [ConvertImageToUint8(single) for single in multi] 
		multi = self.mirrorY(multi)
		multi = self.swapRedAndBlue(multi)
		multi = self.undistortImage(multi)
		multi = self.alignImage(multi)
		return multi

# /////////////////////////////////////////////////////////////////////////////////////////////////////
def CreateInstance(metadata):
	exit_make =metadata["EXIF:Make"].lower()  if "EXIF:Make"  in metadata else ""
	exif_model=metadata["EXIF:Model"].lower() if "EXIF:Model" in metadata else ""
	if "altum" in exif_model or "altum" in exit_make:
		return ImageProviderAltum()
	else:
		return None