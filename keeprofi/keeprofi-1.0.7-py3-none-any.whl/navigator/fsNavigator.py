
from pathlib import PosixPath
import subprocess

import keeprofi

class FSNavigator(keeprofi.Navigator):

	def __init__(self, cwd = None):
		self.show_hidden = self.cache.show_hidden_files;
		self.cwd = (
			lambda: PosixPath(cwd),
			lambda: PosixPath.home()
		)[cwd == None]()

	def open(self):
		if (
			not hasattr(self.cache, 'last_file')
			or not keeprofi.KPNavigator(
				PosixPath(self.cache.last_file)
			).open()
		):
			self.navigate()

	def navigate(self):
		process = self.show_rofi()
		if (process.returncode != 1):
			if (process.returncode == 10):
				self.switch_hidden()
				self.navigate()
			else:
				i = int(process.stdout)
				fs_item = self.ls[i]
				if (fs_item.is_dir()):
					self.chdir(fs_item)
					self.navigate()
				elif (not keeprofi.KPNavigator(fs_item).open()):
					self.navigate()

	@property
	def ls(self):
		if (not hasattr(self, '_ls')):
			self.regen_ls()

		return self._ls

	def regen_ls(self):
		self._ls = [self.cwd.joinpath(self.up_str)] + [item
			for item in sorted(
				self.cwd.iterdir(),
				key = lambda item: str(1 * item.is_file()) + item.name
			) if (
				item.is_dir() and (
					self.show_hidden
					or not item.name.startswith('.')
				)
				or item.name.endswith('.kdbx')
			)
		]

	def ls_string(self):
		return '\n'.join((
			self.item2str(item) for item in self.ls
		))

	def item2str(self, item):
		return (
			lambda: item.name,
			lambda: self.settings.dir_format.format(name=item.name)
		)[item.is_dir()]()

	def set_hidden(self, value: bool):
		self.show_hidden = value
		self.regen_ls()

	def switch_hidden(self):
		self.cache.show_hidden_files \
			= self.show_hidden \
			= not self.show_hidden
		self.regen_ls()

	def chdir(self, path: PosixPath):
		self.cwd = path
		self.regen_ls()

	@property
	def keybindings(self):
		if (not hasattr(self, '_keybindings')):
			self._keybindings = [] \
				+ self.free_kb(self.settings.kb['hidden']) \
				+ ['-kb-custom-1', self.settings.kb['hidden']]

		return self._keybindings

	@property
	def rofi_prompt(self):
		return 'file:'
