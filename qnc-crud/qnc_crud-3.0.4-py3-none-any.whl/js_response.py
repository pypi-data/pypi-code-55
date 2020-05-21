'''
    DEPRECATED (I think).
    See RELEASE_NOTES for version 3.0.4
'''
import warnings
warnings.warn('js_response.py is deprecated. We recommend using django_jsform instead.')

import json
from django import http

from .templatetags.qnc_crud import get_errormessage_id

import logging

def d(text):
	return json.dumps(text)

def js_response(content):
	return http.HttpResponse(content, content_type='text/javascript')

# Helper for combining the instructions of multiple responses
# see reset_form for sample
def multi_response(*responses):
	return js_response(';'.join([r.content.decode(r.charset) for r in responses]))

def reload():
	'''
		Useful if you have an in-page edit form.
		Return true to prevent further submissions while navigating.
	'''
	return js_response('location.reload(); return true')
'''
	TODO - we MAY want to check if SmartBackButton.can_go_back() (or can_go_back_to_same_domain()), and if not, then go to a fallback url. That requires users to be using smart_back_button.js
	Maybe that should be a different function?
'''
def go_back():
	'''
		This is our recommend response for "Edit" form pages.
		Use in conjunction with qnc_crud/reload_if_necessary.html, so that the previous page will immediately reload.
		Return true to prevent further submissions while navigating.
	'''
	return js_response('history.back(); return true')
def close_window(fallback_url='/'):
	'''
		Useful if form page is opened in new widow (ie. for a complex multi-step form).
		We don't recommend this, though. Try to open form in same window, and use go_back() when done.
		Return true to prevent further submissions while navigating.
	'''
	return js_response(f'window.close();location={d(fallback_url)};return true')
def go_to(url):
	'''
		Useful if you have an in-page "Add" form on a list page, and want to navigate to detail page for the created object upon form completion.
		Return true to prevent further submissions while navigating.
	'''
	return js_response(f'location = {d(url)}; return true')
def replace_location(url):
	'''
		Useful for "Add" form pages, where you want to view the created object after form completion, but want to remove the form page from history.

		For most purposes, location.replace(url) would be enough.
		The history.replaceState bit changes what the document.referrer will be on the next page, which is needed for qnc_crud/smart_back_btton.js to work properly.

		TODO - we should either:
			resolve url relative to current page, as is done in qnc_crud/utils.js in [qnc-replace-location] handler
			only accept absolute/site-relative urls
	'''
	return js_response(f'''
		try {{
			history.replaceState(null, '', document.referrer);
		}}
		catch (e) {{}}
		// replaceState is asynchronous - if we do location.replace immediately, next page won't have the modified referrer
		setTimeout(function() {{
			location.replace({d(url)});
		}}, 0);

		// prevent further form submissions
		return true
	''')


def alert(message):
	'''
		Useful for error messages that aren't really typical form error messages, or for actions that are triggered by a simple button push (where there is no corresponding container for error messages).
	'''
	return js_response(f'alert({d(message)})')

'''
	TODO - test and document
	This would be particularly useful when generating forms via react/mithril/etc, and when the response to form submission involves complex state updates (ie. not a simple navigation)
	Users can just bind event listeners to the forms to process the server response -> no need to setup api
'''
def fire_custom_event(data=None, name="ajax_sumbssion_handled"):
	return js_response(f'''
		form.dispatchEvent(new CustomEvent('{name}', {{
			detail: {json.dumps(data)},
			bubbles: true,
		}}));
	''');

# Note - you'll likely want to call render_to_string to generate the html for these:
def replace_element_contents(id, html):
	return js_response(f'document.getElementById({d(id)}).innerHTML = {d(html)}')
def append_to_element(id, html):
	return js_response(f'document.getElementById({d(id)}).innerHTML += {d(html)}')
# Note - we do NOT recommend using this for error messages. Use only when the form was successful, and you're replacing it with another form (ie. another step in a multi-step form).
def replace_form_contents(html):
	return js_response(f'form.innerHTML = {d(html)}')

def reset_form_inputs():
	return js_response(f'form.reset()')

def clear_form_errors():
	return js_response('clear_form_errors(form)')

def set_form_errors(form):
	return set_raw_form_errors(form.non_field_errors(), {get_errormessage_id(field): field.errors for field in form})
def set_raw_form_errors(form_errors, error_map):
	# Notice - this relies on set_form_errors(errors) being defined in global scope
	# We define this in set_form_errors.js
	return js_response(f'set_form_errors(form, {d(form_errors)}, {d(error_map)})');
def reset_form():
	return multi_response(
		clear_form_errors(),
		reset_form_inputs(),
	)