import requests
import json
import time
import platform
import re
import time

# Class to pass request data
class RequestData:
    data = []
    remote_addr = ''
    request_method = ''
    http_host = ''
    path_info = ''
    http_user_agent = ''
    incident_action = ''
    incident_module = ''
    incident_rule = ''
    req_start_ts = None
    perf_data = []

    def __init__(self):
        self.data = []
        self.remote_addr = ''
        self.request_method = ''
        self.http_host = ''
        self.path_info = ''
        self.http_user_agent = ''
        self.incident_action = ''
        self.incident_module = ''
        self.incident_rule = ''
        self.req_start_ts = None
        self.perf_data = []


# Class to keep track of instrumented methods
class InstrMethod:
    sec_module = ''
    py_module = ''
    orig_method = None
    is_instr = False


class PerfTime:
    sec_module = ''
    lang_module = ''
    time = 0

    def __init__(self, sec_module, lang_module, time):
        self.sec_module = sec_module
        self.lang_module = lang_module
        self.time = time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class PerfRecord:
    path = ''
    req_ts = 0
    perf_times = []

    def __init__(self, path, req_ts, perf_times):
        self.path = path
        self.req_ts = req_ts
        self.perf_times = perf_times

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class NeedleApp:
    agent_version = ''
    app_id = ''
    api_key = ''
    server_url = ''
    platform = 'python'
    framework = ''
    project_dir = ''
    settings = {}
    app_active = False
    errors = []
    total_requests = 0
    mal_requests = []
    module_requests = []
    modules_used = []
    test_mode = False
    debug_mode = False
    adv_debug = False
    instr_list = []
    is_instr = False
    libinjec = None
    sqli_pattern = None
    xss_pattern = None
    cmdi_pattern = None
    mdbi_pattern = None
    scan_pattern = None
    orig_sql_cursor_execute = None
    show_blocked_message = False
    use_libinjec = True # Mark false if libinjection should not be used
    flask_app = None
    run_agent = False
    perf_data = []
    perf_active = True
    perf_collect = True
    perf_count = 0
    perf_max = 100
    perf_interval = 12
    perf_collect_ts = 0.0

    def __init__(self, debug=False, show_blocked_message=False, flask_app=None):
        self.debug_mode = debug
        self.show_blocked_message = show_blocked_message
        self.flask_app = flask_app

        # Check if framework supported
        if not self.detect_framework():
            # Framework not supported, stop execution
            print("Needle.sh error: Web framework not supported")
            return

        # Load settings from needle.json
        try:
            filepath = self.project_dir + '/needle.json'
            with open(filepath) as fp:
                content = fp.read()
                needle_settings = json.loads(content)
                self.app_id = needle_settings['app_id']
                self.api_key = needle_settings['api_key']
                self.server_url = needle_settings['server_url']
                test_mode = needle_settings['test_mode']
                self.test_mode = False
                if test_mode == 1:
                    self.test_mode = True
                    print('Needle.sh: Agent in Test Mode')
        except Exception as e:
            error_data = str(e)
            self.add_error(
                'Error opening needle.json file. Please make sure that the file is present in your project\'s '
                'root folder', error_data)
            self.add_error('Error opening needle.json. Trying needle.ini', '')

        if self.app_id == '' or self.api_key == '':
            # Load settings from .ini file
            try:
                filepath = self.project_dir + '/needle.ini'
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        # print("line = " + line)
                        if line[0] != '#':
                            s_name, s_value = line.strip().split('=')
                            if s_name == 'app_id': self.app_id = s_value
                            if s_name == 'api_key': self.api_key = s_value
                            if s_name == 'server_url': self.server_url = s_value
                            if s_name == 'test_mode':
                                if s_value == '0':
                                    self.test_mode = False
                                elif s_value == '1':
                                    self.test_mode = True
                                    print('Needle.sh: Agent in Test Mode')
            except Exception as e:
                error_data = str(e)
                self.add_error('Error opening needle.ini file. Please make sure that the file is present in your project\'s '
                               'root folder', error_data)
            return

        if self.app_id == '' or self.api_key == '':
            print("Needle.sh error: App ID or API key incorrect")
        else:
            self.run_agent = True

        return

    # Detect project framework
    def detect_framework(self):
        detected = False
        # Check for Django framework
        try:
            from django.conf import settings
            self.framework = 'django'
            self.project_dir = settings.BASE_DIR
            detected = True
        except Exception as e:
            pass

        try:
            import flask
            self.framework = 'flask'
            self.project_dir = self.flask_app.root_path
            detected = True
        except Exception as e:
            pass

        return detected

    # Add error
    def add_error(self, error, error_data):
        if self.debug_mode: print('Needle.sh: Error! ', error, error_data)
        self.errors.append({'platform': self.platform, 'error': error, 'error_data': error_data})

    # Add malicious request
    def add_mal_request(self, action, reason, arg_type, arg_name, arg_value, req_data):
        from .utilities import clean_server_values

        # Check for sensitive data
        arg_name, arg_value = clean_server_values(arg_name, arg_value)

        mal_req = {}
        mal_req['type'] = action
        mal_req['reason'] = reason
        mal_req['arg_type'] = arg_type
        mal_req['arg_name'] = arg_name
        mal_req['arg_value'] = arg_value
        mal_req['client_ip'] = req_data.remote_addr
        mal_req['http_method'] = req_data.request_method
        mal_req['server'] = req_data.http_host
        mal_req['path'] = req_data.path_info
        mal_req['user_agent'] = req_data.http_user_agent

        if self.debug_mode: print('Needle.sh: Adding incident: ', mal_req)
        self.mal_requests.append(mal_req)

    # Increment module request count
    def inc_mod_requests(self, sec_module, lang_module):
        index = -1

        for i, obj in enumerate(self.module_requests):
            if obj['sec_module'] == sec_module and obj['lang_module'] == lang_module:
                index = i
                break

        if index == -1:
            self.module_requests.append({'sec_module': sec_module, 'lang_module': lang_module, 'count': 1})
        else:
            self.module_requests[index]['count'] += 1

    # Add module
    def add_module(self, type, package, method):
        module = {'type': type, 'package': package, 'method': method}
        if not (module in self.modules_used): self.modules_used.append(module)

    # Call APIs at regular intervals
    def api_thread(self):
        settings_ping_count = 0
        errors_count = 0
        app_info_count = 0

        try:
            while True:
                # Get app settings
                if settings_ping_count == 0:
                    self.api_get_settings()

                # Send total_req data every minute
                if self.app_active and (self.total_requests > 0 or len(self.mal_requests) > 0):
                    self.api_send_req_data()

                # Send agent errors
                if self.app_active and errors_count == 0 and (len(self.errors) > 0):
                    self.api_send_app_info('errors')

                # Send modules used data
                if self.app_active and app_info_count == 0:
                    self.api_send_app_info('app_info')

                settings_ping_count += 1
                errors_count += 1
                app_info_count += 1

                if settings_ping_count == 1: settings_ping_count = 0
                if errors_count == 1: errors_count = 0
                if app_info_count == 1: app_info_count = 0  # Send frequency = 10 mins

                # Pause for 60 seconds
                time.sleep(60)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending req data', error_data)

    # Get payload for API calls
    def get_api_payload(self):
        test_mode = 0
        if self.test_mode: test_mode = 1
        libinjec = 0
        if self.get_libinjec(): libinjec = 1

        payload = {'app_id': self.app_id, 'api_key': self.api_key, 'test_mode': test_mode, 'libinjec': libinjec,
                   'platform': self.platform, 'framework': self.framework, 'agent_version': self.agent_version}
        return payload

    # Send app info - agent errors, modules used
    def api_send_app_info(self, info):
        if self.debug_mode: print('Needle.sh: Sending app info data')

        try:
            url = self.server_url + '/api/store_app_info'
            data = self.get_api_payload()

            if info == 'errors' and len(self.errors) > 0:
                data['agent_errors'] = self.errors
                self.errors = []

            if info == 'app_info':
                if len(self.modules_used) > 0:
                    data['modules_used'] = self.modules_used
                    self.modules_used = []

                if len(self.perf_data) > 0:
                    data['perf_data'] = self.perf_data
                    self.perf_data = []

            json_data = json.dumps(data)
            x = requests.post(url, data=json_data)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending app info', error_data)

    # Send requests data - total requests, malicious requests
    def api_send_req_data(self):
        if self.debug_mode: print('Needle.sh: Sending requests data')

        data = {}
        try:
            url = self.server_url + '/api/store_requests'
            data = self.get_api_payload()

            if self.total_requests > 0:
                data['total_requests'] = self.total_requests
                self.total_requests = 0

            if len(self.mal_requests) > 0:
                data['mal_requests'] = self.mal_requests
                self.mal_requests = []

            if len(self.module_requests) > 0:
                data['mod_requests'] = self.module_requests
                self.module_requests = []

            json_data = json.dumps(data)
            req = requests.post(url, data=json_data)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while sending req data', error_data)
            # Since requests data could not be sent, save in variable
            # Todo: Make sure that total_req and mal_req dont become too big in size
            self.total_requests += data['total_requests']
            if len(data['mal_requests']) > 0:
                a = data['mal_requests']
                b = self.mal_requests
                a.extend(b)
                self.mal_requests = a

            if len(data['mod_requests']) > 0:
                a = data['mod_requests']
                b = self.module_requests
                a.extend(b)
                self.module_requests = a

    # Get app settings
    def api_get_settings(self):
        if self.debug_mode: print('Needle.sh: Getting app settings')

        try:
            api_url = self.server_url + '/api/get_app_settings'
            # if self.debug_mode: print('Needle API: get app settings. url = ', api_url)
            data = self.get_api_payload()
            json_data = json.dumps(data)

            req = requests.post(api_url, data=json_data)
            if self.debug_mode: print("Needle.sh: Received app settings = ", req.text)

            resp = json.loads(req.text)
            self.settings = resp['settings']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while fetching settings', error_data)

        try:
            if self.settings['active'] == 1:
                self.app_active = True
                self.instrument('basic', True)

                if 'sqli' in self.settings and self.settings['sqli']['active'] == 1:
                    self.instrument('sqli', True)
                else:
                    self.instrument('sqli', False)

                if 'xss' in self.settings and self.settings['xss']['active'] == 1:
                    self.instrument('xss', True)
                else:
                    self.instrument('xss', False)

                if 'cmdi' in self.settings and self.settings['cmdi']['active'] == 1:
                    self.instrument('cmdi', True)
                else:
                    self.instrument('cmdi', False)

                if 'lfi' in self.settings and self.settings['lfi']['active'] == 1:
                    self.instrument('lfi', True)
                else:
                    self.instrument('lfi', False)

                if 'ssrf' in self.settings and self.settings['ssrf']['active'] == 1:
                    self.instrument('ssrf', True)
                else:
                    self.instrument('ssrf', False)

            elif self.settings['active'] == 0:
                self.app_active = False
                self.instrument('basic', False)
                self.instrument('sqli', False)
                self.instrument('xss', False)
                self.instrument('cmdi', False)
                self.instrument('lfi', False)
                self.instrument('ssrf', False)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error while instrumenting', error_data)

    # Update instr status for module
    def update_instr_status(self, sec_module, py_module, orig_method, is_instr):
        is_present = False
        for index, obj in enumerate(self.instr_list):
            if obj.sec_module == sec_module and obj.py_module == py_module:
                is_present = True
                self.instr_list[index].is_instr = is_instr
                break

        # If not present, add object with new status
        if not is_present:
            instr_method = InstrMethod()
            instr_method.sec_module = sec_module
            instr_method.py_module = py_module
            instr_method.orig_method = orig_method
            instr_method.is_instr = is_instr
            self.instr_list.append(instr_method)

        return is_instr

    # Get instrumentation status for module
    def get_module_status(self, py_module):
        is_instr = False
        for obj in self.instr_list:
            if obj.py_module == py_module and obj.is_instr:
                is_instr = True
                break

        return is_instr

    # Return original method for instrumented method
    def get_orig_method(self, py_module):
        for obj in self.instr_list:
            if obj.py_module == py_module:
                return obj.orig_method

    # Instrument
    def instrument(self, sec_module, is_instr):
        from .wrappers import set_wrapper, get_wrapper
        instr_module_list = [
            {'sec_module': 'basic', 'framework': 'django',
             'py_module': 'django.core.handlers.base.BaseHandler.get_response'},
            {'sec_module': 'basic', 'framework': 'flask', 'py_module': 'flask.signals.request_started'},
            {'sec_module': 'basic', 'framework': 'flask', 'py_module': 'flask.signals.request_finished'},
            {'sec_module': 'xss', 'framework': 'django', 'py_module': 'django.template.loader.render_to_string'},
            {'sec_module': 'xss', 'framework': 'flask', 'py_module': 'flask.render_template'},
            {'sec_module': 'sqli', 'framework': '', 'py_module': 'mysql.connector.connect'},
            {'sec_module': 'sqli', 'framework': '', 'py_module': 'psycopg2.connect'},
            {'sec_module': 'cmdi', 'framework': '', 'py_module': 'os.system'},
            {'sec_module': 'cmdi', 'framework': '', 'py_module': 'os.popen'},
            {'sec_module': 'lfi', 'framework': '', 'py_module': 'builtins.open'},
            {'sec_module': 'ssrf', 'framework': '', 'py_module': 'requests.get'},
            {'sec_module': 'ssrf', 'framework': '', 'py_module': 'urllib.request.urlopen'}
        ]

        for mod in instr_module_list:
            if mod['sec_module'] != sec_module: continue
            if mod['framework'] != '' and mod['framework'] != self.framework: continue

            py_module = mod['py_module']

            if is_instr != self.get_module_status(py_module):
                if is_instr:
                    # Instrument module
                    if self.debug_mode: print('Needle.sh: Instrumenting module:', py_module)
                    try:
                        if py_module == 'flask.signals.request_started':
                            try:
                                import flask
                                flask.request_started.connect(get_wrapper(py_module), self.flask_app)
                                continue
                            except ImportError:
                                pass
                        elif py_module == 'flask.signals.request_finished':
                            try:
                                import flask
                                flask.request_finished.connect(get_wrapper(py_module), self.flask_app)
                                continue
                            except ImportError:
                                pass
                        else:
                            set_wrapper(py_module, True)

                        # Update instr status for py_module
                        self.update_instr_status(sec_module, py_module, None, True)
                    except Exception as e:
                        error_data = str(e)
                        self.add_error('Error while instrumenting module: ' + py_module, error_data)
                else:
                    # Uninstrument module
                    if self.debug_mode: print('Un-instrumenting module:', py_module)
                    try:
                        if py_module == 'flask.signals.request_started':
                            try:
                                import flask, blinker
                                flask.request_started.disconnect(get_wrapper(py_module), sender=blinker.base.ANY)
                                continue
                            except ImportError:
                                pass
                        elif py_module == 'flask.signals.request_finished':
                            try:
                                import flask, blinker
                                flask.request_finished.disconnect(get_wrapper(py_module), sender=blinker.base.ANY)
                                continue
                            except ImportError:
                                pass
                        else:
                            set_wrapper(py_module, False)

                        # Update instr status for py_module
                        self.update_instr_status(sec_module, py_module, None, False)
                    except Exception as e:
                        error_data = str(e)
                        self.add_error('Error while un-instrumenting module: ' + py_module, error_data)

    # Get security headers to be inserted
    def get_sec_headers(self):
        headers = {}

        try:
            if self.app_active:
                if 'headers' in self.settings:
                    headers = self.settings['headers']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting security headers: ', error_data)

        return headers

    # Check if security module active
    def module_active(self, sec_module):
        active = False
        action = ''

        try:
            if self.app_active and sec_module in self.settings and self.settings[sec_module]['active'] == 1:
                active = True
                action = self.settings[sec_module]['action']
        except Exception as e:
            error_data = str(e)
            self.add_error('Error checking module active - '+sec_module+':', error_data)

        return active, action

    # Get libinjection module
    def get_libinjec(self):

        # Check the use_libinjec setting
        if not self.use_libinjec:
            return None

        try:
            if self.libinjec:
                return self.libinjec
            if not self.libinjec:
                libinjec = None
                op_system = platform.system()
                if op_system == 'Darwin':  # Mac OS
                    from .libinjection2.mac_x86_64 import libinjection
                    libinjec = libinjection
                elif op_system == 'Linux':
                    from .libinjection2.linux import libinjection
                    libinjec = libinjection
                elif op_system == '':
                    self.add_error('Error getting libinjec module for platform: ', 'Unrecognised platform')

                self.libinjec = libinjec
                return self.libinjec
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting libinjec module for platform: ', error_data)
            return None

    # Get XSS pattern
    def get_xss_pattern(self):
        try:
            if self.xss_pattern:
                return self.xss_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/data/js_event'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'\b(' + str_pattern + r')\b'
                str_pattern = r'(<[\\s]*script[\\s]*[>]*|javascript:|javascript&colon;|FSCommand)|' + str_pattern
                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.xss_pattern = pattern
                return self.xss_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting XSS pattern:', error_data)
            return None

    # Get sqli pattern
    def get_sqli_pattern(self):
        try:
            if self.sqli_pattern:
                return self.sqli_pattern
            else:
                pattern = re.compile(
                    r'\b(select|update|insert|alter|create|drop|delete|merge|union|show|exec|or|and|order|sleep|having|'
                    r'xor|like|regexp)\b|(&&|\|\|)',
                    re.IGNORECASE)

                self.sqli_pattern = pattern
                return self.sqli_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting sqli pattern:', error_data)
            return None

    # Get command injection pattern
    def get_cmdi_pattern(self):
        try:
            if self.cmdi_pattern:
                return self.cmdi_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/data/unix_cmd'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line.rstrip('+') + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'(?:;|\{|\||\|\||&|&&|\n|\r|\$\(|\$\(\(|`|\${|<\(|>\(|\(\s*\))\s*' \
                              r'(?:{|\s*\(\s*|\w+=(?:[^\s]*|\$.*|\$.*|<.*|>.*|\'.*\'|\".*\")\s+|!\s*|\$)*\s*(?:\'|\")*' \
                              r'(?:[\?\*\[\]\(\)\-\|+\w\'\"\./\\\\]+\/)?[\\\\\'\"]*'+str_pattern+'\b'

                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.cmdi_pattern = pattern
                return self.cmdi_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting cmdi pattern:', error_data)
            return None

    # Get security scanner pattern
    def get_scanner_pattern(self):
        try:
            if self.scan_pattern:
                return self.scan_pattern
            else:
                import os, sys, inspect
                current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                filepath = current_dir + '/data/scan'

                str_pattern = ''
                with open(filepath) as fp:
                    for cnt, line in enumerate(fp):
                        line = line.strip()
                        if line == '' or line[0] == '#': continue

                        str_pattern += line.rstrip('+') + '|'

                str_pattern = str_pattern.rstrip('|')
                str_pattern = r'\b(' + str_pattern + r')\b'

                pattern = re.compile(str_pattern, re.IGNORECASE)

                self.scan_pattern = pattern
                return self.scan_pattern
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting scan pattern:', error_data)
            return None

    # Get project modules
    def get_project_modules(self):
        try:
            import sys
            all_modules = sys.modules.keys()
            module_list = []
            for m in all_modules:
                # Only get parent module name. e.g. If module is mysql.connector, only get mysql
                parts = m.split('.')
                # print(parts[0])
                if parts[0] not in module_list:
                    module_list.append(parts[0])

            # print('Modules = ', len(module_list), module_list)
        except Exception as e:
            error_data = str(e)
            self.add_error('Error getting module list', error_data)

    # Return content for blocked message
    def get_blocked_page_content(self, module_id=''):
        str_content = ''
        if self.show_blocked_message:
            module_name = ''

            if module_id == 'sqli': module_name = 'SQL injection'
            if module_id == 'xss': module_name = 'Cross-site Scripting(XSS)'
            if module_id == 'cmdi': module_name = 'Command injection'
            if module_id == 'scan': module_name = 'Security scanner'
            if module_id == 'lfi': module_name = 'Local File Inclusion (LFI)'
            if module_id == 'ssrf': module_name = 'Server Side Request Forgery (SSRF)'

            str_content = 'Blocked by Needle.sh! Attack type: ' + module_name

        return str_content

    def check_perf_collect(self):
        if not self.perf_active: return False

        if self.perf_collect:
            if self.perf_count > self.perf_max:
                self.perf_collect = False
                self.perf_collect_ts = int(time.time()) + self.perf_interval * 3600
        else:
            # Check if collection should be turned on
            if time.time() > self.perf_collect_ts:
                self.perf_collect = True
                self.perf_count = 0

        return self.perf_collect

    def add_perf_time(self, req_data, sec_module, lang_module, time):
        if self.check_perf_collect():
            #p = PerfTime(sec_module, lang_module, time)
            p = {'sec_module': sec_module, 'lang_module': lang_module, 'time': time}
            req_data.perf_data.append(p)

    def add_perf_record(self, req_data):
        if self.check_perf_collect():
            #p = PerfRecord(req_data.path_info, req_data.req_start_ts, req_data.perf_data)
            perf_times = req_data.perf_data
            p = {'path': req_data.path_info, 'req_ts': req_data.req_start_ts, 'perf_times': perf_times}
            self.perf_data.append(p)
            self.perf_count += 1
