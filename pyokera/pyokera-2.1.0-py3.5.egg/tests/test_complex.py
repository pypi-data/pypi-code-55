# Copyright 2019 Okera Inc. All Rights Reserved.
#
# Some integration tests for auth in PyOkera
#
# pylint: disable=global-statement
# pylint: disable=no-self-use
# pylint: disable=no-else-return


import datetime
import json
import warnings

import pytest
import numpy

import requests

from okera import context
from okera._thrift_api import TRecordServiceException

API_URL = "http://localhost:5000"

def get_scan_as_json(conn, dataset):
    data = conn.scan_as_json(
        dataset, strings_as_utf8=True,
        max_records=10, max_client_process_count=1)
    return data

def get_scan_as_pandas(conn, dataset):
    def convert_types(datum):
        if isinstance(datum, datetime.datetime):
            return datum.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        elif isinstance(datum, numpy.int64):
            return int(datum)
        elif isinstance(datum, dict):
            for key, value in datum.items():
                datum[key] = convert_types(value)
            return datum
        elif isinstance(datum, list):
            return [convert_types(child) for child in datum]

        return datum

    data = conn.scan_as_pandas(
        dataset, strings_as_utf8=True,
        max_records=10, max_client_process_count=1)
    data = data.replace({numpy.nan: None})
    data = data.to_dict('records')
    return convert_types(data)

def get_scan_from_rest(dataset):
    headers = {'content-type': 'application/json'}
    query = {'query': 'SELECT * FROM %s' % dataset}
    response = requests.post(
        API_URL + '/api/scan?records=10',
        json=query, headers=headers)
    result = json.loads(response.text)
    return result

def format(data):
    return json.dumps(data, sort_keys=True, indent=1)

@pytest.mark.parametrize("dataset", [
    'rs_complex.array_struct_array',
    'rs_complex.array_struct_t',
    'rs_complex.array_t',
    'rs_complex.avrotbl',
    'rs_complex.bytes_type',
    'rs_complex.bytes_type_file',
    'rs_complex.enum_type',
    'rs_complex.enum_type_default',
    'rs_complex.map_t',
    'rs_complex.market_decide_single_avro',
    'rs_complex.market_v20_single',
    'rs_complex.market_v30_single',
    'rs_complex.multiple_structs_nested',
    'rs_complex.strarray_t',
    'rs_complex.strarray_t_view',
    'rs_complex.struct_array_struct',
    'rs_complex.struct_nested',
    'rs_complex.struct_nested_s1',
    'rs_complex.struct_nested_s1_f1',
    'rs_complex.struct_nested_s1_s2',
    'rs_complex.struct_nested_view',
    'rs_complex.struct_t',
    'rs_complex.struct_t2',
    'rs_complex.struct_t3',
    'rs_complex.struct_t_id',
    'rs_complex.struct_t_s1',
    'rs_complex.struct_t_view',
    'rs_complex.struct_t_view2',
    'rs_complex.user_phone_numbers',
    'rs_complex.user_phone_numbers_map',
    'rs_complex.users',
    'rs_complex.view_over_multiple_structs',
    'rs_complex_parquet.array_struct_array',
    'rs_complex_parquet.array_struct_map_t',
    'rs_complex_parquet.array_struct_t',
    'rs_complex_parquet.array_struct_t2',
    'rs_complex_parquet.array_t',
    'rs_complex_parquet.bytes_type',
    'rs_complex_parquet.enum_type',
    'rs_complex_parquet.map_array',
    'rs_complex_parquet.map_array_t2',
    'rs_complex_parquet.map_struct_array_t',
    'rs_complex_parquet.map_struct_array_t_view',
    'rs_complex_parquet.map_struct_t',
    'rs_complex_parquet.map_struct_t_view',
    'rs_complex_parquet.map_t',
    'rs_complex_parquet.strarray_t',
    'rs_complex_parquet.struct_array_struct',
    'rs_complex_parquet.struct_nested',
    'rs_complex_parquet.struct_nested_s1',
    'rs_complex_parquet.struct_nested_s1_f1',
    'rs_complex_parquet.struct_nested_s1_s2',
    'rs_complex_parquet.struct_nested_view',
    'rs_complex_parquet.struct_t',
    'rs_complex_parquet.struct_t2',
    'rs_complex_parquet.struct_t3',
    'rs_complex_parquet.struct_t_id',
    'rs_complex_parquet.struct_t_s1',
    'rs_complex_parquet.struct_t_view',
    'rs_complex_parquet.struct_t_view2',
    # # The ones below don't work because the /scan API returns the wrong value
    # # for decimals
    # 'rs_complex_parquet.spark_all_mixed_compression',
    # 'rs_complex_parquet.spark_gzip',
    # 'rs_complex_parquet.spark_snappy',
    # 'rs_complex_parquet.spark_snappy_part',
    # 'rs_complex_parquet.spark_uncompressed',
    # 'rs_complex_parquet.spark_uncompressed_legacy_format',
    'customer.zd277_complex',
    'rs_json_format.complex_c1_case_sensitive',
    'rs_json_format.complex_c1_usecase',
    'rs_json_format.complex_nike_usecase',
    # NOT WORKING array of arrays is not allowed, scan error
    # 'rs_json_format.json_array_arrays',
    'rs_json_format.json_array_struct',
    'rs_json_format.json_arrays_test',
    # # These tables don't work because Pandas and JSON don't serialize to the
    # # exact same types (e.g. float vs int), even though the overall data is correct)
    # 'rs_json_format.json_inferred',
    # 'rs_json_format.json_primitives',
    # 'rs_json_format.json_primitives_inferred',
    'rs_json_format.json_struct',
    'rs_json_format.json_struct_array',
    'rs_json_format.json_struct_nested',
    'rs_json_format.primitives_with_array',
])

def test_basic(dataset):
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        json_data = get_scan_as_json(conn, dataset)
        pandas_data = get_scan_as_pandas(conn, dataset)
        rest_data = get_scan_from_rest(dataset)
        assert format(json_data) == format(pandas_data)
        assert format(json_data) == format(rest_data)

def test_pandas_empty_result():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        pandas_data = conn.scan_as_pandas('select s1 from rs_complex.struct_t where 1=0')
        columns = list(pandas_data.columns)
        assert columns == ['s1']

        pandas_data = conn.scan_as_pandas(
            'select a1 from rs_complex.array_struct_array where 1=0')
        columns = list(pandas_data.columns)
        assert columns == ['a1']

        pandas_data = conn.scan_as_pandas(
            'select s1, s1.a1 as x from rs_complex.struct_array_struct where 1=0')
        columns = list(pandas_data.columns)
        assert columns == ['s1', 'x']

        pandas_data = conn.scan_as_pandas(
            'select * from rs_complex_parquet.map_struct_array_t where 1=0')
        columns = list(pandas_data.columns)
        assert columns == ['id', 'str_arr', 'struct_map']

def test_json_nonutf8():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        data = conn.scan_as_json(
            'select * from rs.encoding',
            strings_as_utf8=False)
        assert data == [{'uid': b'ABC123', 'message': b'\xe8 bene'}]

def test_null_map():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        json_data = get_scan_as_json(conn, 'fastparquet.map_array_parq')
        pandas_data = get_scan_as_pandas(conn, 'fastparquet.map_array_parq')
        assert format(json_data) == format(pandas_data)

def assert_scan_output(qry, expected, is_scan=True):
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        if is_scan:
            data = conn.scan_as_json(qry, strings_as_utf8=False)
        else:
            data = conn.execute_ddl(qry)
        print(data)
        print(expected)
        assert data == expected

def assert_scan_exception(qry, expected, is_scan=True):
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    ctx = context()
    with ctx.connect(host='localhost', port=12050) as conn:
        try:
            if is_scan:
                result = conn.scan_as_json(qry, strings_as_utf8=False)
            else:
                result = conn.execute_ddl(qry)
            assert result
        except TRecordServiceException as ex:
            assert expected in str(ex.detail)

def test_unnest():
    assert_scan_output(
        'select id, str_arr.item from ' +\
        'rs_complex.strarray_t, rs_complex.strarray_t.str_arr',
        [{'id': 456, 'item': b'a'}, {'id': 456, 'item': b'b'},
         {'id': 457, 'item': b'cde'}, {'id': 457, 'item': b''},
         {'id': 458, 'item': b'fg'},
         {'id': 458, 'item': b'ijlk'}])

    assert_scan_output(
        'select id, str_arr.item item from ' +\
        'rs_complex.strarray_t, rs_complex.strarray_t.str_arr where id = 456',
        [{'id': 456, 'item': b'a'}, {'id': 456, 'item': b'b'}])

    assert_scan_output(
        'select a1.item, mask(a1.item.f1) from ' +\
        'rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'item': {'f2': b'c', 'f1': b'ab'}, 'mask(a1': {'item': {'f1)': b'XX'}}},
         {'item': {'f2': b'', 'f1': b'def'}, 'mask(a1': {'item': {'f1)': b'XXX'}}},
         {'item': {'f2': b'ij', 'f1': b'g'}, 'mask(a1': {'item': {'f1)': b'X'}}}])

    assert_scan_output(
        'select a1.f1 as raw_f1, ' +\
        'concat(a1.f1, \'_f1\') as concat_f1, a1.f2, ' +\
        'concat(a1.f2, \'_f2\') as concat_f2 ' +\
        'from rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'f2': b'c', 'concat_f2': b'c_f2', 'concat_f1': b'ab_f1', 'raw_f1': b'ab'},
         {'f2': b'', 'concat_f2': b'_f2', 'concat_f1': b'def_f1', 'raw_f1': b'def'},
         {'f2': b'ij', 'concat_f2': b'ij_f2', 'concat_f1': b'g_f1', 'raw_f1': b'g'}])

    assert_scan_output(
        'select a1.f2, mask(a1.f1) from ' +\
        'rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'mask(a1': {'f1)': b'XX'}, 'f2': b'c'},
         {'mask(a1': {'f1)': b'XXX'}, 'f2': b''},
         {'mask(a1': {'f1)': b'X'}, 'f2': b'ij'}])

    assert_scan_exception(
        'select unnest_alias, mask(unnest_alias.f1) ' +\
        'from rs_complex.array_struct_t, ' +\
        'rs_complex.array_struct_t.a1 unnest_alias',
        "AnalysisException: Cannot specify alias 'unnest_alias' " \
        "for collection reference in the from clause.")

    assert_scan_exception(
        'select id, str_arr.item from ' +\
        'rs_complex.strarray_t, rs_complex.strarray_t.str_arr ' +\
        'where str_arr.item = \'cde\'',
        'Predicates on collection types are not yet supported. str_arr.item')

    assert_scan_exception(
        'SELECT `subscription_key_tokenized` ' \
        'FROM chase.subscription_party_view ' \
        'WHERE CAST(`partyrole_updatedDate` AS STRING) = "NOT A VALUE TEST" ',
        'AnalysisException: Predicates on collection types are not yet supported.')

    assert_scan_exception(
        'SELECT `subscription_key_tokenized` FROM chase.subscription_party_view ' \
        'WHERE partyRoleKey IS NULL ',
        'AnalysisException: Predicates on collection types are not yet supported.',
        False
    )

    assert_scan_exception(
        'select tokenize(partyroles.item.partykey) as tokenized_key ' +\
        'from chase.zd1238_4.partyroles ',
        "AnalysisException: Correlated table 'chase.zd1238_4' must " \
        "be specified before the collection reference " \
        "'chase.zd1238_4.partyroles' in the from clause")

    # TODO: Make execddl return the raw output for explain plan, then enable this.
    # assert_scan_output(
    #     'EXPLAIN SELECT subscription_key_tokenized FROM chase.subscription_party_view',
    #     '00:SCAN HDFS [chase.zd1238_4] '\
    #     '    partitions=1/1 files=1 size=54.05KB '\
    #     '    predicates: !empty(chase.zd1238_4.partyroles)',
    #     False
    # )

    assert_scan_output(
        'select a1.* from rs_complex.array_struct_t, ' +\
        'rs_complex.array_struct_t.a1',
        [{'f2': b'c', 'f1': b'ab'},
         {'f2': b'', 'f1': b'def'},
         {'f2': b'ij', 'f1': b'g'}])

    assert_scan_output(
        'select a1.item.* from rs_complex.array_struct_t, ' +\
        'rs_complex.array_struct_t.a1',
        [{'item': {'f2': b'c', 'f1': b'ab'}},
         {'item': {'f2': b'', 'f1': b'def'}},
         {'item': {'f2': b'ij', 'f1': b'g'}}])

    ## FIXME : Incorrect a1.f2 results in this output
    assert_scan_output(
        'select a1, mask(a1.f1) from ' +\
        'rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'mask(a1': {'f1)': b'XX'}, 'a1': [{'f1': b'ab', 'f2': None}]},
         {'mask(a1': {'f1)': b'XXX'}, 'a1': [{'f1': b'def', 'f2': None}]},
         {'mask(a1': {'f1)': b'X'}, 'a1': [{'f1': b'g', 'f2': None}]}])

    assert_scan_output(
        'select a1.* from rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'f1': b'ab', 'f2': b'c'},
         {'f1': b'def', 'f2': b''},
         {'f1': b'g', 'f2': b'ij'}])

    assert_scan_output(
        'select a1.item.a2 from rs_complex.array_struct_array, ' +\
        'rs_complex.array_struct_array.a1',
        [{'item': {'a2': [b'jk']}},
         {'item': {'a2': [b'l']}},
         {'item': {'a2': [b'']}}])

    assert_scan_output(
        'select a1.f2, mask(a1.f1) from ' +\
        'rs_complex.array_struct_t, rs_complex.array_struct_t.a1',
        [{'f2': b'c', 'mask(a1': {'f1)': b'XX'}},
         {'f2': b'', 'mask(a1': {'f1)': b'XXX'}},
         {'f2': b'ij', 'mask(a1': {'f1)': b'X'}}])

    ## Test on many Array types in same table.
    assert_scan_output(
        'select int32, int_arr, str_arr from ' +\
        'rs_complex_parquet.spark_snappy',
        [{'int_arr': [1, 2], 'int32': 1, 'str_arr': [b't1', b't2']},
         {'int_arr': [3, 4], 'int32': 2, 'str_arr': [b't3', b't4']}])

    assert_scan_output(
        'select int32, str_arr.item, int_arr from ' +\
        'rs_complex_parquet.spark_gzip, rs_complex_parquet.spark_gzip.str_arr',
        [{'item': b't1', 'int_arr': [1, 2], 'int32': 1},
         {'item': b't2', 'int_arr': [1, 2], 'int32': 1},
         {'item': b't3', 'int_arr': [3, 4], 'int32': 2},
         {'item': b't4', 'int_arr': [3, 4], 'int32': 2}])

    assert_scan_output(
        'select int32, int_arr.item, str_arr.item, ' +\
        'mask(str_arr.item) as str_masked from ' +\
        'rs_complex_parquet.spark_snappy, rs_complex_parquet.spark_snappy.str_arr ' +\
        ', rs_complex_parquet.spark_snappy.int_arr ',
        [{'item': 1, 'item_2': b't1', 'str_masked': b'XX', 'int32': 1},
         {'item': 2, 'item_2': b't1', 'str_masked': b'XX', 'int32': 1},
         {'item': 1, 'item_2': b't2', 'str_masked': b'XX', 'int32': 1},
         {'item': 2, 'item_2': b't2', 'str_masked': b'XX', 'int32': 1},
         {'item': 3, 'item_2': b't3', 'str_masked': b'XX', 'int32': 2},
         {'item': 4, 'item_2': b't3', 'str_masked': b'XX', 'int32': 2},
         {'item': 3, 'item_2': b't4', 'str_masked': b'XX', 'int32': 2},
         {'item': 4, 'item_2': b't4', 'str_masked': b'XX', 'int32': 2}])

    assert_scan_output(
        'select int32, inner_str_arr.item as srt_arr_str, ' +\
        'mask(inner_str_arr.item) as masked_srt_arr_str, ' +\
        'mask(struct_arr.item.inner_str) masked_struct_str ' +\
        'from rs_complex_parquet.spark_snappy, ' +\
        'rs_complex_parquet.spark_snappy.struct_t.inner_str_arr, ' +\
        'rs_complex_parquet.spark_snappy.struct_arr',
        [{'masked_srt_arr_str': b'XXX', 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In1'},
         {'masked_srt_arr_str': b'XXX', 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In1'},
         {'masked_srt_arr_str': b'XXX', 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In2'},
         {'masked_srt_arr_str': b'XXX', 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In2'},
         {'masked_srt_arr_str': b'XXX', 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In7'},
         {'masked_srt_arr_str': b'XXX', 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In7'},
         {'masked_srt_arr_str': b'XXX', 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In8'},
         {'masked_srt_arr_str': b'XXX', 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'srt_arr_str': b'In8'}])

    ## One test with array of int, string and struct<string>.
    ## we may not write many such tests as its too verbose output but this should
    ## be good coverage for flattened output.
    assert_scan_output(
        'select int32, int_arr.item as flat_int, mask(str_arr.item) as masked_str ' +\
        ',struct_arr.item.inner_str as raw_struct_str, ' +\
        'mask(struct_arr.item.inner_str) masked_struct_str ' +\
        'from rs_complex_parquet.spark_snappy, ' +\
        'rs_complex_parquet.spark_snappy.str_arr, ' +\
        'rs_complex_parquet.spark_snappy.int_arr, ' +\
        'rs_complex_parquet.spark_snappy.struct_arr',
        [{'masked_str': b'XX', 'flat_int': 1, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr2'},
         {'masked_str': b'XX', 'flat_int': 1, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr3'},
         {'masked_str': b'XX', 'flat_int': 2, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr2'},
         {'masked_str': b'XX', 'flat_int': 2, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr3'},
         {'masked_str': b'XX', 'flat_int': 1, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr2'},
         {'masked_str': b'XX', 'flat_int': 1, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr3'},
         {'masked_str': b'XX', 'flat_int': 2, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr2'},
         {'masked_str': b'XX', 'flat_int': 2, 'int32': 1,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr3'},
         {'masked_str': b'XX', 'flat_int': 3, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr5'},
         {'masked_str': b'XX', 'flat_int': 3, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr6'},
         {'masked_str': b'XX', 'flat_int': 4, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr5'},
         {'masked_str': b'XX', 'flat_int': 4, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr6'},
         {'masked_str': b'XX', 'flat_int': 3, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr5'},
         {'masked_str': b'XX', 'flat_int': 3, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr6'},
         {'masked_str': b'XX', 'flat_int': 4, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr5'},
         {'masked_str': b'XX', 'flat_int': 4, 'int32': 2,
          'masked_struct_str': b'XXXXXXXXX', 'raw_struct_str': b'InnerStr6'}])

    assert_scan_output(
        'select id, str_arr.item item from rs_complex.strarray_t, ' \
        'rs_complex.strarray_t.str_arr where id = 456',
        [{'item': b'a', 'id': 456}, {'item': b'b', 'id': 456}])

    assert_scan_exception(
        'select id, str_arr.item item from rs_complex.strarray_t.str_arr, ' \
        'rs_complex.strarray_t where id = 456',
        "Correlated table 'rs_complex.strarray_t' must be specified before " \
        "the collection reference 'rs_complex.strarray_t.str_arr' in the from clause ")

    assert_scan_output(
        'select int32, int_arr.item from rs_complex_parquet.spark_gzip, ' \
        'rs_complex_parquet.spark_gzip.int_arr',
        [{'int32': 1, 'item': 1}, {'int32': 1, 'item': 2},
         {'int32': 2, 'item': 3}, {'int32': 2, 'item': 4}]
    )

    assert_scan_output(
        'select int32, int_arr.item from rs_complex_parquet.spark_gzip, ' \
        'rs_complex_parquet.spark_gzip.int_arr',
        [{'int32': 1, 'item': 1}, {'int32': 1, 'item': 2},
         {'int32': 2, 'item': 3}, {'int32': 2, 'item': 4}]
    )

    assert_scan_output(
        'select * from rs_complex.pn_view',
        [{'uid': 123, 'item': b'111-222-3333'}, {'uid': 123, 'item': b'444-555-6666'},
         {'uid': 234, 'item': b'222-333-4444'}, {'uid': 234, 'item': b'555-666-7777'},
         {'uid': 345, 'item': b'111-222-5555'}]
    )

    assert_scan_output(
        'select count(*) as unnest_view_count from rs_complex.pn_view',
        [{'unnest_view_count': 5}]
    )

    assert_scan_output(
        'select count(*) as unnest_view_count from rs_complex.pn_view ' \
        'where uid = 234',
        [{'unnest_view_count': 2}]
    )

    ## Some GROUP BY/HAVING tests
    assert_scan_output(
        'select count(item) as item_count, uid from rs_complex.pn_view ' \
        'GROUP BY uid HAVING count(item) > 1 ',
        [{'item_count': 2, 'uid': 123}, {'item_count': 2, 'uid': 234}]
    )
    assert_scan_output(
        'select count(item) as item_count, uid from rs_complex.pn_view ' \
        'GROUP BY uid HAVING count(item) >= 1',
        [{'item_count': 1, 'uid': 345}, {'item_count': 2, 'uid': 123},
         {'item_count': 2, 'uid': 234}]
    )
    assert_scan_output(
        'select count(item) as item_count, uid from rs_complex.pn_view ' \
        'GROUP BY uid HAVING count(item) = 1',
        [{'item_count': 1, 'uid': 345}]
    )

# pylint: disable=bad-continuation
# pylint: disable=line-too-long
def test_array_of_arrays():
    assert_scan_output(
        'select * from rs_json_format.json_array_arrays',
        [{'arr_outer': [[1, 2], [1200000, 345600]], 'arr_string': [b'a', b'b'],
          'str_val': b'abc', 'int_val': 1},
         {'arr_outer': [[3, 4], [1200000, 345600]], 'arr_string': [b'c', b'd'],
          'str_val': b'def', 'int_val': 4}])

    assert_scan_output(
        'select * from parquet_testing.nested_lists_snappy',
        [{'a': [[[b'a', b'b'], [b'c']], [None, [b'd']]], 'b': 1},
         {'a': [[[b'a', b'b'], [b'c', b'd']], [None, [b'e']]], 'b': 1},
         {'a': [[[b'a', b'b'], [b'c', b'd'], [b'e']], [None, [b'f']]], 'b': 1}])

    assert_scan_output(
        'select payload.shas from rs_json_format.gharch_test_data ' +
        'where id = \'1201654257\'',
        [
            {'payload':
                {'shas':[
                        [b'4d1085635d642ba60071341dd46d38216bff1313',
                        b'86d2a548fee49abc43bd1c251300d7089748195b@mitechie.com',
                        b'Garden it up',
                        b'Richard Harding'
                        ]
                    ]
                }
            }
        ]
    )

def test_complex_json_format():
    assert_scan_output(
        'select * from rs_json_format.gharch_test_data where id = \'1201654257\'',
        [{'actor':
            {'avatar_url':
            b'https://secure.gravatar.com/avatar/1641c0f988b844f44de596fcef3adc62?d=http://github.dev%2Fimages%2Fgravatars%2Fgravatar-user-420.png',
            'gravatar_id': b'1641c0f988b844f44de596fcef3adc62',
            'id': 75915,
            'url': b'https://api.github.dev/users/mitechie',
            'login': b'mitechie'},
            'id': b'1201654257',
            'public': True,
            'payload': {
                'actor': b'mitechie', 'size': 1,
                'head': b'4d1085635d642ba60071341dd46d38216bff1313', 'push_id': 27295992,
                'actor_gravatar': b'1641c0f988b844f44de596fcef3adc62',
                'ref': b'refs/heads/develop',
                'shas':
                    [[
                        b'4d1085635d642ba60071341dd46d38216bff1313',
                        b'86d2a548fee49abc43bd1c251300d7089748195b@mitechie.com',
                        b'Garden it up',
                        b'Richard Harding'
                    ]],
                'repo': b'mitechie/Bookie'
            },
            'type': b'PushEvent',
            'repo':
                {'id': 1176073,
                'url': b'https://api.github.dev/repos/mitechie/Bookie',
                'name': b'mitechie/Bookie'},
            'created_at': '2011-03-23 00:06:16.000'
        }]
    )
# pylint: enable=bad-continuation
# pylint: enable=line-too-long
