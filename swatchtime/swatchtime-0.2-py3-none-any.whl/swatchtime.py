from datetime import datetime
from datetime import timedelta
from math import floor
import argparse


class SwatchTime:
	"""
	A small utility class to give current the Swatch Internet Time.

	Because Swatch Internet Time in time zone independent and does not
	observe daylight saving, no conversions are needed. 
	"""

	@staticmethod
	def get() -> int:
		"""
		v1, no args, outputs current swatch time
		"""
		now = datetime.utcnow() + timedelta(hours=1)
		beats = ((now.hour * 1000) + 
				 (now.minute * 1000/60) +
				 (now.second * 1000/60/60) )/24
		return floor(beats)


	def __str__(self):
		return f"{self.get()} .beats"




if __name__ == "__main__":
	# parser = argparse.ArgumentParser(
	# 	description='Converts current time to Swatch Internet Time.',
	# 	formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	# parser.add_argument('-t', '--time_zone', 
	# 					nargs=2,
	# 					default=[None, None],
	# 					metavar=("%H-%M-%S","time-zone"),
	# 					help='Set time and time zone for a conversion. Not implemented.')

	# args = parser.parse_args()

	print(SwatchTime())




