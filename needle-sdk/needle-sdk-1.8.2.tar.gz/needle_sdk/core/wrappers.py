from .classes import RequestData
import threading
import time

wrappers = None
needle_data = threading.local()

# Initialise wrappers
def init_wrapper_store():
    global wrappers

    wrappers = []

    try:
        lang_module = 'django.core.handlers.base.BaseHandler.get_response'
        from django.core.handlers.base import BaseHandler
        add_wrapper_record(lang_module, BaseHandler.get_response, needle_django_get_response)
    except ImportError:
        pass

    try:
        lang_module = 'django.template.loader.render_to_string'
        import django.template.loader
        add_wrapper_record(lang_module, django.template.loader.render_to_string, needle_django_template_render)
    except ImportError:
        pass

    try:
        lang_module = 'flask.signals.request_started'
        add_wrapper_record(lang_module, None, needle_flask_request_started)
    except ImportError:
        pass

    try:
        lang_module = 'flask.signals.request_finished'
        add_wrapper_record(lang_module, None, needle_flask_request_finished)
    except ImportError:
        pass

    try:
        lang_module = 'flask.render_template'
        import flask
        add_wrapper_record(lang_module, flask.render_template, needle_flask_render_template)
    except ImportError:
        pass

    try:
        lang_module = 'mysql.connector.connect'
        import mysql.connector
        add_wrapper_record(lang_module, mysql.connector.connect, needle_mysql_connect)
    except ImportError:
        pass

    try:
        lang_module = 'psycopg2.connect'
        import psycopg2
        add_wrapper_record(lang_module, psycopg2.connect, needle_psycopg2_connect)
    except ImportError:
        pass

    try:
        lang_module = 'os.system'
        import os
        add_wrapper_record(lang_module, os.system, needle_os_system)
    except ImportError:
        pass

    try:
        lang_module = 'os.popen'
        import os
        add_wrapper_record(lang_module, os.popen, needle_os_popen)
    except ImportError:
        pass

    try:
        lang_module = 'builtins.open'
        import builtins
        add_wrapper_record(lang_module, builtins.open, needle_builtins_open)
    except ImportError:
        pass

    try:
        lang_module = 'requests.get'
        import requests
        add_wrapper_record(lang_module, requests.get, needle_requests_get)
    except ImportError:
        pass

    try:
        lang_module = 'urllib.request.urlopen'
        import urllib.request
        add_wrapper_record(lang_module, urllib.request.urlopen, needle_urllib_request_urlopen)
    except ImportError:
        pass


# Add wrapper record
def add_wrapper_record(lang_module, orig, wrapper):
    global wrappers
    wrappers.append({'lang_module': lang_module, 'orig': orig, 'wrapper': wrapper})


# Get wrapper
def get_wrapper(lang_module):
    global wrappers
    wrapper = None

    for w in wrappers:
        if w['lang_module'] == lang_module:
            wrapper = w['wrapper']
            break

    return wrapper


# Get original
def get_orig(lang_module):
    global wrappers
    orig = None

    for w in wrappers:
        if w['lang_module'] == lang_module:
            orig = w['orig']
            break

    return orig


# Set wrapper
def set_wrapper(lang_module, set_flag):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        if set_flag:
            func = get_wrapper(lang_module)
        else:
            func = get_orig(lang_module)

        if lang_module == 'django.core.handlers.base.BaseHandler.get_response':
            try:
                from django.core.handlers.base import BaseHandler
                BaseHandler.get_response = func
            except ImportError:
                pass

        if lang_module == 'django.template.loader.render_to_string':
            try:
                import django.template.loader
                django.template.loader.render_to_string = func
            except ImportError:
                pass

        if lang_module == 'flask.render_template':
            try:
                import flask
                flask.render_template = func
            except ImportError:
                pass

        if lang_module == 'mysql.connector.connect':
            try:
                import mysql.connector
                mysql.connector.connect = func
            except ImportError:
                pass

        if lang_module == 'psycopg2.connect':
            try:
                import psycopg2
                psycopg2.connect = func
            except ImportError:
                pass

        if lang_module == 'os.system':
            try:
                import os
                os.system = func
            except ImportError:
                pass

        if lang_module == 'os.popen':
            try:
                import os
                os.popen = func
            except ImportError:
                pass

        if lang_module == 'builtins.open':
            try:
                import builtins
                builtins.open = func
            except ImportError:
                pass

        if lang_module == 'requests.get':
            try:
                import requests
                requests.get = func
            except ImportError:
                pass

        if lang_module == 'urllib.request.urlopen':
            try:
                import urllib.request
                urllib.request.urlopen = func
            except ImportError:
                pass
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error setting wrapper', error_data)


# Wrapper
def needle_django_get_response(*args, **kwargs):
    lang_module = 'django.core.handlers.base.BaseHandler.get_response'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:' + lang_module, error_data)

    if needle_app.debug_mode: print('Needle.sh: Inside Django get_response')

    try:
        needle_app.total_requests += 1

        try:
            request_data = RequestData()
            request_data.req_start_ts = ts_fn_start

            values = []
            for key, value in args[1].GET.items():
                values.append({'type': 'get', 'name': key, 'value': value})

            for key, value in args[1].POST.items():
                values.append({'type': 'post', 'name': key, 'value': value})

            path_args = args[1].path.split('/')
            for p in path_args:
                if p == '': continue
                values.append({'type': 'path', 'name': 'path', 'value': p})

            request_data.data = values

            if 'REMOTE_ADDR' in args[1].META: request_data.remote_addr = args[1].META['REMOTE_ADDR']
            if 'REQUEST_METHOD' in args[1].META: request_data.request_method = args[1].META['REQUEST_METHOD']
            if 'HTTP_HOST' in args[1].META: request_data.http_host = args[1].META['HTTP_HOST']
            if 'PATH_INFO' in args[1].META: request_data.path_info = args[1].META['PATH_INFO']
            if 'HTTP_USER_AGENT' in args[1].META: request_data.http_user_agent = args[1].META['HTTP_USER_AGENT']

            needle_data.req_data = request_data
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error adding request data to thread storage:', error_data)

        # Check for security scanner
        block_request = False
        try:
            sec_module = 'scan'
            scan_check, action = needle_app.module_active(sec_module)
            if scan_check:
                needle_app.inc_mod_requests(sec_module, lang_module)
                match, arg_type, arg_name, arg_value = check_sec_scanner()
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: Security scanner')

                    if action == 'block': block_request = True

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = action
                    needle_data.req_data.incident_module = sec_module

                    # Add mal request
                    needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)

        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error checking security scanner:', error_data)

        if block_request:
            return ''

        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, '_basic', lang_module, fn_time)

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding request data to thread storage', error_data)

    # Call original method
    response = get_orig(lang_module)(*args, **kwargs)

    try:
        # Insert security related HTTP headers
        sec_headers = needle_app.get_sec_headers()
        for i, (key, value) in enumerate(sec_headers.items()):
            response[key] = value

        if len(sec_headers) > 0: needle_app.inc_mod_requests('add_headers', lang_module)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding security headers:'+lang_module, error_data)

    try:
        req_time = int(time.time() * 1000) - needle_data.req_data.req_start_ts
        needle_app.add_perf_time(needle_data.req_data, '_req', lang_module, req_time)

        needle_app.add_perf_record(needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return response


# Save Request Get/Post params
def needle_flask_request_started(*args, **kwargs):
    lang_module = 'flask.signals.request_started'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:' + lang_module, error_data)

    try:
        needle_app.total_requests += 1

        from flask import request

        request_data = RequestData()
        request_data.req_start_ts = ts_fn_start

        values = []
        get_params = request.args
        for key, value in get_params.items():
            values.append({'type': 'get', 'name': key, 'value': value})

        post_params = request.form
        for key, value in post_params.items():
            values.append({'type': 'post', 'name': key, 'value': value})

        path_args = request.path.split('/')
        for p in path_args:
            if p == '': continue
            values.append({'type': 'path', 'name': 'path', 'value': p})

        request_data.data = values

        request_data.remote_addr = request.remote_addr
        request_data.request_method = request.method
        request_data.http_host = request.host
        request_data.path_info = request.path
        request_data.http_user_agent = request.user_agent.string

        needle_data.req_data = request_data
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while adding request data to thread storage', error_data)

    block_request = False
    try:
        block_request = needle_scan_module(lang_module)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error while checking sec scanner', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, '_basic', lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)


def needle_flask_request_finished(*args, **kwargs):
    lang_module = 'flask.signals.request_finished'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:' + lang_module, error_data)

    response = kwargs['response']

    try:
        # Insert security related HTTP headers
        sec_headers = needle_app.get_sec_headers()
        for i, (key, value) in enumerate(sec_headers.items()):
            response.headers[key] = value

        if len(sec_headers) > 0: needle_app.inc_mod_requests('add_headers', lang_module)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, '_basic', lang_module, fn_time)

        req_time = int(time.time() * 1000) - needle_data.req_data.req_start_ts
        needle_app.add_perf_time(needle_data.req_data, '_req', lang_module, req_time)

        needle_app.add_perf_record(needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)


# Check for security scanner
def needle_scan_module(py_module):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    sec_module = 'scan'
    block_request = False

    try:
        scan_check, action = needle_app.module_active(sec_module)
        if scan_check:
            needle_app.inc_mod_requests(sec_module, py_module)
            match, arg_type, arg_name, arg_value = check_sec_scanner()
            if match:

                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Security scanner')

                if action == 'block': block_request = True

                # Save request action to thread-data
                needle_data.req_data.incident_action = action
                needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking security scanner', error_data)

    return block_request


# Check for XSS attack
def check_content_xss(content):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']
            if value == '': continue

            if libinjec:
                resp = libinjec.xss(value)
                if resp == 1:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value

            # If XSS not detected using libinjec module, use regex
            if needle_app.debug_mode: print('Checking XSS using regex...')
            xss_pattern = needle_app.get_xss_pattern()

            if xss_pattern:
                if len(xss_pattern.findall(value)) > 0:
                    # Check if content contains arg value
                    if content.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        return match, arg_type, arg_name, arg_value
            else:
                needle_app.add_error('Error checking XSS:', 'XSS pattern unavailable')
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking XSS:', error_data)

    return match, arg_type, arg_name, arg_value


def needle_django_template_render(*args, **kwargs):
    sec_module = 'xss'
    lang_module = 'django.template.loader.render_to_string'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    try:
        req_data = needle_data.req_data.data
    except Exception as e:
        error_data = str(e)
        msg = 'Error checking XSS in module: ' + lang_module
        needle_app.add_error(msg, error_data)
        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:'+lang_module, error_data)

    content = ''
    try:
        # Add module used
        needle_app.add_module(sec_module, 'django.template.loader', 'render_to_string')

        # Get HTML content
        content = get_orig(lang_module)(*args, **kwargs)

        # Save request action to thread-data
        if needle_data.req_data.incident_action == 'block':
            content = needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
        else:
            # Check if XSS module is active
            xss_check, action = needle_app.module_active(sec_module)
            if xss_check:
                needle_app.inc_mod_requests(sec_module, lang_module)
                if needle_app.debug_mode: print('Needle.sh: Checking XSS')

                match, arg_type, arg_name, arg_value = check_content_xss(content)
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: XSS')

                    if action == 'block':
                        # Show blocked message
                        content = needle_app.get_blocked_page_content('xss')

                    # Add mal request
                    needle_app.add_mal_request(action, 'xss', arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking reflected XSS:', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return content


# Monkey patch: Render template function
def needle_flask_render_template(*args, **kwargs):
    sec_module = 'xss'
    lang_module = 'flask.render_template'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:'+lang_module, error_data)

    try:
        needle_app.add_module(sec_module, 'flask', lang_module)
    except Exception as e:
        pass

    content = ''
    try:
        # Get HTML content
        content = get_orig(lang_module)(*args, **kwargs)

        # Save request action to thread-data
        if needle_data.req_data.incident_action == 'block':
            content = needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
        else:
            # Check if XSS module is active
            xss_check, action = needle_app.module_active(sec_module)
            if xss_check:
                needle_app.inc_mod_requests(sec_module, lang_module)
                if needle_app.debug_mode: print('Checking XSS...')

                match, arg_type, arg_name, arg_value = check_content_xss(content)
                if match:
                    if needle_app.debug_mode: print('Needle.sh: New Incident of type: XSS')

                    if action == 'block':
                        # Show blocked message
                        content = needle_app.get_blocked_page_content('xss')

                    # Add mal request
                    needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking reflected XSS', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return content


# Check command injection
def check_command_injection(command):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        cmdi_pattern = needle_app.get_cmdi_pattern()

        if cmdi_pattern:
            for obj in needle_data.req_data.data:
                value = obj['value']
                if value == '': continue

                remove_chars = ['\'', '"', '\\', '$@', '`', '$(', ')']  # Remove characters that will be ignored by command shell
                for c in remove_chars:
                    value = value.replace(c, '')
                    command = command.replace(c, '')

                if value == '': continue

                if len(cmdi_pattern.findall(value)) > 0:
                    # Check if command contains arg value
                    if command.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']
                        return match, arg_type, arg_name, arg_value
        else:
            needle_app.add_error('Error checking command injection:', 'Unavailable cmdi pattern')

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    return match, arg_type, arg_name, arg_value


# Check command injection
def needle_cmdi_check(lang_module, *args, **kwargs):
    sec_module = 'cmdi'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    try:
        req_data = needle_data.req_data.data
    except Exception as e:
        error_data = str(e)
        msg = 'Error checking CMDI in module: ' + lang_module

        try:
            if needle_app.adv_debug: msg += '  / command: ' + args[0]
        except Exception as e:
            pass

        needle_app.add_error(msg, error_data)

        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:' + lang_module, error_data)

    try:
        # Add module used
        needle_app.add_module(sec_module, '', lang_module)
    except Exception as e:
        pass

    try:
        cmdi_check, action = needle_app.module_active(sec_module)

        if cmdi_check:
            needle_app.inc_mod_requests(sec_module, lang_module)
            match, arg_type, arg_name, arg_value = check_command_injection(args[0])

            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Command injection')

                if action == 'block':
                    # Replace with blank command
                    args = ('',)

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = 'block'
                    needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    # Call original function
    return get_orig(lang_module)(*args, **kwargs)


# Instrumented method for os.system
def needle_os_system(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()
    try:
        py_module = 'os.system'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Instrumented method for os.popen
def needle_os_popen(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()
    try:
        py_module = 'os.popen'
        return needle_cmdi_check(py_module, *args, **kwargs)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking command injection', error_data)


# Check LFI
def check_lfi(filepath):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        for obj in needle_data.req_data.data:
            value = obj['value']
            if value == '': continue

            if filepath == value and (filepath[0] == '/' or filepath.find('../') > -1):
                match = True
                arg_type = obj['type']
                arg_name = obj['name']
                arg_value = obj['value']
                return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        msg = 'Error checking LFI'
        try:
            if needle_app.adv_debug: msg += ':' + filepath
        except Exception as e:
            pass

        needle_app.add_error(msg, error_data)

    return match, arg_type, arg_name, arg_value


# Check LFI
def needle_lfi_check(lang_module, *args, **kwargs):
    sec_module = 'lfi'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    try:
        req_data = needle_data.req_data.data
    except Exception as e:
        error_data = str(e)
        msg = 'Error checking LFI in module: ' + lang_module

        try:
            if needle_app.adv_debug: msg += '  / filepath: ' + args[0]
        except Exception as e:
            pass

        needle_app.add_error(msg, error_data)

        return get_orig(lang_module)(*args, **kwargs)


    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:'+lang_module, error_data)

    try:
        needle_app.add_module(sec_module, '', lang_module)
    except Exception as e:
        pass

    try:
        lfi_check, action = needle_app.module_active(sec_module)

        if lfi_check:
            needle_app.inc_mod_requests(sec_module, lang_module)
            match, arg_type, arg_name, arg_value = check_lfi(args[0])

            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Local File Inclusion')

                if action == 'block':
                    # Replace with blank
                    args = ('',)

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = 'block'
                    needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking LFI', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return get_orig(lang_module)(*args, **kwargs)


def needle_builtins_open(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    #print('Needle.sh: Inside builtins.open:', args)

    py_module = 'builtins.open'
    return needle_lfi_check(py_module, *args, **kwargs)


def check_private_ip(host_string):
    prefixes = [
        "127.", "0.",
        "10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
        "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168.", "169.254.",
        "fc", "fe", "ff", "::1", "localhost"
    ]

    # Check if host is IP address or number
    parts = host_string.split(".")
    mod_parts = []

    for p in parts:
        mod_p = p
        is_int = False

        # If hex, convert to dec
        if p.startswith('0x') or p.startswith('0X'):
            #s = p[2:len(p)]
            try:
                if hex(int(p, 16)) == p.lower():
                    is_int = True
                    mod_p = str(int(p, 16))
            except Exception as e:
                pass

        elif p.startswith('0'): #If octal, convert to dec
            s = p.lstrip('0')
            try:
                if str(int(s)) == s:
                    is_int = True
                    mod_p = str(int(s, 8))
            except Exception as e:
                pass

        try:
            if str(int(p)) == p:
                is_int = True
        except Exception as e:
            pass

        if len(parts) == 1 and is_int:
            try:
                import socket, struct
                mod_p = socket.inet_ntoa(struct.pack('!L', int(mod_p)))
            except Exception as e:
                pass

        mod_parts.append(mod_p)

    mod_host_string = '.'.join(mod_parts)
    is_private = False

    # str_ip_addr = ''
    # try:
    #     int_url_host = int(url_host)
    #     if str(int_url_host) == url_host:
    #         import socket, struct
    #         str_ip_addr = socket.inet_ntoa(struct.pack('!L', int_url_host))
    # except Exception as e:
    #     pass

    for prefix in prefixes:
        #if url_host.startswith(prefix) or str_ip_addr.startswith(prefix):
        if mod_host_string.startswith(prefix):
            is_private = True
            break

    return is_private


def check_ssrf(url_string):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    try:
        from urllib.parse import urlparse
        u = urlparse(url_string)
        url_host = u.netloc

        for obj in needle_data.req_data.data:
            value = obj['value']
            if value == '': continue

            if url_string == value and check_private_ip(url_host):
                match = True
                arg_type = obj['type']
                arg_name = obj['name']
                arg_value = obj['value']
                return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SSRF', error_data)

    return match, arg_type, arg_name, arg_value


# Check SSRF
def needle_ssrf_check(lang_module, *args, **kwargs):
    sec_module = 'ssrf'

    try:
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
    except Exception as e:
        return get_orig(lang_module)(*args, **kwargs)

    try:
        req_data = needle_data.req_data.data
    except Exception as e:
        error_data = str(e)
        msg = 'Error checking SSRF in module: ' + lang_module

        try:
            if needle_app.adv_debug: msg += '  / URL: ' + args[0]
        except Exception as e:
            pass

        needle_app.add_error(msg, error_data)

        return get_orig(lang_module)(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:'+lang_module, error_data)

    try:
        needle_app.add_module(sec_module, '', lang_module)
    except Exception as e:
        pass

    try:
        ssrf_check, action = needle_app.module_active(sec_module)

        if ssrf_check:
            needle_app.inc_mod_requests(sec_module, lang_module)
            match, arg_type, arg_name, arg_value = check_ssrf(args[0])

            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: Server Side Request Forgery (SSRF)')

                if action == 'block':
                    # Replace with blank
                    args = ('',)

                    # Save request action to thread-data
                    needle_data.req_data.incident_action = 'block'
                    needle_data.req_data.incident_module = sec_module

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SSRF', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return get_orig(lang_module)(*args, **kwargs)


def needle_requests_get(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    if needle_app.debug_mode: print('Needle.sh: Inside needle_requests_get:', args)

    py_module = 'requests.get'
    return needle_ssrf_check(py_module, *args, **kwargs)


def needle_urllib_request_urlopen(*args, **kwargs):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    if needle_app.debug_mode: print('Needle.sh: Inside needle_urllib_request_urlopen:', args)

    py_module = 'urllib.request.urlopen'
    return needle_ssrf_check(py_module, *args, **kwargs)


# Check SQL injection
def check_sql_injection(query):
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking SQL injection')

    try:
        libinjec = needle_app.get_libinjec()

        for obj in needle_data.req_data.data:
            value = obj['value']

            if value == '': continue

            if libinjec:
                resp = libinjec.sqli(value, '')
                if resp == 1:
                    # Check if SQL query contains arg value
                    if query.find(value) > -1:
                        match = True
                        arg_type = obj['type']
                        arg_name = obj['name']
                        arg_value = obj['value']

                        # Save request action to thread-data
                        needle_data.req_data.incident_action = 'block'
                        needle_data.req_data.incident_module = 'sqli'
                        needle_data.req_data.incident_rule = 'sqli_1'

                        return match, arg_type, arg_name, arg_value

            # If no sql injection detected with libinjection, use regex
            pattern = needle_app.get_sqli_pattern()

            if len(value.split()) > 1 and len(pattern.findall(value)) > 0 and query.find(value) > -1:
                match = True
                arg_type = obj['type']
                arg_name = obj['name']
                arg_value = obj['value']

                # Save request action to thread-data
                needle_data.req_data.incident_action = 'block'
                needle_data.req_data.incident_module = 'sqli'
                needle_data.req_data.incident_rule = 'sqli_2'

                return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        msg = 'Error checking SQL injection'
        if needle_app.adv_debug: msg += ':' + query
        needle_app.add_error(msg, error_data)

    return match, arg_type, arg_name, arg_value


# Instrumented function for mysql.connection.cursor.execute
def needle_sql_cursor_execute(*args, **kwargs):
    lang_module = 'mysql.connection.cursor.execute'
    sec_module = 'sqli'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        req_data = needle_data.req_data.data
    except Exception as e:
        error_data = str(e)
        msg = 'Error checking SQL injection in module: ' + lang_module

        try:
            if needle_app.adv_debug: msg += '  / query: ' + args[0]
        except Exception as e:
            pass

        needle_app.add_error(msg, error_data)

        return needle_app.orig_sql_cursor_execute(*args, **kwargs)

    ts_fn_start = None
    try:
        ts_fn_start = int(time.time() * 1000)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting perf tracking:'+lang_module, error_data)

    try:
        needle_app.add_module(sec_module, 'mysql.connection.cursor', 'execute')
    except Exception as e:
        pass

    try:
        # Check for SQL injection
        sqli_check, action = needle_app.module_active(sec_module)
        if sqli_check:
            needle_app.inc_mod_requests(sec_module, lang_module)
            match, arg_type, arg_name, arg_value = check_sql_injection(args[0])
            if match:
                if needle_app.debug_mode: print('Needle.sh: New Incident of type: SQL injection (rule: '+needle_data.req_data.incident_rule+')')

                if action == 'block':
                    # Change query to blank query
                    args = ('-- Query blocked by Needle.sh agent (Possible SQL injection)',)

                # Add mal request
                needle_app.add_mal_request(action, sec_module, arg_type, arg_name, arg_value, needle_data.req_data)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking SQL injection', error_data)

    try:
        fn_time = int(time.time() * 1000) - ts_fn_start
        needle_app.add_perf_time(needle_data.req_data, sec_module, lang_module, fn_time)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error adding perf time:' + lang_module, error_data)

    return needle_app.orig_sql_cursor_execute(*args, **kwargs)


# Wrapper class around mysql.connection.cursor
class NeedleSqlCursor():
    def __init__(self, cursor):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
        try:
            self.cursor = cursor
            # self.execute = patcher(self.cursor.execute)
            needle_app.orig_sql_cursor_execute = self.cursor.execute
            self.execute = needle_sql_cursor_execute
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising cursor object:', error_data)

    def __getattr__(self, name):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()
        try:
            return getattr(self.cursor, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom cursor method:', error_data)


# Wrapper class around mysql.connection
class NeedleSqlConnection():
    def __init__(self, connection):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            self.connection = connection
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error initialising custom SQL connection object:', error_data)

    def cursor(self, *args, **kwargs):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            orig_cursor = self.connection.cursor(*args, **kwargs)
            return NeedleSqlCursor(orig_cursor)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error getting cursor object from SQL connection:', error_data)

    # Handle unknown method calls
    def __getattr__(self, name):
        from .needle_app import get_needle_app
        needle_app = get_needle_app()

        try:
            return getattr(self.connection, name)
        except Exception as e:
            error_data = str(e)
            needle_app.add_error('Error returning custom connection method:', error_data)


# Instrumented function for MySQL connect
def needle_mysql_connect(*args, **kwargs):
    py_module = 'mysql.connector.connect'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        conn = get_orig(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented MySQL connect:', error_data)


# Instrumented function for MySQL connect
def needle_psycopg2_connect(*args, **kwargs):
    py_module = 'psycopg2.connect'

    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    try:
        # conn = needle_app.orig_mysql_connect(*args, **kwargs)
        conn = get_orig(py_module)(*args, **kwargs)
        return NeedleSqlConnection(conn)
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error in instrumented psycopg2 connect:', error_data)


# Check security scanner
def check_sec_scanner():
    from .needle_app import get_needle_app
    needle_app = get_needle_app()

    match = False
    arg_type = ''
    arg_name = ''
    arg_value = ''

    if needle_app.debug_mode: print('Needle.sh: Checking security scanner')

    try:
        scan_pattern = needle_app.get_scanner_pattern()
        if not scan_pattern: return match, arg_type, arg_name, arg_value

        value = needle_data.req_data.http_user_agent

        if value == '': return match, arg_type, arg_name, arg_value

        if len(scan_pattern.findall(value)) > 0:
            match = True
            arg_type = 'http_header'
            arg_name = 'user_agent'
            arg_value = value

            return match, arg_type, arg_name, arg_value

    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error checking security scanner:', error_data)

    return match, arg_type, arg_name, arg_value
