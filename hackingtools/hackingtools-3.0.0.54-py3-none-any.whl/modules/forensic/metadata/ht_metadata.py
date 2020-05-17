from hackingtools.core import Logger, Config
import hackingtools as ht

from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfrw import PdfReader, PdfWriter 
# import mutagen

import os

config = Config.getConfig(parentKey='modules', key='ht_metadata')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'get_pdf_exif'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_metadata'), debug_module=True)

	def get_image_exif(self, filename):
		Logger.printMessage(message='{methodName}'.format(methodName='get_image_exif'), description=filename, debug_module=True)
		try:
			img_file = Image.open(filename)
			img_file.verify()
			info = img_file._getexif()
			return info
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
			return e
		return -1

	def get_pdf_exif(self, pdf_file):
		Logger.printMessage(message='{methodName}'.format(methodName='get_pdf_exif'), description=pdf_file, debug_module=True)
		info = ''
		data = {}
		try:
			with open(pdf_file, 'rb') as f:
				pdf = PdfFileReader(f)
				info = pdf.getDocumentInfo()
				number_of_pages = pdf.getNumPages()
			for a in info:
				data[a] = info[a]
			return data
		except Exception as e:
			Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
			return e
		return -1
	
	def set_pdf_author(self, pdf_file, author):
		try:
			trailer = PdfReader(pdf_file)    
			trailer.Info.Creator = author
			new_pdf = 'edited-{f}'.format(f=os.path.split(pdf_file)[1])
			new_file = os.path.join( os.path.split(pdf_file)[0], new_pdf)
			PdfWriter(new_file, trailer=trailer).write()
			return new_file
		except Exception as e:
			Logger.printMessage(str(e), is_error=True)

	# def get_audio_video_exif(self, filename):
	# 	Logger.printMessage(message='{methodName}'.format(methodName='get_audio_video_exif'), description=filename, debug_module=True)
	# 	try:
	# 		my_file = mutagen.File(filename)
	# 		img_file.verify()
	# 		info = img_file._getexif()
	# 		return info
	# 	except Exception as e:
	# 		Logger.printMessage(message='{methodName}'.format(methodName='exception'), description=e, debug_module=True)
	# 		return e
	# 	return -1
