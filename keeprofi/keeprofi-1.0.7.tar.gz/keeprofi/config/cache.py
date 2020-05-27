
import os
import xdg
from pathlib import PosixPath

import keeprofi

class Cache(keeprofi.Resource):

	@property
	def defaults(self):
		return {
			'show_hidden_files': False,
			'keyring_timestamp': 0,
		}

	@property
	def path(self):
		data_home = xdg.XDG_DATA_HOME.as_posix()
		return PosixPath(
			data_home \
			+ (
				'/keeprofi',
				'/.keeprofi',
			)[int(os.environ['HOME'] == data_home)] \
			+ '/cache.json'
		)
