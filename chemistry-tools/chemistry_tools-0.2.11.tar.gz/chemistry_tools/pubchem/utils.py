#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  utils.py
"""
Various tools
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
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


# stdlib
import functools
import json
import os
import time
from decimal import Decimal, DecimalException
# from urllib.request import urlopen
# from urllib.error import HTTPError
from urllib.parse import quote, urlencode

# 3rd party
import requests
# from requests.exceptions import HTTPError

# this package
from chemistry_tools.constants import API_BASE, log, PROPERTY_MAP, text_types
from .errors import NotFoundError, PubChemHTTPError


def get_full_json(cid):
	json_file = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/")
	return json_file.json()


def get_json(identifier, namespace='cid', domain='compound', operation=None, searchtype=None, **kwargs):
	"""
	Request wrapper that automatically parses JSON response and suppresses NotFoundError.
	"""

	try:
		return json.loads(get(identifier, namespace, domain, operation, 'JSON', searchtype, **kwargs).decode())
	except NotFoundError as e:
		log.info(e)
		return None


def get(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
	"""
	Request wrapper that automatically handles async requests.
	"""

	if (searchtype and searchtype != 'xref') or namespace in ['formula']:
		# response = request(identifier, namespace, domain, None, 'JSON', searchtype, **kwargs).read()
		response = request(identifier, namespace, domain, None, 'JSON', searchtype, **kwargs).content
		status = json.loads(response.decode())
		if 'Waiting' in status and 'ListKey' in status['Waiting']:
			identifier = status['Waiting']['ListKey']
			namespace = 'listkey'
			while 'Waiting' in status and 'ListKey' in status['Waiting']:
				time.sleep(2)
				# response = request(identifier, namespace, domain, operation, 'JSON', **kwargs).read()
				response = request(identifier, namespace, domain, operation, 'JSON', **kwargs).content
				status = json.loads(response.decode())
			if not output == 'JSON':
				# response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).read()
				response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).content
	else:
		# response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).read()
		response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).content
	return response


def request(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
	"""
	Construct API request from parameters and return the response.

	Full specification at http://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
	"""

	if not identifier:
		raise ValueError('identifier/cid cannot be None')
	# If identifier is a list, join with commas into string
	if isinstance(identifier, int):
		identifier = str(identifier)
	if not isinstance(identifier, text_types):
		identifier = ','.join(str(x) for x in identifier)
	# Filter None values from kwargs
	kwargs = {k: v for k, v in kwargs.items() if v is not None}
	# Build API URL
	urlid, postdata = None, None
	if namespace == 'sourceid':
		identifier = identifier.replace('/', '.')
	if namespace in ['listkey', 'formula', 'sourceid'] \
			or searchtype == 'xref' \
			or (searchtype and namespace == 'cid') or domain == 'sources':
		urlid = quote(identifier.encode('utf8'))
	else:
		postdata = urlencode([(namespace, identifier)]).encode('utf8')
	comps = filter(None, [API_BASE, domain, searchtype, namespace, urlid, operation, output])
	apiurl = '/'.join(comps)
	if kwargs:
		apiurl += '?%s' % urlencode(kwargs)
	# Make request
	# try:
	log.debug('Request URL: %s', apiurl)
	log.debug('Request data: %s', postdata)
	# response = urlopen(apiurl, postdata)
	response = requests.get(apiurl, postdata)
	if response.status_code in ERROR_CODES:
		raise PubChemHTTPError(response)
		# print(f"#{response}")
	return response
	# except HTTPError as e:
	# 	raise PubChemHTTPError(e)


ERROR_CODES = [400, 404, 405, 504, 501, 500]


def get_sdf(identifier, namespace='cid', domain='compound', operation=None, searchtype=None, **kwargs):
	"""
	Request wrapper that automatically parses SDF response and suppresses NotFoundError.
	"""

	try:
		return get(identifier, namespace, domain, operation, 'SDF', searchtype, **kwargs).decode()
	except NotFoundError as e:
		log.info(e)
		return None


def get_properties(properties, identifier, namespace='cid', searchtype=None, as_dataframe=False, **kwargs):
	"""
	Retrieve the specified properties from PubChem.

	:param identifier: The compound, substance or assay identifier to use as a search query.
	:param namespace: (optional) The identifier type.
	:param searchtype: (optional) The advanced search type, one of substructure, superstructure or similarity.
	:param as_dataframe: (optional) Automatically extract the properties into a pandas :class:`~pandas.DataFrame`.
	"""

	if isinstance(properties, text_types):
		properties = properties.split(',')
	properties = ','.join([PROPERTY_MAP.get(p, p) for p in properties])
	properties = 'property/%s' % properties
	results = get_json(identifier, namespace, 'compound', properties, searchtype=searchtype, **kwargs)
	results = results['PropertyTable']['Properties'] if results else []
	if as_dataframe:
		import pandas as pd
		return pd.DataFrame.from_records(results, index='CID')
	return results


def get_synonyms(identifier, namespace='cid', domain='compound', searchtype=None, **kwargs):
	results = get_json(identifier, namespace, domain, 'synonyms', searchtype=searchtype, **kwargs)
	return results['InformationList']['Information'] if results else []


def get_cids(identifier, namespace='name', domain='compound', searchtype=None, **kwargs):
	results = get_json(identifier, namespace, domain, 'cids', searchtype=searchtype, **kwargs)
	if not results:
		return []
	elif 'IdentifierList' in results:
		return results['IdentifierList']['CID']
	elif 'InformationList' in results:
		return results['InformationList']['Information']


def get_sids(identifier, namespace='cid', domain='compound', searchtype=None, **kwargs):
	results = get_json(identifier, namespace, domain, 'sids', searchtype=searchtype, **kwargs)
	if not results:
		return []
	elif 'IdentifierList' in results:
		return results['IdentifierList']['SID']
	elif 'InformationList' in results:
		return results['InformationList']['Information']


def get_aids(identifier, namespace='cid', domain='compound', searchtype=None, **kwargs):
	results = get_json(identifier, namespace, domain, 'aids', searchtype=searchtype, **kwargs)
	if not results:
		return []
	elif 'IdentifierList' in results:
		return results['IdentifierList']['AID']
	elif 'InformationList' in results:
		return results['InformationList']['Information']


def get_all_sources(domain='substance'):
	"""
	Return a list of all current depositors of substances or assays.
	"""

	results = json.loads(get(domain, None, 'sources').decode())
	return results['InformationList']['SourceName']


def download(
		outformat, path, identifier, namespace='cid', domain='compound',
		operation=None, searchtype=None, overwrite=False, **kwargs):
	"""
	Format can be  XML, ASNT/B, JSON, SDF, CSV, PNG, TXT.
	"""

	response = get(identifier, namespace, domain, operation, outformat, searchtype, **kwargs)
	if not overwrite and os.path.isfile(path):
		raise OSError("%s already exists. Use 'overwrite=True' to overwrite it." % path)
	with open(path, 'wb') as f:
		f.write(response)


def memoized_property(fget):
	"""
	Decorator to create memoized properties.

	Used to cache :class:`~pubchempy.Compound` and :class:`~pubchempy.Substance` properties that require an additional
	request.
	"""

	attr_name = '_{}'.format(fget.__name__)

	@functools.wraps(fget)
	def fget_memoized(self):
		if not hasattr(self, attr_name):
			setattr(self, attr_name, fget(self))
		return getattr(self, attr_name)

	return property(fget_memoized)


def _parse_prop(search, proplist):
	"""
	Extract property value from record using the given urn search filter.
	"""

	props = [i for i in proplist if all(item in i['urn'].items() for item in search.items())]
	if len(props) > 0:
		if search != {'implementation': 'E_SCREEN'}:  # True for "fingerprint", which isn't a number
			try:
				return Decimal(str(props[0]['value'][list(props[0]['value'].keys())[0]]))
			except DecimalException:
				return props[0]['value'][list(props[0]['value'].keys())[0]]
		else:
			return props[0]['value'][list(props[0]['value'].keys())[0]]


def format_string(stringwithmarkup):
	"""
	Convert a PubChem formatted string into an HTML formatted string
	"""

	string = list(stringwithmarkup["String"])
	try:
		markup_list = stringwithmarkup["Markup"]
	except KeyError:
		markup_list = []

	for markup in markup_list:
		style = None
		start = markup["Start"]
		end = markup["Length"] + start - 1
		if markup["Type"] == "Italics":
			style = "i"
		# handle Other formats

		if style is None:
			print(markup)
			continue

		string[start] = f"<{style}>{string[start]}"
		string[end] = f"{string[end]}</{style}>"

	string = ''.join(string)

	return string
