# pylint: disable=bare-except
# pylint: disable=consider-using-enumerate
# pylint: disable=len-as-condition
# pylint: disable=protected-access
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=unidiomatic-typecheck
# pylint: disable=bare-except

import datetime
import json
import math
import os
import random
import string
import unittest

from okera import context, _thrift_api
from okera._thrift_api import TTypeId, TConfigType

DEFAULT_PRESTO_HOST = 'localhost'
DEFAULT_PRESTO_PORT = 8049

TEST_LEVEL = 'smoke'
if 'TEST_LEVEL' in os.environ:
    TEST_LEVEL = os.environ['TEST_LEVEL']
ROOT_TOKEN = os.environ['OKERA_HOME'] + '/integration/tokens/cerebro.token'

identity = lambda x: x

def get_env_var(name, coercer, default):
    if name in os.environ:
        return coercer(os.environ[name])
    return default

def get_bool_env_var(name, default):
    return get_env_var(name, lambda x: str(x).lower() in ['true'], default)

def get_test_context(auth_mech=None):
    if auth_mech is None:
        auth_mech = get_env_var('PYCEREBRO_TEST_AUTH_MECH', identity, 'NOSASL')

    ctx = context()
    if auth_mech == 'NOSASL':
        ctx.disable_auth()
    elif auth_mech == 'TOKEN':
        ctx.enable_token_auth(token_file=ROOT_TOKEN)
    else:
        ctx.disable_auth()
    return ctx

def get_planner(host=None, port=None, dialect='okera'):
    if host is not None:
        host = host
    else:
        host = get_env_var('PYCEREBRO_TEST_HOST', identity, 'localhost')

    if port is not None:
        port = port
    else:
        port = get_env_var('PYCEREBRO_TEST_PLANNER_PORT', int, 12050)
    if 'presto' in dialect:
        ctx = get_test_context()
        ctx.enable_token_auth(token_str='root')
        return ctx.connect(host=host,
                           port=port,
                           presto_host=host,
                           presto_port=DEFAULT_PRESTO_PORT)
    return get_test_context().connect(host=host, port=port)

def get_worker(host=None, port=None):
    if host is not None:
        host = host
    else:
        host = get_env_var('PYCEREBRO_TEST_HOST', identity, 'localhost')

    if port is not None:
        port = port
    else:
        port = get_env_var('PYCEREBRO_TEST_WORKER_PORT', int, 13050)

    return get_test_context().connect_worker(host=host, port=port)

def configure_botocore_patch():
    os.environ['OKERA_PATCH_BOTO'] = 'True'
    os.environ['OKERA_PLANNER_HOST'] = 'localhost'
    with open(ROOT_TOKEN, 'r') as token_file:
        os.environ['OKERA_USER_TOKEN'] = token_file.read().strip(' \t\n\r')
    from okera import initialize_default_context, check_and_patch_botocore
    initialize_default_context()
    check_and_patch_botocore()

def upsert_config(conn, config_type, key, value):
    """Upsert a configuration.

    config_type : TConfigType
        The type of configurations to return.
    key : str
        The key for this configuration. This must be unique with config_type.
    value : str
        The value for this config.

    Returns
    -------
    bool
        Returns true if the config was updated or false if it was inserted.
    list(str), optional
        List of warnings that were generated as part of this request.
    """
    request = _thrift_api.TConfigUpsertParams()
    request.config_type = config_type
    request.key = key
    if isinstance(value, str):
        request.params = {'value': value}
    else:
        request.params = value
    result = conn.service.client.UpsertConfig(request)
    # TODO: server needs to return if it was an upsert or not
    return True, result.warnings

def delete_config(conn, config_type, key):
    """Upsert a configuration.

    config_type : TConfigType
        The type of configurations to return.
    key : str
        The key for this configuration. This must be unique with config_type.

    Returns
    -------
    bool
        Returns true if the config was deleted.
    list(str), optional
        List of warnings that were generated as part of this request.
    """
    request = _thrift_api.TConfigDeleteParams()
    request.config_type = config_type
    request.key = key
    result = conn.service.client.DeleteConfig(request)
    # TODO: server needs to return if it was deleted or not
    return True, result.warnings

def list_configs(conn, config_type):
    """List configurations of the specified type.

    config_type : TConfigType
        The type of configurations to return.

    Returns
    -------
    map(str, str)
        List of configs as a map of key values.
    """
    table_name = None
    if config_type == TConfigType.AUTOTAGGER_REGEX:
        table_name = "okera_system.tagging_rules"
    elif config_type == TConfigType.SYSTEM_CONFIG:
        table_name = "okera_system.configs"
    else:
        raise ValueError("Invalid config type.")
    return conn.scan_as_json(table_name)

class JsonGeneratorNode():
    def __init__(self):
        self.types = []
        self.children = {}

    def to_json(self):
        result = {}
        result['types'] = []
        for t in self.types:
            result['types'].append(TTypeId._VALUES_TO_NAMES[t])
        result['types'] = ', '.join(result['types'])
        if not self.children:
            return result
        for name, child in self.children.items():
            result[name] = child.to_json()
        return result

class JsonGenerator():
    def __init__(self,
                 types=None,
                 record_probabilities=None,
                 array_probabilties=None,
                 null_probability=.1,
                 empty_record_probability=.1,
                 min_fields=1,
                 max_fields=5,
                 max_array_len=3,
                 min_records=2,
                 max_records=10,
                 max_string_len=20,
                 seed=0,
                 max_recursion=5,
                 missing_fields_probability=0,
                 generate_variadic_schema=False,
                 generate_empty_record_all_types=False):
        random.seed(seed)
        if not types:
            types = [[TTypeId.BOOLEAN],
                     [TTypeId.BIGINT],
                     [TTypeId.DOUBLE],
                     [TTypeId.DATE],
                     [TTypeId.TIMESTAMP_NANOS],
                     [TTypeId.STRING]]
            if generate_variadic_schema:
                # This indicates that if this "type" is selected in the schema, the
                # data will be one of these types
                types.append([TTypeId.BIGINT, TTypeId.DOUBLE])
                types.append([TTypeId.BIGINT, TTypeId.DATE])
                types.append([TTypeId.DOUBLE, TTypeId.BOOLEAN])
                types.append([TTypeId.DATE, TTypeId.TIMESTAMP_NANOS])
                types.append([TTypeId.BOOLEAN, TTypeId.BIGINT, TTypeId.DATE,
                              TTypeId.TIMESTAMP_NANOS, TTypeId.DOUBLE, TTypeId.STRING])

        # Probabilities of generating record/array schemas by level. We want to
        # generate them with higher probabilities at the beginning to minimize
        # generating a lot of simple schemas.
        # This generate a CDF (i.e the remaining percentage is used to generate a
        # simple type).
        if not record_probabilities:
            record_probabilities = [.5, .4, .3, .25, .25, .2, .1]
        if not array_probabilties:
            array_probabilities = [.3, .3, .3, .25, .25, .2, .1]

        self.__min_fields = min_fields
        self.__max_fields = max_fields
        self.__min_records = min_records
        self.__max_records = max_records
        self.__max_array_len = max_array_len
        self.__null_probability = null_probability
        self.__max_string_len = max_string_len
        self.__empty_record_probability = empty_record_probability
        self.__max_recursion = max_recursion
        self.__types = types
        self.__array_probabilities = array_probabilities
        self.__record_probabilities = record_probabilities

        # Configs to control schema merge cases
        self.__generate_invalid_schema_merges = False
        self.__generate_empty_record_all_types = generate_empty_record_all_types
        self.__missing_fields_probability = missing_fields_probability

        self.__field_idx = 0
        self.__schema = None

        print("Generating with configuration")
        print("    Seed:  %s" % seed)
        print("    Types:  %s" % self.__types)
        print("    Record Probabilities:  %s" % self.__record_probabilities)
        print("    Array Probabilities:  %s" % self.__array_probabilities)
        print("    Max Array Len: %d" % (self.__max_array_len))
        print("    Max String Len: %d" % (self.__max_string_len))
        print("    Null Probability: %s" % (self.__null_probability))
        print("    Empty Record Probability: %s" % (self.__empty_record_probability))
        print("    Missing Field Probability: %s" % (self.__missing_fields_probability))
        print("    Max Depth: %d" % (self.__max_recursion))
        print("    # Fields: [%d, %d]" % (self.__min_fields, self.__max_fields))
        print("    # Records: [%d, %d]" % (self.__min_records, self.__max_records))
        print("    Generate variadic schemas: %s" % generate_variadic_schema)
        print("    Generate invalid merges: %s" %\
            self.__generate_invalid_schema_merges)
        print("    Generate empty records all types: %s" %\
            self.__generate_empty_record_all_types)

    def new_schema(self):
        self.__field_idx = 0
        self.__schema = self._generate_schema([TTypeId.RECORD], 0)

    def _random_type(self, level):
        prob_record = self.__record_probabilities[\
            min(level, len(self.__record_probabilities) - 1)]
        prob_array = self.__array_probabilities[\
            min(level, len(self.__array_probabilities) - 1)]
        r = random.random()
        if r < prob_record:
            return [TTypeId.RECORD]
        if r < prob_record + prob_array:
            return [TTypeId.ARRAY]
        return random.choice(self.__types)

    def _generate_schema(self, types, level):
        # Recursively generates a test schema
        node = JsonGeneratorNode()
        if level == self.__max_recursion:
            node.types = [TTypeId.STRING]
            return node

        node.types = types
        if types == [TTypeId.RECORD]:
            num_fields = random.randint(self.__min_fields, self.__max_fields - 1)
            for idx in range(0, num_fields):
                t = self._random_type(level)
                if level == 0:
                    name = 'c' + str(idx)
                else:
                    name = 'f' + str(self.__field_idx)
                    self.__field_idx += 1
                node.children[name] = self._generate_schema(t, level + 1)
        elif types == [TTypeId.ARRAY]:
            t = self._random_type(level)
            node.children['item'] = self._generate_schema(t, level + 1)
        return node

    def __generate_random_data(self, schema):
        if random.random() < self.__null_probability:
            return None
        t = random.choice(schema.types)
        if self.__generate_empty_record_all_types or t == TTypeId.RECORD:
            if random.random() < self.__empty_record_probability:
                return {}

        if t == TTypeId.BIGINT:
            digits = random.random() * 10
            v = int(pow(10, digits) * random.random())
            if random.random() < .1:
                return -v
            return v
        if t == TTypeId.DOUBLE:
            digits = random.random() * 10
            v = pow(10, digits) * random.random()
            if random.random() < .1:
                return -v
            return v
        if t == TTypeId.BOOLEAN:
            if random.random() > 0.5:
                return True
            return False
        if t == TTypeId.DATE:
            return '2020-01-01'
        if t == TTypeId.TIMESTAMP_NANOS:
            return '2020-01-01 01:02:03.123'
        if t == TTypeId.STRING:
            n = random.randint(0, self.__max_string_len - 1)
            return ''.join(random.choice(string.ascii_lowercase) for i in range(n))
        if t == TTypeId.RECORD:
            return self.__generate_record(schema)
        if t == TTypeId.ARRAY:
            return self.__generate_array(schema.children['item'])
        return 'Unsupported Type %s' % t

    def __generate_array(self, schema):
        result = []
        num_children = random.randint(0, self.__max_array_len - 1)
        for _ in range(0, num_children):
            result.append(self.__generate_random_data(schema))
        return result

    def __generate_record(self, schema):
        record = {}
        for name, child in schema.children.items():
            if random.random() < self.__missing_fields_probability:
                continue
            record[name] = self.__generate_random_data(child)
        return record

    def generate(self, generate_record_idx=False):
        n = self.__min_records
        if self.__min_records != self.__max_records:
            n = random.randint(self.__min_records, self.__max_records - 1)
        data = []
        for idx in range(0, n):
            r = self.__generate_record(self.__schema)
            if generate_record_idx:
                r['idx'] = idx
            data.append(r)
        return data

class TestBase(unittest.TestCase):
    """ Base class with some common test utilities. """
    @staticmethod
    def _ddl_count(conn, sql):
        return len(conn.execute_ddl(sql))

    @staticmethod
    def _visible_cols(cols):
        result = []
        for c in cols:
            if c.hidden:
                continue
            result.append(c)
        return result

    @staticmethod
    def _top_level_columns(cols):
        total_children = 0
        for c in cols:
            if c.type.num_children:
                total_children += c.type.num_children
        return len(cols) - total_children

    @staticmethod
    def _try_parse_datetime(v):
        if not isinstance(v, str):
            return None

        FORMATS = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
        ]

        for fmt in FORMATS:
            try:
                return datetime.datetime.strptime(v, fmt)
            except ValueError:
                pass
        return None

    @staticmethod
    def _is_float(v):
        if v is None:
            return False
        try:
            float(v)
            return True
        except:
            return False

    def _equals(self, v1, v2):
        if self._is_float(v1) and self._is_float(v2):
            v1 = float(v1)
            v2 = float(v2)

        if isinstance(v1, float) and isinstance(v2, float):
            return v1 == v2 or (math.isnan(v1) and math.isnan(v2)) \
                or abs(v1 - v2) < .00001
        if v1 != v2:
            # Try as datetime with different formats
            d1 = TestBase._try_parse_datetime(v1)
            d2 = TestBase._try_parse_datetime(v2)
            if d1 is not None and d1 == d2:
                return True
            print("Values do not match. %s != %s" % (v1, v2))
            print("Types: %s != %s" % (type(v1), type(v2)))
        return v1 == v2

    def _is_empty_dictionary(self, v):
        """ Checks if v is None or a dictionary (recursively) of None values """
        if v is None:
            return True
        if type(v) != dict:
            return False
        for _, val in v.items():
            if not self._is_empty_dictionary(val):
                return False
        return True

    def __deep_compare(self, actual, expected, allow_missing, empty_struct_equals_null,
                       required_type):
        if empty_struct_equals_null:
            if type(actual) == dict and (expected is None or len(expected) == 0):
                # We don't support nullable structs, so instead every field in the
                # struct is None
                for k, v in actual.items():
                    if not self._is_empty_dictionary(v):
                        print("actual has a non-null struct. Expecting null.")
                        return False
                return True
            if type(expected) == dict and len(expected) == 0 and actual is None:
                # Allow empty struct to be considered equal to null. A struct with no
                # fields is otherwise not possible.
                return True

        # As we are strongly typed, we will convert the types to the "bigger" type for
        # schema merge cases.
        if type(actual) == str and type(expected) in [int, float]:
            expected = str(expected)
        if type(actual) == str and type(expected) == bool:
            if expected:
                expected = "true"
            else:
                expected = "false"
        if type(actual) == float and type(expected) == int:
            expected = float(expected)

        if type(actual) != type(expected):
            if type(actual) == list and type(expected) == dict:
                # Can't tell difference between empty list and empty dict
                if not actual and not expected:
                    return True
            # Handle some schema merge cases that are ambiguous with empty records
            if type(actual) == dict and not actual and \
                    type(expected) in [bool, float, int]:
                return True
            if type(actual) in [bool, float, int] and type(expected) == dict \
                    and not expected:
                return True
            if required_type and type(expected) in [bool, float, int, str]:
                if type(expected) != required_type:
                    # The required type doesn't match so the expected should be None
                    if actual is not None and \
                            not self._equals(actual, required_type(expected)):
                        print("Expecting actual to be None. %s, %s" % (actual, expected))
                        return False
                    return True
            print("Types don't match %s != %s" % (type(actual), type(expected)))
            print("%s != %s" % (actual, expected))
            return False

        if type(actual) == dict:
            for k, v in actual.items():
                # Handle the case where some field that exists in the Okera version
                # but is null might not exist in the raw file version, but only if
                # allow_missing is set
                if k in expected:
                    if not self.__deep_compare(v, expected[k], allow_missing,
                                               empty_struct_equals_null, required_type):
                        print("Key %s from expected is not in actual." % k)
                        print("%s != %s" % (v, expected[k]))
                        return False
                elif k not in expected and not \
                        (self._is_empty_dictionary(v) and allow_missing):
                    print("Key %s from actual is not in expected." % k)
                    return False
            for k, v in expected.items():
                if k not in actual:
                    print("Key %s from expected is not in actual." % k)
                    return False
        elif type(actual) == list:
            if len(actual) != len(expected):
                print("Length of arrays are not equal. %s != %s" % \
                      (len(actual), len(expected)))
                return False
            for idx in range(len(actual)):
                if not self.__deep_compare(actual[idx], expected[idx], allow_missing,
                                           empty_struct_equals_null, required_type):
                    print("List elements don't match at idx %s. %s != %s" % \
                          (idx, actual[idx], expected[idx]))
                    return False
        else:
            return self._equals(actual, expected)

        return True

    def _lower_keys(self, x):
        if isinstance(x, list):
            return [self._lower_keys(v) for v in x]
        if isinstance(x, dict):
            return dict((k.lower(), self._lower_keys(v)) for k, v in x.items())
        return x

    def compare_json(self, actual, expected, allow_missing, empty_struct_equals_null,
                     batch_mode, required_type):
        actual = self._lower_keys(actual)
        expected = self._lower_keys(expected)

        if batch_mode and len(actual) != len(expected):
            print("Failure: Lengths did not match %s != %s" % \
                (len(actual), len(expected)))
            return False
        self.assertEqual(len(actual), len(expected))

        for idx in range(len(actual)):
            obj1 = actual[idx]
            obj2 = expected[idx]

            if self.__deep_compare(obj1, obj2, allow_missing, empty_struct_equals_null,
                                   required_type):
                continue
            if batch_mode:
                return False
            print("EXPECTED:\n%s" % json.dumps(expected, indent=2, sort_keys=True))
            print("\nACTUAL:\n%s" % json.dumps(actual, indent=2, sort_keys=True))
            self.assertEqual(json.dumps(actual, indent=2, sort_keys=True),
                             json.dumps(expected, indent=2, sort_keys=True))
        return True
