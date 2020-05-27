
import subprocess
import re

import keeprofi

class Navigator():

	def open(self):
		pass

	def navigate(self):
		pass

	def show_rofi(self):
		return subprocess.run(
			[
				'rofi',
				'-dmenu',
				'-no-custom',
				'-format',
				'i',
				'-p',
				self.rofi_prompt,
			] + self.keybindings,
			input = self.ls_string(),
			text = True,
			capture_output = True
		)

	@property
	def ls(self):
		pass

	def regen_ls(self):
		pass

	def ls_string(self):
		pass

	def chdir(self):
		pass

	@property
	def keybindings(self):
		pass

	def free_kb(self, kb):
		result = []

		r = subprocess.run(
			'rofi -dump-xresources | grep ' + kb,
			shell = True,
			text = True,
			capture_output = True
		)

		if (r.stdout):
			bind = re.compile(r'^! rofi.(.+):\s+(.+)$')
			(name, keys) = bind.match(r.stdout).groups()
			keys = keys.split(',')
			keys.remove(kb)

			result = ['-' + name, ','.join(keys)]

		return result

	@property
	def rofi_prompt(self):
		pass

	@property
	def settings(self):
		if (not hasattr(self, '_settings')):
			self._settings = keeprofi.Settings.get()

		return self._settings

	@property
	def cache(self):
		if (not hasattr(self, '_cache')):
			self._cache = keeprofi.Cache.get()

		return self._cache

	@property
	def up_str(self):
		return '..'


