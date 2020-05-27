
from pykeepass.entry import Entry
from pynput.keyboard import Controller
import xerox

import keeprofi

class KPEntryNavigator(keeprofi.Navigator):

	def __init__(self, entry: Entry):
		self.entry = entry
		self.process = None

	def open(self):
		return self.navigate()

	def navigate(self):
		self.process = self.show_rofi()

		return (
			self.act,
			self.exit,
		)[self.process.returncode == 1]()

	@property
	def selection(self):
		item = None
		if (self.process.returncode != 1):
			i = int(self.process.stdout)
			item = self.ls[i]

		return item

	@property
	def selection_value(self):
		return (
			lambda: self.entry.custom_properties[self.selection],
			lambda: getattr(self.entry, self.selection)
		)[hasattr(self.entry, self.selection)]()

	def exit(self):
		return True

	def act(self):
		if (self.selection == self.up_str):
			return False

		return {
			0:  self.default_action,
			10: self.custom_action,
		}[self.process.returncode]()

		return True

	def default_action(self):
		if (self.settings.is_copy_default()):
			self.copy_pass(self.selection_value)
		else:
			self.type_pass(self.selection_value)

		return True

	def custom_action(self):
		if (self.settings.is_copy_default()):
			self.type_pass(self.selection_value)
		else:
			self.copy_pass(self.selection_value)

		return True

	def copy_pass(self, value):
		xerox.copy(value)
		keeprofi.Notify(
			'Password attribute copied',
			self.entry.title + '.' + self.selection,
			self.settings.icons['success']
		).show()

	def type_pass(self, value):
		Controller().type(value)

	@property
	def ls(self):
		if (not hasattr(self, '_ls')):
			self.regen_ls()

		return self._ls

	def regen_ls(self):
		self._ls = [self.up_str] + [
			attr for attr in [
				'password',
				'username',
				'url',
				'notes',
				'tags',
			] if (getattr(self.entry, attr))
		] + [k for k, v in self.entry.custom_properties.items()]

	def ls_string(self):
		return '\n'.join(self.ls)

	@property
	def keybindings(self):
		if (not hasattr(self, '_keybindings')):
			self._keybindings = [] \
				+ self.free_kb(self.settings.kb['custom_action']) \
				+ ['-kb-custom-1', self.settings.kb['custom_action']]

		return self._keybindings

	@property
	def rofi_prompt(self):
		return 'entry:'
