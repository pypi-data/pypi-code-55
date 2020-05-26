#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pug_rest.py
"""
Functions for interacting with PubChem PUG_REST API
"""
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on PubChemPy https://github.com/mcs07/PubChemPy/blob/master/LICENSE
#  |  Copyright 2014 Matt Swain <m.swain@me.com>
#  |  Licensed under the MIT License
#  |
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
import time
from urllib.parse import quote

# this package
from chemistry_tools import cached_requests
from chemistry_tools.pubchem import API_BASE
from chemistry_tools.pubchem.enums import PubChemFormats, PubChemNamespace
from chemistry_tools.pubchem.errors import HTTP_ERROR_CODES, PubChemHTTPError
from chemistry_tools.pubchem.utils import _force_sequence_or_csv, _make_base_url


def _do_rest_get(
		namespace, identifier, format_=PubChemFormats.JSON, domain=None,
		record_type="2d",
		png_width=300, png_height=300):
	"""
	:param identifier: Identifiers (e.g. name, CID) for the compounds to look up.
		When using the CID namespace data for multiple compounds can be retrieved at once by
		supplying either a comma-separated string or a list.
	:type identifier: str, Sequence[str]
	:param namespace: The type of identifier to look up. Valid values are in :class:`PubChemNamespace`. Default "name"
	:type namespace: PubChemNamespace, optional
	:type namespace: str, optional
	:param format_: The file format to retrieve the data in. Valid values are in :class:`PubChemFormats`, plus "PNG"
	:type format_: PubChemFormats or str, optional

	:return:
	:rtype:
	"""

	# domain = description, synonyms, or property followed by a comma-separated list of desired properties

	if not PubChemNamespace.is_valid_value(namespace):
		raise ValueError(f"'{namespace}' is not a valid value for 'namespace'")

	if not PubChemFormats.is_valid_value(format_):
		raise ValueError(f"'{format_}' is not a valid value for 'format_'")

	query_params = {}

	if str(format_).upper() == str(PubChemFormats.PNG):
		query_params["image_size"] = f"{png_width}x{png_height}"

	if domain:
		r = cached_requests.get(f"{_make_base_url(namespace, identifier)}/{domain}/{format_}", params=query_params)
	else:
		query_params["record_type"] = record_type
		r = cached_requests.get(f"{_make_base_url(namespace, identifier)}/{format_}", params=query_params)

	if r.status_code in HTTP_ERROR_CODES:
		raise PubChemHTTPError(r)

	return r


def get_full_json(cid):
	json_file = cached_requests.get(f"{API_BASE}_view/data/compound/{cid}/JSON/")
	return json_file.json()


def async_get(identifier, namespace='cid', operation=None, output='JSON', searchtype=None, **kwargs):
	"""
	Request wrapper that automatically handles async requests.
	"""
	# TODO:

	if (searchtype and searchtype != 'xref') or namespace in ['formula']:
		r = request(identifier, namespace, None, 'JSON', searchtype, **kwargs)
		response = r.content
		status = r.json()
		if 'Waiting' in status and 'ListKey' in status['Waiting']:
			identifier = status['Waiting']['ListKey']
			namespace = 'listkey'
			while 'Waiting' in status and 'ListKey' in status['Waiting']:
				time.sleep(2)
				r = request(identifier, namespace, operation, 'JSON', **kwargs)
				response = r.content
				status = r.json()
			if output != 'JSON':
				response = request(identifier, namespace, operation, output, searchtype, **kwargs).content
	else:
		response = request(identifier, namespace, operation, output, searchtype, **kwargs).content

	return response


def request(identifier, namespace='cid', operation=None, output='JSON', searchtype=None, **kwargs):
	"""
	Construct API request from parameters and return the response.

	Full specification at http://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
	"""

	# If identifier is a list, join with commas into string
	if isinstance(identifier, int):
		identifier = str(identifier)

	identifier = _force_sequence_or_csv(identifier, "identifier")
	identifier = ','.join(str(x) for x in identifier)

	# Build API URL
	urlid, params = None, {}

	# use this function when:
		# namespace in ['listkey', 'formula']
		# searchtype == 'xref'

	urlid = quote(identifier.encode('utf8'))

	comps = filter(None, [API_BASE, "compound", searchtype, namespace, urlid, operation, output])
	apiurl = '/'.join(comps)

	# Filter None values from kwargs
	for key, val in kwargs.items():
		if val is not None:
			params[key] = val

	# print(f'Request URL: {apiurl}')
	# print(f'Request data: {params}')

	response = cached_requests.get(apiurl, params=params)
	if response.status_code in HTTP_ERROR_CODES:
		raise PubChemHTTPError(response)

	return response
