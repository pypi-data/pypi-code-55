import pandas as pd
class Voltammogram:
	def __init__(self, s_flat = 105, e_flat = 110, max_peak = 0, min_peak = 0):
		self.s_flat = s_flat
		self.e_flat = e_flat
		self.max = max_peak
		self.min = min_peak
		self.data = []
		self.x_values = []
		self.y_values = []


	def read_data_file(self, file_name):
		data = pd.read_csv(file_name)
		df = pd.DataFrame(data)
		self.x_values = [float(i) for i in df.iloc[7::, 0].tolist()]
		self.y_values = [float(i) for i in df.iloc[7::, 1].tolist()]
		return self.x_values, self.y_values
