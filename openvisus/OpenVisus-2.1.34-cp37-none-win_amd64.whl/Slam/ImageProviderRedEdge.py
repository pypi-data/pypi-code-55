
from OpenVisus.Slam import *

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
class ImageProviderRedEdge(ImageProvider):
	
	#  constructor (TODO: panel_calibration)
	def __init__(self,panel_calibration=[0.67, 0.69, 0.68, 0.61, 0.67]):
		super().__init__()
		self.panel_calibration=panel_calibration
		self.panel_irradiance=None
		self.camera_yaw=math.pi # in the sequence I have the yaw is respect to the south
	
	# example: NIR_608.TIF  / RGB_608.TIF / Thermal_608.TIF returns 608
	def getGroupId(self,filename):
		filename=os.path.basename(filename)
		v=os.path.splitext(filename)[0].split("_")
		if len(v)<2 or not v[-2].isdigit(): return ""
		return v[-2]

	# findPanels
	def findPanels(self):
		print("Finding panels...")
		self.panels=[]
		for img in self.images.copy():
			panel = micasense.panel.Panel(micasense.image.Image(img.filenames[0]))
			if not panel.panel_detected(): break
			print(img.filenames,"is panel")
			self.panels.append(img)
			self.images.remove(img)
		panel = micasense.capture.Capture.from_filelist(self.panels[0].filenames) 
		self.panel_irradiance = panel.panel_irradiance(self.panel_calibration)	
		print("panel_irradiance",self.panel_irradiance)

	# generateImage
	def generateImage(self,img):
		capture = micasense.capture.Capture.from_filelist(img.filenames)
		# note I'm ignoring distotions here
		# capture.images[I].undistorted(capture.images[I].reflectance())
		multi = capture.reflectance(self.panel_irradiance)
		multi = [single.astype('float32') for single in multi]
		multi = self.mirrorY(multi)
		multi = self.swapRedAndBlue(multi)
		multi = self.undistortImage(multi)
		multi = self.alignImage(multi)
		return multi

# /////////////////////////////////////////////////////////////////////////////////////////////////////
def CreateInstance(metadata):
	exit_make =metadata["EXIF:Make"].lower()  if "EXIF:Make"  in metadata else ""
	exif_model=metadata["EXIF:Model"].lower() if "EXIF:Model" in metadata else ""
	if "rededge" in exif_model or "rededge" in exif_model:
		return ImageProviderRedEdge()
	else:
		return None