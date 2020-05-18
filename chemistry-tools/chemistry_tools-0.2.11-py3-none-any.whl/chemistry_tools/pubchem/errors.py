#  !/usr/bin/env python
#
#  errors.py
"""Error handling functions"""
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import functools
import json
import warnings


class PubChemPyError(Exception):
	"""
	Base class for all PubChemPy exceptions.
	"""
	pass


class ResponseParseError(PubChemPyError):
	"""
	PubChem response is uninterpretable.
	"""
	pass


class PubChemHTTPError(PubChemPyError):
	"""
	Generic error class to handle all HTTP error codes.
	"""

	def __init__(self, e):
		self.code = e.status_code
		self.msg = e.reason
		try:
			self.msg += ': %s' % json.loads(e.content.decode())['Fault']['Details'][0]
		except (ValueError, IndexError, KeyError):
			pass
		if self.code == 400:
			raise BadRequestError(self.msg)
		elif self.code == 404:
			raise NotFoundError(self.msg)
		elif self.code == 405:
			raise MethodNotAllowedError(self.msg)
		elif self.code == 504:
			raise TimeoutError(self.msg)
		elif self.code == 501:
			raise UnimplementedError(self.msg)
		elif self.code == 500:
			raise ServerError(self.msg)

	def __str__(self):
		return repr(self.msg)


class BadRequestError(PubChemHTTPError):
	"""
	Request is improperly formed (syntax error in the URL, POST body, etc.).
	"""

	def __init__(self, msg='Request is improperly formed'):
		self.msg = msg


class NotFoundError(PubChemHTTPError):
	"""
	The input record was not found (e.g. invalid CID).
	"""

	def __init__(self, msg='The input record was not found'):
		self.msg = msg


class MethodNotAllowedError(PubChemHTTPError):
	"""
	Request not allowed (such as invalid MIME type in the HTTP Accept header).
	"""

	def __init__(self, msg='Request not allowed'):
		self.msg = msg


class TimeoutError(PubChemHTTPError):
	"""
	The request timed out, from server overload or too broad a request.

	See :ref:`Avoiding TimeoutError <avoiding_timeouterror>` for more information.
	"""

	def __init__(self, msg='The request timed out'):
		self.msg = msg


class UnimplementedError(PubChemHTTPError):
	"""The requested operation has not (yet) been implemented by the server."""

	def __init__(self, msg='The requested operation has not been implemented'):
		self.msg = msg


class ServerError(PubChemHTTPError):
	"""Some problem on the server side (such as a database server down, etc.)."""

	def __init__(self, msg='Some problem on the server side'):
		self.msg = msg


def deprecated(message=None):
	"""Decorator to mark functions as deprecated. A warning will be emitted when the function is used."""

	def deco(func):
		@functools.wraps(func)
		def wrapped(*args, **kwargs):
			warnings.warn(
					message or 'Call to deprecated function {}'.format(func.__name__),
					category=PubChemPyDeprecationWarning,
					stacklevel=2
					)
			return func(*args, **kwargs)

		return wrapped

	return deco


class PubChemPyDeprecationWarning(Warning):
	"""Warning category for deprecated features."""
	pass
