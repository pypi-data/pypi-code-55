
import sys
from pathlib import PosixPath
import subprocess

from pykeepass import PyKeePass
from pykeepass.group import Group
from pykeepass.entry import Entry
from pynput.keyboard import Controller
import xerox

import keeprofi

class KPNavigator(keeprofi.Navigator):

	def __init__(self, path: PosixPath):
		self.kp = None
		self.path = path
		self.process = None

	def open(self):
		password = self.keyring.get_pass()

		if (not password or not self.init_keepass(password)):
			self.process = self.ask_pass()

			if (self.process.returncode == 1):
				return self.exit()

			password = self.process.stdout.strip()

			if (password == self.up_str):
				return False

		if (not self.kp and not self.init_keepass(password)):
			return self.wrong_password()

		self.keyring.save_pass(password)
		self.cache.last_file = self.path.as_posix()
		self.cwg = self.kp.root_group

		return self.navigate()

	def init_keepass(self, password):
		try:
			self.kp = PyKeePass(
				self.path.as_posix(),
				password=password
			)
		except Exception as e:
			pass

		return self.kp

	def ask_pass(self):
		return subprocess.run(
			[
				'rofi',
				'-dmenu',
				'-password',
				'-p',
				'pass:',
			],
			input = self.up_str,
			text = True,
			capture_output = True
		)

	def wrong_password(self):
		keeprofi.Notify(
			'Wrong password',
			self.path.as_posix(),
			self.settings.icons['fail']
		).show()

		return True

	@property
	def selection(self):
		item = None
		if (self.process.returncode != 1):
			i = int(self.process.stdout)
			item = self.ls[i]

		return item

	def navigate(self):
		self.process = self.show_rofi()

		return (
			self.act,
			self.exit,
		)[self.process.returncode == 1]()

	def exit(self):
		return True

	def act(self):
		if (isinstance(self.selection, Group)):
			return self.chgroup()
		else:
			return {
				0:  self.default_action,
				10: self.custom_action,
				11: self.navigate_entry,
			}[self.process.returncode]()

	def default_action(self):
		if (self.settings.is_copy_default()):
			self.copy_pass(self.selection)
		else:
			self.type_pass(self.selection)

		return True

	def custom_action(self):
		if (self.settings.is_copy_default()):
			self.type_pass(self.selection)
		else:
			self.copy_pass(self.selection)

		return True

	def navigate_entry(self):
		if (keeprofi.KPEntryNavigator(self.selection).open()):
			return True
		else:
			return self.navigate()

	def copy_pass(self, entry: Entry):
		xerox.copy(entry.password)
		keeprofi.Notify(
			'Password copied',
			self.entry_title(entry),
			self.settings.icons['success']
		).show()

	def type_pass(self, entry: Entry):
		Controller().type(entry.password)

	def chgroup(self):
		if (self.selection == self.cwg):
			delattr(self.cache, 'last_file')
			return False

		self.chdir(self.selection)

		return self.navigate()

	def chdir(self, group):
		self.cwg = group
		self.regen_ls()

	@property
	def ls(self):
		if (not hasattr(self, '_ls')):
			self.regen_ls()

		return self._ls

	def regen_ls(self):
		self._ls = [self.parentgroup()]\
			+ sorted(
				self.cwg.subgroups,
				key = lambda g: g.name
			) + sorted(
				self.cwg.entries,
				key = lambda e: self.entry_title(e)
			)

	def parentgroup(self):
		group = self.cwg.parentgroup or self.cwg
		group.name = self.up_str

		return group

	def ls_string(self):
		return '\n'.join((
			self.item2str(item) for item in self.ls
		))

	def item2str(self, item):
		return (
			lambda: self.entry_title(item),
			lambda: '/' + item.name
		)[isinstance(item, Group)]()

	def entry_title(self, entry):
		return entry.title \
			or entry.username \
			or entry.url \
			or 'Entry#' + entry.uuid

	@property
	def keybindings(self):
		if (not hasattr(self, '_keybindings')):
			self._keybindings = [] \
				+ self.free_kb(self.settings.kb['custom_action']) \
				+ self.free_kb(self.settings.kb['pass_attrs']) \
				+ ['-kb-custom-1', self.settings.kb['custom_action']] \
				+ ['-kb-custom-2', self.settings.kb['pass_attrs']]

		return self._keybindings

	@property
	def rofi_prompt(self):
		return 'kbd:'

	@property
	def keyring(self):
		if (not hasattr(self, '_keyring')):
			self._keyring = keeprofi.Keyring.get()

		return self._keyring
