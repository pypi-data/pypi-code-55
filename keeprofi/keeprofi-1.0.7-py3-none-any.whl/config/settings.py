
import os
import xdg
from pathlib import PosixPath

import keeprofi

class Settings(keeprofi.Resource):
	ACTION_COPY: 'copy'
	ACTION_TYPE: 'type'

	@property
	def defaults(self):
		return {
			'kb': {
				'hidden': 'Control+h',
				'custom_action': 'Control+Return',
				'pass_attrs': 'Shift+Return',
			},
			'icons': {
				'success': 'keepassxc-dark',
				'fail': 'keepassxc-locked',
			},
			'default_action': 'copy',
			'remember_pass': False,
			'dir_format': '/{name}'
		}

	@property
	def path(self):
		config_home = xdg.XDG_CONFIG_HOME.as_posix()
		return PosixPath(
			config_home \
			+ (
				'/keeprofi',
				'/.keeprofi',
			)[int(os.environ['HOME'] == config_home)] \
			+ '/config.json'
		)

	def is_copy_default(self):
		consts = self.__class__.__dict__.get('__annotations__')

		return self.default_action == consts['ACTION_COPY']
