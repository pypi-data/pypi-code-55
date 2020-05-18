#!/usr/bin/env python3

# © 2020, Midgard
# License: LGPL-3.0-or-later

import sys
import io
import csv
import itertools
from builtins import str as _str, list as _list, tuple as _tuple, map as _map, filter as _filter


class ipo:
	def __init__(self, function):
		self.function = function


	# Make it possible to pipe, e.g.
	#   [1, 5, 3] | sort
	def __ror__(self, data):
		return self.function(data)


	# Make it possible to provide arguments, e.g. the call to `take` in
	#   [1, 5, 3, 4] | take(3)
	def __call__(self, *args, **kwargs):
		return ipo(lambda data: self.function(data, *args, **kwargs))


	# Enable chaining pipes that have not received data, e.g.
	#   get_top3 = sort | take(3)
	#   top3 = [1, 5, 3, 4] | get_top3
	def __or__(self, other):
		if not isinstance(other, ipo):
			raise TypeError("ipo can only be piped to other ipo")
		return ipo(lambda data: data | self | other)


	def __repr__(self):
		return "ipo({0!r})".format(self.function)


# =================================================================================
# STANDARD LIBRARY

# ----------------------------------------------------
# I/O

# This must not be decorated with @ipo because it has to generate data.
def read(file):
	return (line.rstrip("\n") for line in file)

stdin = read(sys.stdin)


@ipo
def write(str_or_iter, **kwargs):
	"""
	Write to file. If the data is iterable, each item is printed on its own line.

	Exception: strings and bytes are not iterated but printed as-is.
	"""
	if isinstance(str_or_iter, (_str, bytes)):
		print(str_or_iter, **kwargs)
		return

	try:
		it = iter(str_or_iter)
	except TypeError:
		print(str_or_iter, **kwargs)
		return

	for x in it:
		print(x, **kwargs)


# ----------------------------------------------------
# CSV

from_csv = ipo(csv.reader)


@ipo
def to_csv(data, separator=",", quotechar='"', escapechar=None, quoteall=False):
	# We have our own CSV writer because csv.writer insists upon writing to a file

	if escapechar is None:
		escapechar = quotechar

	def serialize(item):
		if item is None:
			return ""

		item_s = _str(item)

		# If item should not be quoted
		if not quoteall and quotechar not in item_s and "\n" not in item_s:
			return item_s

		if quotechar != escapechar:
			item_s = item_s.replace(escapechar, escapechar + escapechar)
		item_s = item_s.replace(quotechar, escapechar + quotechar)
		return quotechar + item_s + quotechar

	return (
		separator.join(serialize(item) for item in line)
		for line in data
	)


# ----------------------------------------------------
# Iterable stuff

@ipo
def map(data, function, **kwargs):
	if isinstance(function, ipo):
		return _map(function.__ror__, data, **kwargs)
	else:
		return _map(function, data, **kwargs)


@ipo
def starmap(data, function, **kwargs):
	if isinstance(function, ipo):
		return itertools.starmap(function.__ror__, data, **kwargs)
	else:
		return itertools.starmap(function, data, **kwargs)


@ipo
def filter(data, function, **kwargs):
	if isinstance(function, ipo):
		return _filter(function.__ror__, data, **kwargs)
	else:
		return _filter(function, data, **kwargs)


sort = ipo(sorted)

str = ipo(_str)

list = ipo(_list)

# dict.items() returns dict_items which overrides __or__, so we need to convert to another iterable
items = ipo(lambda d: _tuple(d.items()))


islice = ipo(itertools.islice)

# Some aliases for common usages of slicing makes things more understandable
@ipo
def take(data, n):
	return itertools.islice(data, n)
@ipo
def skip(data, n):
	return itertools.islice(data, n, None)


@ipo
def before(data, data_to_prepend):
	return itertools.chain(data_to_prepend, data)


@ipo
def after(data, data_to_append):
	return itertools.chain(data, data_to_append)
