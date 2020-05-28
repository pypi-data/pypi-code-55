import re, datetime, math, time
from dateutil import parser
import frappe
from six import iteritems, text_type, string_types, integer_types
import babel.dates
from babel.core import UnknownLocaleError
import operator, os

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S.%f"
DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT


def flt(s, precision=None):
    """Convert to float (ignore commas)"""
    if isinstance(s, string_types):
        s = s.replace(',', '')

    try:
        num = float(s)
        if precision is not None:
            num = rounded(num, precision)
    except Exception:
        num = 0

    return num


def rounded(num, precision=0):
    """round method for round halfs to nearest even algorithm aka banker's rounding - compatible with python3"""
    precision = cint(precision)
    multiplier = 10 ** precision

    # avoid rounding errors
    num = round(num * multiplier if precision else num, 8)

    floor = math.floor(num)
    decimal_part = num - floor

    if not precision and decimal_part == 0.5:
        num = floor if (floor % 2 == 0) else floor + 1
    else:
        if decimal_part == 0.5:
            num = floor + 1
        else:
            num = round(num)

    return (num / multiplier) if precision else num


def cint(s):
    """Convert to integer"""
    try:
        num = int(float(s))
    except:
        num = 0
    return num


def cast_fieldtype(fieldtype, value):
    if fieldtype in ("Currency", "Float", "Percent"):
        value = flt(value)

    elif fieldtype in ("Int", "Check"):
        value = cint(value)

    elif fieldtype in ("Data", "Text", "Small Text", "Long Text",
                       "Text Editor", "Select", "Link", "Dynamic Link"):
        value = cstr(value)

    elif fieldtype == "Date":
        value = getdate(value)

    elif fieldtype == "Datetime":
        value = get_datetime(value)

    elif fieldtype == "Time":
        value = to_timedelta(value)

    return value


def cstr(s, encoding='utf-8'):
    return frappe.as_unicode(s, encoding)


def get_filter(doctype, f):
    """Returns a _dict like

        {
            "doctype":
            "fieldname":
            "operator":
            "value":
        }
    """
    from frappe.model import default_fields, optional_fields

    if isinstance(f, dict):
        key, value = next(iter(f.items()))
        f = make_filter_tuple(doctype, key, value)

    if not isinstance(f, (list, tuple)):
        frappe.throw(frappe._("Filter must be a tuple or list (in a list)"))

    if len(f) == 3:
        f = (doctype, f[0], f[1], f[2])
    elif len(f) > 4:
        f = f[0:4]
    elif len(f) != 4:
        frappe.throw(frappe._("Filter must have 4 values (doctype, fieldname, operator, value): {0}").format(str(f)))

    f = frappe._dict(doctype=f[0], fieldname=f[1], operator=f[2], value=f[3])

    sanitize_column(f.fieldname)

    if not f.operator:
        # if operator is missing
        f.operator = "="

    valid_operators = ("=", "!=", ">", "<", ">=", "<=", "like", "not like", "in", "not in", "is",
                       "between", "descendants of", "ancestors of", "not descendants of", "not ancestors of",
                       "previous", "next")
    if f.operator.lower() not in valid_operators:
        frappe.throw(frappe._("Operator must be one of {0}").format(", ".join(valid_operators)))

    if f.doctype and (f.fieldname not in default_fields + optional_fields):
        # verify fieldname belongs to the doctype
        meta = frappe.get_meta(f.doctype)
        if not meta.has_field(f.fieldname):

            # try and match the doctype name from child tables
            for df in meta.get_table_fields():
                if frappe.get_meta(df.options).has_field(f.fieldname):
                    f.doctype = df.options
                    break

    return f


def lock_exists(name):
    '''Returns True if lock of the given name exists'''
    return os.path.exists(name)


def sanitize_column(column_name):
    from frappe import _
    regex = re.compile("^.*[,'();].*")
    blacklisted_keywords = ['select', 'create', 'insert', 'delete', 'drop', 'update', 'case', 'and', 'or']

    def _raise_exception():
        frappe.throw(_("Invalid field name {0}").format(column_name), frappe.DataError)

    if 'ifnull' in column_name:
        if regex.match(column_name):
            # to avoid and, or
            if any(' {0} '.format(keyword) in column_name.split() for keyword in blacklisted_keywords):
                _raise_exception()

            # to avoid select, delete, drop, update and case
            elif any(keyword in column_name.split() for keyword in blacklisted_keywords):
                _raise_exception()

    elif regex.match(column_name):
        _raise_exception()


def cint(s):
    """Convert to integer"""
    try: num = int(float(s))
    except: num = 0
    return num


def make_filter_tuple(doctype, key, value):
    '''return a filter tuple like [doctype, key, operator, value]'''
    if isinstance(value, (list, tuple)):
        return [doctype, key, value[0], value[1]]
    else:
        return [doctype, key, "=", value]


number_format_info = {
    "#,###.##": (".", ",", 2),
    "#.###,##": (",", ".", 2),
    "# ###.##": (".", " ", 2),
    "# ###,##": (",", " ", 2),
    "#'###.##": (".", "'", 2),
    "#, ###.##": (".", ", ", 2),
    "#,##,###.##": (".", ",", 2),
    "#,###.###": (".", ",", 3),
    "#.###": ("", ".", 0),
    "#,###": ("", ",", 0)
}

operator_map = {
    # startswith
    "^": lambda a, b: (a or "").startswith(b),

    # in or not in a list
    "in": lambda a, b: operator.contains(b, a),
    "not in": lambda a, b: not operator.contains(b, a),

    # comparison operators
    "=": lambda a, b: operator.eq(a, b),
    "!=": lambda a, b: operator.ne(a, b),
    ">": lambda a, b: operator.gt(a, b),
    "<": lambda a, b: operator.lt(a, b),
    ">=": lambda a, b: operator.ge(a, b),
    "<=": lambda a, b: operator.le(a, b),
    "not None": lambda a, b: a and True or False,
    "None": lambda a, b: (not a) and True or False
}


def compare(val1, condition, val2):
    ret = False
    if condition in operator_map:
        ret = operator_map[condition](val1, val2)

    return ret


def format_time(txt):
    try:
        formatted_time = babel.dates.format_time(get_time(txt), locale=(frappe.local.lang or "").replace("-", "_"))
    except UnknownLocaleError:
        formatted_time = get_time(txt).strftime("%H:%M:%S")
    return formatted_time


def get_datetime_str(datetime_obj):
    if isinstance(datetime_obj, string_types):
        datetime_obj = get_datetime(datetime_obj)
    return datetime_obj.strftime(DATETIME_FORMAT)


def date_diff(string_ed_date, string_st_date):
    return (getdate(string_ed_date) - getdate(string_st_date)).days


def format_datetime(datetime_string, format_string=None):
    if not datetime_string:
        return

    datetime = get_datetime(datetime_string)
    if not format_string:
        format_string = get_user_format().replace("mm", "MM") + " HH:mm:ss"

    try:
        formatted_datetime = babel.dates.format_datetime(datetime, format_string,
                                                         locale=(frappe.local.lang or "").replace("-", "_"))
    except UnknownLocaleError:
        formatted_datetime = datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_datetime


def get_number_format_info(format):
    return number_format_info.get(format) or (".", ",", 2)


def fmt_money(amount, precision=None, currency=None):
    """
    Convert to string with commas for thousands, millions etc
    """
    number_format = frappe.db.get_default("number_format") or "#,###.##"
    if precision is None:
        precision = cint(frappe.db.get_default('currency_precision')) or None

    decimal_str, comma_str, number_format_precision = get_number_format_info(number_format)

    if precision is None:
        precision = number_format_precision

    # 40,000 -> 40,000.00
    # 40,000.00000 -> 40,000.00
    # 40,000.23000 -> 40,000.23

    if isinstance(amount, string_types):
        amount = flt(amount, precision)

    if decimal_str:
        decimals_after = str(round(amount % 1, precision))
        parts = decimals_after.split('.')
        parts = parts[1] if len(parts) > 1 else parts[0]
        decimals = parts
        if precision > 2:
            if len(decimals) < 3:
                if currency:
                    fraction = frappe.db.get_value("Currency", currency, "fraction_units", cache=True) or 100
                    precision = len(cstr(fraction)) - 1
                else:
                    precision = number_format_precision
            elif len(decimals) < precision:
                precision = len(decimals)

    amount = '%.*f' % (precision, round(flt(amount), precision))

    if amount.find('.') == -1:
        decimals = ''
    else:
        decimals = amount.split('.')[1]

    parts = []
    minus = ''
    if flt(amount) < 0:
        minus = '-'

    amount = cstr(abs(flt(amount))).split('.')[0]

    if len(amount) > 3:
        parts.append(amount[-3:])
        amount = amount[:-3]

        val = number_format == "#,##,###.##" and 2 or 3

        while len(amount) > val:
            parts.append(amount[-val:])
            amount = amount[:-val]

    parts.append(amount)

    parts.reverse()

    amount = comma_str.join(parts) + ((precision and decimal_str) and (decimal_str + decimals) or "")
    if amount != '0':
        amount = minus + amount

    if currency and frappe.get_global_default("hide_currency_symbol") != "Yes":
        symbol = frappe.db.get_value("Currency", currency, "symbol", cache=True) or currency
        amount = symbol + " " + amount

    return amount


# datetime functions
def formatdate(string_date=None, format_string=None):
    """
        Converts the given string date to :data:`user_format`
        User format specified in defaults

         Examples:

         * dd-mm-yyyy
         * mm-dd-yyyy
         * dd/mm/yyyy
    """

    if not string_date:
        return ''

    date = getdate(string_date)
    if not format_string:
        format_string = get_user_format()
    format_string = format_string.replace("mm", "MM")
    try:
        formatted_date = babel.dates.format_date(date, format_string,
                                                 locale=(frappe.local.lang or "").replace("-", "_"))
    except UnknownLocaleError:
        format_string = format_string.replace("MM", "%m").replace("dd", "%d").replace("yyyy", "%Y")
        formatted_date = date.strftime(format_string)
    return formatted_date


def get_user_format():
    if getattr(frappe.local, "user_format", None) is None:
        frappe.local.user_format = frappe.db.get_default("date_format")

    return frappe.local.user_format or "yyyy-mm-dd"


def nowdate():
    """return current date as yyyy-mm-dd"""
    return now_datetime().strftime(DATE_FORMAT)


def nowtime():
    """return current time in hh:mm"""
    return now_datetime().strftime(TIME_FORMAT)


def add_to_date(date, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, as_string=False,
                as_datetime=False):
    """Adds `days` to the given date"""
    from dateutil.relativedelta import relativedelta

    if date == None:
        date = now_datetime()

    if hours:
        as_datetime = True

    if isinstance(date, string_types):
        as_string = True
        if " " in date:
            as_datetime = True
        date = parser.parse(date)

    date = date + relativedelta(years=years, months=months, weeks=weeks, days=days, hours=hours, minutes=minutes,
                                seconds=seconds)

    if as_string:
        if as_datetime:
            return date.strftime(DATETIME_FORMAT)
        else:
            return date.strftime(DATE_FORMAT)
    else:
        return date


def get_time(time_str):
    if isinstance(time_str, datetime.datetime):
        return time_str.time()
    elif isinstance(time_str, datetime.time):
        return time_str
    else:
        if isinstance(time_str, datetime.timedelta):
            time_str = str(time_str)
        return parser.parse(time_str).time()


def to_timedelta(time_str):
    if isinstance(time_str, string_types):
        t = parser.parse(time_str)
        return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

    else:
        return time_str


def getdate(string_date=None):
    """
    Converts string date (yyyy-mm-dd) to datetime.date object
    """

    if not string_date:
        return get_datetime().date()
    if isinstance(string_date, datetime.datetime):
        return string_date.date()

    elif isinstance(string_date, datetime.date):
        return string_date

    # dateutil parser does not agree with dates like 0001-01-01
    if not string_date or string_date == "0001-01-01":
        return None
    return parser.parse(string_date).date()


def get_datetime(datetime_str=None):
    if not datetime_str or datetime_str == "0000-00-00 00:00:00.000000":
        return now_datetime()

    if isinstance(datetime_str, (datetime.datetime, datetime.timedelta)):
        return datetime_str

    elif isinstance(datetime_str, (list, tuple)):
        return datetime.datetime(datetime_str)

    elif isinstance(datetime_str, datetime.date):
        return datetime.datetime.combine(datetime_str, datetime.time())

    # dateutil parser does not agree with dates like 0001-01-01
    if not datetime_str or (datetime_str or "").startswith("0001-01-01"):
        return None

    try:
        return datetime.datetime.strptime(datetime_str, DATETIME_FORMAT)
    except ValueError:
        return parser.parse(datetime_str)


def now():
    """return current datetime as yyyy-mm-dd hh:mm:ss"""
    if frappe.flags.current_date:
        return getdate(frappe.flags.current_date).strftime(DATE_FORMAT) + " " + \
               now_datetime().strftime(TIME_FORMAT)
    else:
        return now_datetime().strftime(DATETIME_FORMAT)


def now_datetime():
    dt = convert_utc_to_user_timezone(datetime.datetime.utcnow())
    return dt.replace(tzinfo=None)


def _get_time_zone():
    return frappe.db.get_system_setting('time_zone') or 'Asia/Kolkata'  # Default to India ?!


def get_time_zone():
    if frappe.local.flags.in_test:
        return _get_time_zone()

    return frappe.cache().get_value("time_zone", _get_time_zone)


def convert_utc_to_user_timezone(utc_timestamp):
    from pytz import timezone, UnknownTimeZoneError
    utcnow = timezone('UTC').localize(utc_timestamp)
    try:
        return utcnow.astimezone(timezone(get_time_zone()))
    except UnknownTimeZoneError:
        return utcnow


def encode(obj, encoding="utf-8"):
    # if isinstance(obj, list):
    #     out = []
    #     for o in obj:
    #         if isinstance(o, text_type):
    #             out.append(o.encode(encoding))
    #         else:
    #             out.append(o)
    #     return out
    # elif isinstance(obj, text_type):
    #     return obj.encode(encoding)
    # else:
    return obj


def log(method, message=None):
    """log error in patch_log"""
    message = frappe.utils.cstr(message) + "\n" if message else ""
    message += frappe.get_traceback()

    if not (frappe.db and frappe.db._conn):
        frappe.connect()

    frappe.db.rollback()
    frappe.db.begin()

    d = frappe.new_doc("Error Log")
    d.method = method
    d.error = message
    d.insert(ignore_permissions=True)

    frappe.db.commit()

    return message
