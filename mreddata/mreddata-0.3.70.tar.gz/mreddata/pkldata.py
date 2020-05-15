import pandas as pd
import pickle as pkl
from .datatools import _HistogramList, options
 
class PklData(_HistogramList):
	#Expects a dictionary (or eventually list -- TODO) with keys set to the histogram name and values set to the output format generated by Histogram().to_string in MRED. 
	# what about saving directly as a list of lists? consider this possibility too
	def __init__(self):
		self.__rawdata = {}#should tihs be a dict? Yes -- with the key being each filename
		self.__loadRawData()
		super().__init__(self.__getHistogramNames())
		self.__parseRawData()
		self.__getNormalizationInfo()
		options.fullpath = True

		## if the items in __rawdata are list-type, then assume only one histogram per file
		## if dictionary type, then check each value to see if it's list or string type (string being default)

	__filenames = property(lambda self: set([x.fullpath.split(" - ")[0] for x in self.histograms]), None, None, "")

	def __getNormalizationInfo(self):
		print("Getting information for normalization (pickle files loaded)" )
		for filename in self.__filenames:
			self.normalize(filename)

	def normalize(self, filename):	
		if not options.no_norm:
			print("-----------------------------")
			print("filename: {}".format(filename))
			while True:
				try:
					nIons = int(input("\tnIons: "))
					gfu = float(input("\tgun fluence unit: "))
					break
				except KeyboardInterrupt:
					return False		
				except:
					print("ERROR: enter a valid value")
		else:
			nIons=1
			gfu=1
		for name, histogram in self.histogramsDict.items():
			if filename in name:
				histogram.normFactor = gfu * nIons
				histogram.normalize()

	def __loadRawData(self):
		#explicit or automatic type comprehension?
		for filename in options.files:
			if '.pkl' in filename:
				try:
					print("attempting to load file: {}".format(filename))
					with open(filename, "rb") as f:
						self.__rawdata[filename] = pkl.load(f)
				except Exception as e:
					print("Error loading pickle data for the file: {}".format(filename))
					print(e)
					
	def __getHistogramNames(self):
		names = []
		for filename, histogram in self.__rawdata.items():
			if type(histogram) == list:
				names.append(filename + " - data")
			elif type(histogram) == dict:
				for k in histogram.keys():
					names.append(filename + " - " + k)
			else:
				print("ERROR: Expected types for pickle objects are lists or strings. ")
		return names

	def __parseRawData(self):
		for filename, histogramData in self.__rawdata.items():
			if type(histogramData) == list:
				histogram = self.histogramsDict[filename + " - data"]
				df = pd.DataFrame(histogramData).T
				df.columns = ['x', 'y', 'y2', 'xy', 'x2y', 'n', 'w', 'edges']
				histogram.setDF(df)
			elif type(histogramData) == dict:
				for hName, hValue in histogramData.items():
					histogram = self.histogramsDict[filename + " - " + hName]
					# Convert string histogram object (from histogram.to_string method in MRED)
					if type(hValue) == str:
						splitValues = [x.split(",") for x in hValue.split("(") if len(x) > 1]
						df = pd.DataFrame([[float(x.split(")")[0]) for x in s if len(x) > 1] for s in splitValues]).T
						df.columns = ['x', 'y', 'y2', 'xy', 'x2y', 'n', 'w', 'edges']
					else:#type(hValue) == list or type(hValue) == :numpy? ? TODO: Test this option!
						df = pd.DataFrame(hValue).T
						df.columns = ['x', 'y', 'y2', 'xy', 'x2y', 'n', 'w', 'edges']

					histogram.setDF(df)
			else:
				print("ERROR: Expected types for pickle objects are lists or strings. ")
