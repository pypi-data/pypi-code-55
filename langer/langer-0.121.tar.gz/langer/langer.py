"""
Langer - V0.121
Simple translate html pages.
Maked for simple translating small flask sites.
BY: @Djangoner, valeraefimov6@gmail.com.

Use Example:

import langer
from langer import phrase as _
langer.LANG = "en"
langer.LANGS = ["ru"]
langer.init()

print(_('hello_world','ru')) # Phrase ID
print(_('Hello World!','ru')) # Phrase in English

Flask Example:
...
@app.after_request
def langer_translate(response):
	response_text = response.data.decode("utf8")
	translate_lang = session.get("translate")
	if langer:
		try:
			response_text = langer.translate_text(response_text, translate_lang)
		except Exception as e:
			TTX = f"Langer translating page error: {e}"
			logging.exception(TTX)
			return response
	response.data = response_text.encode("utf8")
	return response
"""
from lxml import html
import os, json
# import logging
import re

class LangNotAdded(ValueError):
	def __init__(self):
		super().__init__("lang is not in LANGS")


class ListDump:
	data = []
	def __init__(self, file):
		self.file = file
		self._read()
	def _read(self):
		if not os.path.exists(self.file):
			self._write()
		with open(self.file,"rb") as f:
			self.data = [i for i in f.read().decode("utf8").split("\n") if i.strip()]
	def _write(self):
		with open(self.file,"wb") as f:
			f.write("\n".join(self.data).encode("utf8"))
	def update(self, data):
		self.data = data
		self._write()
	def extend(self, data):
		self.data.extend(data)
		self._write()
	def get(self):
		return self.data
class DictReplacer:
	data = {}
	auto_save = False
	def __init__(self):
		pass
	def __setitem__(self, key, value):
		self.data[key] = value
		self._autosave_check()
	def __getitem__(self, key):
		return self.data[key]
	def __delitem__(self, key):
		del self.data[key]
		self._autosave_check()
	def __repr__(self):
		return self.data
	def __str__(self):
		return f"DictReplacer {self.file}"
	def _autosave_check(self):
		if self.autosave:
			self._autosave()
	def _autosave(self):
		self._write()
class LangReader(DictReplacer):
	"TODO"
	file = None
	data = {}
	auto_save = True
	def __init__(self, lang, read = True, auto_save = True):
		self.file = self.file_path(lang)
		if not lang in LANGS:
			raise LangNotAdded()
		self.lang = lang
		self.auto_save = auto_save
		if read:
			self.read()
	@staticmethod
	def file_path(lang):
		return os.path.join(LANG_DIR, lang+LANG_EXT)
	def write(self, data = None):
		if data == None:
			data = self.data
		with open(self.file, "wb") as f:
			f.write("\n".join([DELIMITER.join([k,v]) for k,v in data.items() if k.strip()]).encode("utf8")) # Translates[self.lang]
	def read(self):
		if not os.path.exists(self.file):
			self.write()
		with open(self.file, "rb") as f:
			content_raw = [i.split(DELIMITER) for i in f.read().decode("utf8").split("\n") if i.strip()]
			content = {k:v for k,v in content_raw}
		# Translates[self.lang] = content
		self.data = content
		return content
	save = write
# LogFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# logging.basicConfig(filename="logs/langer.log", level = logging.DEBUG, format = LogFormat)

LANG = "en"
TRANSLATE_LANG = None # Language default used for phrase translating. 
LANGS = ["ru", "tr"]
ADD_MAIN_LANG = False # Adding main lang to LANGS. Use if you specifing ID, not phrase in main lang.

AUTO_DETECT_LANGS = True # Scan LANG_DIR for langs
LANG_DIR = "langs" # Dir with lang files
LANG_EXT = ".lang" # Extension of lang files
DELIMITER = "||" # Delimiter in lang files.

TRANSLATE_ENABLE = True # TestFunc
CACHE_PHRASES = False # Cache all phrases to phrases.phrases
PHRASES = [] # Phrases that finded everywhere
PHRASES_APP = [] # Phrases in app
SCAN_APP = True # Scan app for _() calls.
SCAN_FILE = None # File for scan. Set it to __file__ in your app
if not os.path.exists(LANG_DIR):
	os.mkdir(LANG_DIR)
PHRASES_DUMP = ListDump(os.path.join(LANG_DIR, "phrases.phrases"))

SEARCH_CALLS = True
SEARCH_CALLS_RE = "[^_]_\((.*)\)"# Any starts with _()

def clean_quotes(string):
	quotes = ['\"', "\'"]
	# print(string[-1] in quotes, string[-1]=='\"', quotes)
	if string[0] in quotes:
		string = string[1:]
	if string[-1] in quotes:
		string = string[:-1]
	return string

def scan_app():
	if not SCAN_FILE:
		return
	with open(SCAN_FILE, "rb") as f:
		content = f.read().decode("utf8")
	#####
	raw = re.findall(SEARCH_CALLS_RE, content)
	calls = [clean_quotes(i) for i in raw if i.strip()]
	# print(calls)
	PHRASES_APP.extend(calls)


def add_phrases(*args):
	R = []
	for item in args:
		if isinstance(item, list):
			R.extend(item)
		else:
			R.append(item)

	unique = [i for i in R if not i in PHRASES]
	if unique:
		PHRASES_APP.extend(*unique)
		if CACHE_PHRASES:
			PHRASES_DUMP.extend(unique)
def phrase(text, lang = None):
	if not lang:
		if TRANSLATE_LANG:
			lang = TRANSLATE_LANG
		else:
			lang = LANGS[0]
	phrase = text#clear_from_fstring(text)
	if not phrase in PHRASES:
		add_phrases(phrase)
	translate = translate_raw(phrase, lang)
	return translate
	# PHRASES_APP.append(text)
	# print(f"New phrase: {text}")

TEMPLATES_DIR = "templates"
Translates = {}

def clear_from_fstring(string):
	return re.sub("{.*}\W", "", string)

def translate_save(lang):
	file = os.path.join(LANG_DIR, lang+LANG_EXT)
	with open(file, "wb") as f:
		f.write("\n".join([DELIMITER.join([k,v]) for k,v in Translates[lang].items() if k.strip()]).encode("utf8"))

def translate_prc():
	R = {}
	for lang in LANGS:
		changed = 0
		total = len(Translates[lang])
		for phrase, translate in Translates[lang].items():
			if translate:
				changed += 1
		if lang == LANG:
			chaned = total
		prc = int((changed/total) * 100)
		R[lang] = {"prc":prc, "changed":changed, "total":total, "not_changed":total - changed}
	return R
def init():
	global PHRASES
	PHRASES.clear()
	Translates.clear()
	# if not LANG in LANGS:
	# 	LANGS.append(LANG)
	if AUTO_DETECT_LANGS:
		for lang in os.listdir(LANG_DIR):
			name, ext = os.path.splitext(lang)
			if not name in LANGS:
				if ext != LANG_EXT: continue
				LANGS.append(name)
	###--- Finding dir
	if not os.path.isdir(LANG_DIR):
		os.mkdir(LANG_DIR)
	# LangsFinded = os.listdir(LANG_DIR)
	###--- Checking for new texts
	if not os.path.exists(TEMPLATES_DIR):
		Files = []
	else:
		Files = os.listdir(TEMPLATES_DIR) # Searching for flask templates
	all_texts = [] # List for finded texts
	for filename in Files: # for each file in TEMPLATEDS_DIR
		file = os.path.join(TEMPLATES_DIR, filename) # full path to file
		texts = translate_file(file, only_texts = True) # Translating text
		all_texts.extend([tx for tx in texts if not tx in all_texts]) # adding text to all_texts without repeat


	###--- Checking for lang files


	MainLang = os.path.join(LANG_DIR, LANG+LANG_EXT) # Main lang file
	# if not os.path.exists(MainLang): # If not exists
	# 	with open(MainLang, "w") as f: # Creating
	# 		f.write("") # Empty file
	# with open(MainLang, "rb") as f: # Opening file
		# content = f.read().decode("utf8").split("\n") # Reading content
		# initial_content = content
	if SCAN_APP:
		scan_app()
	def unique_extend(items):
		for item in items:
			if not item in PHRASES:
				PHRASES.append(item)
	unique_extend(all_texts)
	unique_extend(PHRASES_APP)
	if CACHE_PHRASES:
		unique_extend(PHRASES_DUMP.get())
		PHRASES_DUMP.extend([i for i in PHRASES if not i in PHRASES_DUMP])
	# print(PHRASES)
	# PHRASES = list(TEMP)
	# Translates[LANG] = content

	# if content != initial_content:
		# with open(MainLang, "wb") as f: # Writing Main lang file
			# f.write("\n".join([i for i in content if i.strip()]).encode("utf8")) # edited lines
	for lang in LANGS: # Searching lang files
		file = os.path.join(LANG_DIR, f"{lang}{LANG_EXT}")
		is_main = lang == LANG
		if not os.path.exists(file):
			with open(file,"w") as f:
				f.write("")
	# 	###
		with open(file, "rb") as f:
			content_raw = [i.split(DELIMITER) for i in f.read().decode("utf8").split("\n") if i.strip()]
			content = {k:v for k,v in content_raw}
			initial_content = content.copy()
		###
		# for i, line in enumerate(Translates[LANG]):
			# if len(content) <= i:
				# content.append(line)
		###
		for phrase in PHRASES:
			if not phrase in content:
				content[phrase] = ""
		# print(content)
		Translates[lang] = content
		if initial_content != content:
			translate_save(lang)
		
def translate_raw(text, language):
	"Translates raw text"
	if not language in Translates:
		return text

	R = Translates[language].get(text, text)
	if not R.strip():
		R = text
	# logging.debug(f"Translated {text} > {R}")
	return R
	# return text

def translate_file(file, *args, **kwargs):
	"Translates HTML File to translated text"
	with open(file,"rb") as f:
		text = f.read().decode("utf8")
	return translate_text(text, *args, **kwargs)
def translate_text(text, language = None, only_texts = False):
	"Translates HTML text to translated text"
	# logging.debug(f"Translating to language: {language}")
	if not language:
		language = LANGS[0]
	tree = html.fromstring(text)
	raw_items = tree.xpath("//*")
	texts = []
	parsed_items = []
	for raw_item in raw_items:
		item = raw_item.text
		if not item:
			continue
		item = item.replace("\t","").replace("№","#").strip().replace("\n", "|n|")
		tag = raw_item.tag
		#####
		if not item:
			continue
		if tag in ["script", "style"]: # Ignore tags
			continue
		if "{%" in item and "%}" in item:
			continue
		if "{{" in item and "}}" in item:
			continue
		# print(raw_item.tag,"|||", item)
		# texts.append(item)
		if not only_texts and TRANSLATE_ENABLE:
			###Here translating
			item = translate_raw(item, language)
		raw_item.text = item
		parsed_items.append(raw_item)
	if only_texts:
		return [i.text for i in parsed_items]
	else:
		return html.tostring(tree).decode("utf8")
		# return html.text_content()
if __name__ == "__main__":
	init()
	for lang, data in translate_prc().items():
		print(f"{lang} - {data['prc']}% ({data['changed']}/{data['total']})")
	# print(translate_file("error.html", "ru"))