# -*- coding: utf-8 -*-
"""
test_requests
~~~~~~~~~~~~~

Test basic requests.

"""


from chemistry_tools.pubchem.pug_rest import _do_rest_get


def test_requests():
	"""
	Test a variety of basic raw requests and ensure they don't return an error code.
	"""

	assert _do_rest_get(identifier='c1ccccc1', namespace='smiles').status_code == 200
	assert _do_rest_get(identifier='coumarin', namespace='name', format_='PNG', png_width=50, png_height=50).status_code == 200


def test_content_type():
	"""
	Test content type header matches desired output format.
	"""

	assert _do_rest_get(identifier=241, namespace="cid", format_='JSON').headers['Content-Type'] == 'application/json'
	assert _do_rest_get(identifier=241, namespace="cid", format_='XML').headers['Content-Type'] == 'application/xml'
	# assert _do_rest_get(identifier=241, namespace="cid", format_='SDF').headers['Content-Type'] == 'chemical/x-mdl-sdfile'
	# assert _do_rest_get(identifier=241, namespace="cid", format_='ASNT').headers['Content-Type'] == 'text/plain'
	assert _do_rest_get(identifier=241, namespace="cid", format_='PNG').headers['Content-Type'] == 'image/png'

