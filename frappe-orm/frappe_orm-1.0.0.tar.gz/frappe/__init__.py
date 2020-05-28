from werkzeug.local import Local, release_local
import re, os, sys, importlib, inspect, json
from six import iteritems, binary_type, text_type, string_types
import frappe

local = Local()

# local-globals
db = local("db")
conf = local("conf")
form = form_dict = local("form_dict")
flags = local("flags")
error_log = local("error_log")
debug_log = local("debug_log")
message_log = local("message_log")

lang = local("lang")


class _dict(dict):
    """dict like object that exposes keys as attributes"""

    def __getattr__(self, key):
        ret = self.get(key)
        if not ret and key.startswith("__"):
            raise AttributeError()
        return ret

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return self

    def __setstate__(self, d):
        self.update(d)

    def update(self, d):
        """update and return self -- the missing dict feature in python"""
        super(_dict, self).update(d)
        return self

    def copy(self):
        return _dict(dict(self).copy())


class init_frappe:
    def __init__(self):
        '''If site==None, initialize it for empty site ('') to load common_site_config.json'''

    def __enter__(self):
        init()
        return local

    def __exit__(self, type, value, traceback):
        destroy()


def init(sites_path=None, new_site=False):
    """Initialize frappe for the current site. Reset thread locals `frappe.local`"""
    if getattr(local, "initialised", None):
        return

    local.error_log = []
    local.message_log = []
    local.debug_log = []
    local.realtime_log = []
    local.flags = _dict({
        "ran_schedulers": [],
        "currently_saving": [],
        "redirect_location": "",
        "in_install_db": False,
        "in_install_app": False,
        "in_import": False,
        "in_test": False,
        "mute_messages": False,
        "ignore_links": False,
        "mute_emails": False,
        "has_dataurl": False,
        "new_site": new_site
    })
    local.rollback_observers = []
    local.test_objects = {}

    local.site = "Nana"
    local.sites_path = sites_path
    local.site_path = os.path.abspath('.')
    local.request_ip = None
    local.response = _dict({"docs": []})
    local.task_id = None

    local.conf = _dict(get_site_config())
    local.lang = local.conf.lang or "en"
    local.lang_full_dict = None

    local.module_app = None
    local.app_modules = None
    local.system_settings = _dict()

    local.user = None
    local.user_perms = None
    local.session = None
    local.role_permissions = {}
    local.valid_columns = {}
    local.new_doc_templates = {}
    local.link_count = {}

    local.jenv = None
    local.jloader = None
    local.cache = {}
    local.document_cache = {}
    local.meta_cache = {}
    local.form_dict = _dict()
    local.session = _dict()

    # setup_module_map()

    local.initialised = True


def connect():
    """Connect to site database instance.

    :param site: If site is given, calls `frappe.init`.
    :param db_name: Optional. Will use from `site_config.json`."""
    from frappe.database import get_db
    init()

    local.db = get_db(user=getattr(local.conf, 'db_user', '') or local.conf.db_name)


def destroy():
    """Closes connection and releases werkzeug local."""
    if db:
        db.close()

    release_local(local)


def get_site_config():
    """Returns `site_config.json` combined with `sites/common_site_config.json`.
    `site_config` is a set of site wide settings like database name, password, email etc."""
    config = {}

    site_path = getattr(local, "site_path", None)

    if site_path:
        common_site_config = os.path.join(site_path, "common_site_config.json")
        if os.path.exists(common_site_config):
            config.update(get_file_json(common_site_config))

    # if site_path:
    #     site_config = os.path.join(site_path, "site_config.json")
    #     if os.path.exists(site_config):
    #         config.update(get_file_json(site_config))
    #     elif local.site and not local.flags.new_site:
    #         print("{0} does not exist".format(local.site))
    #         sys.exit(1)
    # raise IncorrectSitePath, "{0} does not exist".format(site_config)

    return _dict(config)


def get_conf(site=None):
    if hasattr(local, 'conf'):
        return local.conf

    else:
        # if no site, get from common_site_config.json
        with init_frappe(site):
            return local.conf


def get_file_json(path):
    """Read a file and return parsed JSON object."""
    with open(path, 'r') as f:
        return json.load(f)


def _(msg, lang=None):
    """Returns translated string in current lang, if exists."""
    if not hasattr(local, 'lang'):
        local.lang = lang or 'en'

    non_translated_msg = msg
    return non_translated_msg


def compare(val1, condition, val2):
    """Compare two values using `frappe.utils.compare`

    `condition` could be:
    - "^"
    - "in"
    - "not in"
    - "="
    - "!="
    - ">"
    - "<"
    - ">="
    - "<="
    - "not None"
    - "None"
    """
    import frappe.utils
    return frappe.utils.compare(val1, condition, val2)


# def html_to_js_template(path, content):
#     '''returns HTML template content as Javascript code, adding it to `frappe.templates`'''
#     return """frappe.templates["{key}"] = '{content}';\n""".format( \
#         key=path.rsplit("/", 1)[-1][:-5], content=scrub_html_template(content))
#
# def scrub_html_template(content):
#     '''Returns HTML content with removed whitespace and comments'''
#     # remove whitespace to a single space
#     content = re.sub("\s+", " ", content)
#
#     # strip comments
#     content =  re.sub("(<!--.*?-->)", "", content)
#
#     return content.replace("'", "\'")


def clear_cache(user=None, doctype=None):
    """Clear **User**, **DocType** or global cache.

    :param user: If user is given, only user cache is cleared.
    :param doctype: If doctype is given, only DocType cache is cleared."""
    pass


def safe_decode(param, encoding='utf-8'):
    try:
        param = param.decode(encoding)
    except Exception:
        pass
    return param


def as_unicode(text, encoding='utf-8'):
    '''Convert to unicode if required'''
    if isinstance(text, text_type):
        return text
    elif text == None:
        return ''
    elif isinstance(text, binary_type):
        return text_type(text, encoding)
    else:
        return text_type(text)


def get_meta(doctype, cached=True):
    """Get `frappe.model.meta.Meta` instance of given doctype name."""
    import frappe.model.meta
    return frappe.model.meta.get_meta(doctype, cached=cached)


def bold(text):
    return '<b>{0}</b>'.format(text)


def has_permission(doctype=None, ptype="read", doc=None, user=None, verbose=False, throw=False):
    """Raises `frappe.PermissionError` if not permitted.

    :param doctype: DocType for which permission is to be check.
    :param ptype: Permission type (`read`, `write`, `create`, `submit`, `cancel`, `amend`). Default: `read`.
    :param doc: [optional] Checks User permissions for given doc.
    :param user: [optional] Check for given user. Default: current user."""
    if not doctype and doc:
        doctype = doc.doctype

    out = True
    if throw and not out:
        if doc:
            frappe.throw(_("No permission for {0}").format(doc.doctype + " " + doc.name))
        else:
            frappe.throw(_("No permission for {0}").format(doctype))

    return out


def throw(msg, exc=0, title=None):
    """Throw execption and show message (`msgprint`).

    :param msg: Message.
    :param exc: Exception class. Default `frappe.ValidationError`"""
    msgprint(msg, raise_exception=exc, title=title, indicator='red')


def msgprint(msg, title=None, raise_exception=0, as_table=False, indicator=None, alert=False):
    """Print a message to the user (via HTTP response).
    Messages are sent in the `__server_messages` property in the
    response JSON and shown in a pop-up / modal.

    :param msg: Message.
    :param title: [optional] Message title.
    :param raise_exception: [optional] Raise given exception and show message.
    :param as_table: [optional] If `msg` is a list of lists, render as HTML table.
    """
    from frappe.utils import encode

    msg = safe_decode(msg)
    out = _dict(message=msg)

    def _raise_exception():
        if raise_exception:
            if flags.rollback_on_exception:
                db.rollback()
            import inspect

            if inspect.isclass(raise_exception) and issubclass(raise_exception, Exception):
                raise raise_exception(msg)
            else:
                raise ValidationError(msg)

    if flags.mute_messages:
        _raise_exception()
        return

    if as_table and type(msg) in (list, tuple):
        out.msg = '<table border="1px" style="border-collapse: collapse" cellpadding="2px">' + ''.join(
            ['<tr>' + ''.join(['<td>%s</td>' % c for c in r]) + '</tr>' for r in msg]) + '</table>'

    if flags.print_messages and out.msg:
        print("Message: " + repr(out.msg).encode("utf-8"))

    if title:
        out.title = title

    if not indicator and raise_exception:
        indicator = 'red'

    if indicator:
        out.indicator = indicator

    if alert:
        out.alert = 1

    message_log.append(json.dumps(out))

    if raise_exception and hasattr(raise_exception, '__name__'):
        local.response['exc_type'] = raise_exception.__name__

    _raise_exception()


def get_list(doctype, *args, **kwargs):
    """List database query via `frappe.model.db_query`. Will also check for permissions.

    :param doctype: DocType on which query is to be made.
    :param fields: List of fields or `*`.
    :param filters: List of filters (see example).
    :param order_by: Order By e.g. `modified desc`.
    :param limit_page_start: Start results at record #. Default 0.
    :param limit_page_length: No of records in the page. Default 20.

    Example usage:

        # simple dict filter
        frappe.get_list("ToDo", fields=["name", "description"], filters = {"owner":"test@example.com"})

        # filter as a list of lists
        frappe.get_list("ToDo", fields="*", filters = [["modified", ">", "2014-01-01"]])

        # filter as a list of dicts
        frappe.get_list("ToDo", fields="*", filters = {"description": ("like", "test%")})
    """
    import frappe.model.db_query
    return frappe.model.db_query.DatabaseQuery(doctype).execute(None, *args, **kwargs)


def get_all(doctype, *args, **kwargs):
    """List database query via `frappe.model.db_query`. Will **not** check for permissions.
    Parameters are same as `frappe.get_list`

    :param doctype: DocType on which query is to be made.
    :param fields: List of fields or `*`. Default is: `["name"]`.
    :param filters: List of filters (see example).
    :param order_by: Order By e.g. `modified desc`.
    :param limit_start: Start results at record #. Default 0.
    :param limit_page_length: No of records in the page. Default 20.

    Example usage:

        # simple dict filter
        frappe.get_all("ToDo", fields=["name", "description"], filters = {"owner":"test@example.com"})

        # filter as a list of lists
        frappe.get_all("ToDo", fields=["*"], filters = [["modified", ">", "2014-01-01"]])

        # filter as a list of dicts
        frappe.get_all("ToDo", fields=["*"], filters = {"description": ("like", "test%")})
    """
    kwargs["ignore_permissions"] = True
    if not "limit_page_length" in kwargs:
        kwargs["limit_page_length"] = 0
    return get_list(doctype, *args, **kwargs)


def get_value(*args, **kwargs):
    """Returns a document property or list of properties.

    Alias for `frappe.db.get_value`

    :param doctype: DocType name.
    :param filters: Filters like `{"x":"y"}` or name of the document. `None` if Single DocType.
    :param fieldname: Column name.
    :param ignore: Don't raise exception if table, column is missing.
    :param as_dict: Return values as dict.
    :param debug: Print query in error log.
    """
    return db.get_value(*args, **kwargs)


if sys.version_info.major == 2:
    class FileNotFoundError(Exception):
        pass
else:
    from builtins import FileNotFoundError


class ValidationError(Exception):
    http_status_code = 417


class AuthenticationError(Exception):
    http_status_code = 401


class SessionExpired(Exception):
    http_status_code = 401


class PermissionError(Exception):
    http_status_code = 403


class DoesNotExistError(ValidationError):
    http_status_code = 404


class NameError(Exception):
    http_status_code = 409


class OutgoingEmailError(Exception):
    http_status_code = 501


class SessionStopped(Exception):
    http_status_code = 503


class UnsupportedMediaType(Exception):
    http_status_code = 415


class RequestToken(Exception):
    http_status_code = 200


class Redirect(Exception):
    http_status_code = 301


class CSRFTokenError(Exception):
    http_status_code = 400


class ImproperDBConfigurationError(Exception):
    """
    Used when frappe detects that database or tables are not properly
    configured
    """

    def __init__(self, reason, msg=None):
        if not msg:
            msg = "MariaDb is not properly configured"
        super(ImproperDBConfigurationError, self).__init__(msg)
        self.reason = reason


def html_to_js_template(path, content):
    '''returns HTML template content as Javascript code, adding it to `frappe.templates`'''
    return """frappe.templates["{key}"] = '{content}';\n""".format( \
        key=path.rsplit("/", 1)[-1][:-5], content=scrub_html_template(content))


def scrub_html_template(content):
    '''Returns HTML content with removed whitespace and comments'''
    # remove whitespace to a single space
    content = re.sub("\s+", " ", content)

    # strip comments
    content = re.sub("(<!--.*?-->)", "", content)

    return content.replace("'", "\'")


def get_doc(*args, **kwargs):
    """Return a `frappe.model.document.Document` object of the given type and name.

    :param arg1: DocType name as string **or** document JSON.
    :param arg2: [optional] Document name as string.

    Examples:

        # insert a new document
        todo = frappe.get_doc({"doctype":"ToDo", "description": "test"})
        tood.insert()

        # open an existing document
        todo = frappe.get_doc("ToDo", "TD0001")

    """
    import frappe.model.document
    doc = frappe.model.document.get_doc(*args, **kwargs)

    return doc


def new_doc(doctype, parent_doc=None, parentfield=None, as_dict=False):
    """Returns a new document of the given DocType with defaults set.

    :param doctype: DocType of the new document.
    :param parent_doc: [optional] add to parent document.
    :param parentfield: [optional] add against this `parentfield`."""
    from frappe.model.create_new import get_new_doc
    return get_new_doc(doctype, parent_doc, parentfield, as_dict=as_dict)


def set_value(doctype, docname, fieldname, value=None):
    pass


# frappe Initialize
connect()


# Global
def get_defaults(user=None):
    globald = get_defaults_for()

    if not user:
        user = "Guest"

    if user:
        userd = {}
        userd.update(get_defaults_for(user))
        userd.update({"user": user, "owner": user})
        globald.update(userd)

    return globald


def set_global_default(key, value):
    set_default(key, value, "__default")


def add_global_default(key, value):
    add_default(key, value, "__default")


def get_global_default(key):
    d = get_defaults().get(key, None)

    value = isinstance(d, (list, tuple)) and d[0] or d
    return value


# Common

def get_module(modulename):
    """Returns a module object for given Python module name using `importlib.import_module`."""
    pass


def scrub(txt):
    """Returns sluggified string. e.g. `Sales Order` becomes `sales_order`."""
    return txt.replace(' ', '_').replace('-', '_').lower()


def set_default(key, value, parent, parenttype="__default"):
    """Override or add a default value.
    Adds default value in table `tabDefaultValue`.

    :param key: Default key.
    :param value: Default value.
    :param parent: Usually, **User** to whom the default belongs.
    :param parenttype: [optional] default is `__default`."""
    if frappe.db.sql('''
		select
			defkey
		from
			`tabDefaultValue`
		where
			defkey=%s and parent=%s
		for update''', (key, parent)):
        frappe.db.sql("""
			delete from
				`tabDefaultValue`
			where
				defkey=%s and parent=%s""", (key, parent))
    if value != None:
        add_default(key, value, parent)
    else:
        pass


def add_default(key, value, parent, parenttype=None):
    d = frappe.get_doc({
        "doctype": "DefaultValue",
        "parent": parent,
        "parenttype": parenttype or "__default",
        "parentfield": "system_defaults",
        "defkey": key,
        "defvalue": value
    })
    d.insert(ignore_permissions=True)


def clear_default(key=None, value=None, parent=None, name=None, parenttype=None):
    """Clear a default value by any of the given parameters and delete caches.

    :param key: Default key.
    :param value: Default value.
    :param parent: User name, or `__global`, `__default`.
    :param name: Default ID.
    :param parenttype: Clear defaults table for a particular type e.g. **User**.
    """
    conditions = []
    values = []

    if name:
        conditions.append("name=%s")
        values.append(name)

    else:
        if key:
            conditions.append("defkey=%s")
            values.append(key)

        if value:
            conditions.append("defvalue=%s")
            values.append(value)

        if parent:
            conditions.append("parent=%s")
            values.append(parent)

        if parenttype:
            conditions.append("parenttype=%s")
            values.append(parenttype)

    if not conditions:
        raise Exception("[clear_default] No key specified.")

    frappe.db.sql("""delete from tabDefaultValue where {0}""".format(" and ".join(conditions)),
                  tuple(values))


def get_defaults_for(parent="__default"):
    """get all defaults"""
    defaults = None

    if defaults == None:
        # sort descending because first default must get precedence
        res = frappe.db.sql("""select defkey, defvalue from `tabDefaultValue`
			where parent = %s order by creation""", (parent,), as_dict=1)

        defaults = frappe._dict({})
        for d in res:
            if d.defkey in defaults:
                # listify
                if not isinstance(defaults[d.defkey], list) and defaults[d.defkey] != d.defvalue:
                    defaults[d.defkey] = [defaults[d.defkey]]

                if d.defvalue not in defaults[d.defkey]:
                    defaults[d.defkey].append(d.defvalue)

            elif d.defvalue is not None:
                defaults[d.defkey] = d.defvalue

    return defaults


class DuplicateEntryError(NameError): pass


class DataError(ValidationError): pass


class UnknownDomainError(Exception): pass


class MappingMismatchError(ValidationError): pass


class InvalidStatusError(ValidationError): pass


class MandatoryError(ValidationError): pass


class InvalidSignatureError(ValidationError): pass


class RateLimitExceededError(ValidationError): pass


class CannotChangeConstantError(ValidationError): pass


class CharacterLengthExceededError(ValidationError): pass


class UpdateAfterSubmitError(ValidationError): pass


class LinkValidationError(ValidationError): pass


class CancelledLinkError(LinkValidationError): pass


class DocstatusTransitionError(ValidationError): pass


class TimestampMismatchError(ValidationError): pass


class EmptyTableError(ValidationError): pass


class LinkExistsError(ValidationError): pass


class InvalidEmailAddressError(ValidationError): pass


class TemplateNotFoundError(ValidationError): pass


class UniqueValidationError(ValidationError): pass


class AppNotInstalledError(ValidationError): pass


class ImplicitCommitError(ValidationError): pass


class RetryBackgroundJobError(Exception): pass


class DocumentLockedError(ValidationError): pass


class CircularLinkingError(ValidationError): pass


class SecurityException(Exception): pass


class InvalidColumnName(ValidationError): pass


class IncompatibleApp(ValidationError): pass


class InvalidDates(ValidationError): pass


class DataTooLongException(ValidationError): pass
