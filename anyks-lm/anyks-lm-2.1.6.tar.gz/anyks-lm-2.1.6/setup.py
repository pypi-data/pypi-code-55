#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import os
import pybind11
import setuptools
from distutils.core import setup, Extension

with open("README.md", "r") as fh:
    description = fh.read()

root_dir = './alm_pkg'

include_files = [
    '%s/include/idw.hpp' % root_dir,
    '%s/include/env.hpp' % root_dir,
    '%s/include/alm.hpp' % root_dir,
    '%s/include/nwt.hpp' % root_dir,
    '%s/include/word.hpp' % root_dir,
    '%s/include/fsys.hpp' % root_dir,
    '%s/include/aspl.hpp' % root_dir,
    '%s/include/ablm.hpp' % root_dir,
    '%s/include/arpa.hpp' % root_dir,
    '%s/include/python.hpp' % root_dir,
    '%s/include/toolkit.hpp' % root_dir,
    '%s/include/general.hpp' % root_dir,
    '%s/include/alphabet.hpp' % root_dir,
    '%s/include/progress.hpp' % root_dir,
    '%s/include/tokenizer.hpp' % root_dir,
    '%s/include/collector.hpp' % root_dir,
    '%s/include/threadpool.hpp' % root_dir,
    '%s/include/levenshtein.hpp' % root_dir
]

include_bigint = [
    '%s/contrib/include/bigint/BigInteger.hh' % root_dir,
    '%s/contrib/include/bigint/BigUnsigned.hh' % root_dir,
    '%s/contrib/include/bigint/NumberlikeArray.hh' % root_dir,
    '%s/contrib/include/bigint/BigIntegerUtils.hh' % root_dir,
    '%s/contrib/include/bigint/BigIntegerLibrary.hh' % root_dir,
    '%s/contrib/include/bigint/BigUnsignedInABase.hh' % root_dir,
    '%s/contrib/include/bigint/BigIntegerAlgorithms.hh' % root_dir
]

include_nlohmann = [
    '%s/contrib/include/nlohmann/json.hpp' % root_dir,
    '%s/contrib/include/nlohmann/json_fwd.hpp' % root_dir,
    '%s/contrib/include/nlohmann/adl_serializer.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/exceptions.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/json_pointer.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/value_t.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/json_ref.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/macro_scope.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/macro_unscope.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/conversions/to_json.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/conversions/to_chars.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/conversions/from_json.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/meta/void_t.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/meta/is_sax.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/meta/detected.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/meta/cpp_future.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/meta/type_traits.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/lexer.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/parser.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/json_sax.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/position_t.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/binary_reader.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/input/input_adapters.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/output/serializer.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/output/binary_writer.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/output/output_adapters.hpp' % root_dir,
    '%s/contrib/include/nlohmann/thirdparty/hedley/hedley.hpp' % root_dir,
    '%s/contrib/include/nlohmann/thirdparty/hedley/hedley_undef.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/iter_impl.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/iteration_proxy.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/iterator_traits.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/internal_iterator.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/primitive_iterator.hpp' % root_dir,
    '%s/contrib/include/nlohmann/detail/iterators/json_reverse_iterator.hpp' % root_dir
]

src_files = [
    '%s/src/idw.cpp' % root_dir,
    '%s/src/nwt.cpp' % root_dir,
    '%s/src/arpa.cpp' % root_dir,
    '%s/src/python.cpp' % root_dir,
    '%s/src/alphabet.cpp' % root_dir,
    '%s/src/alm.cpp' % root_dir,
    '%s/src/tokenizer.cpp' % root_dir,
    '%s/src/toolkit.cpp' % root_dir,
    '%s/src/levenshtein.cpp' % root_dir,
    '%s/src/ablm.cpp' % root_dir,
    '%s/contrib/src/bigint/BigInteger.cc' % root_dir,
    '%s/contrib/src/bigint/BigUnsigned.cc' % root_dir,
    '%s/contrib/src/bigint/BigIntegerUtils.cc' % root_dir,
    '%s/contrib/src/bigint/BigUnsignedInABase.cc' % root_dir,
    '%s/contrib/src/bigint/BigIntegerAlgorithms.cc' % root_dir,
    '%s/palm.cxx' % root_dir
]

pakage_files = [
    ('include/alm', include_files),
    ('include/bigint', include_bigint),
    ('include/nlohmann', include_nlohmann)
]

ext_modules = [
    Extension(
        'alm', src_files,
        include_dirs = [
            root_dir,
            '%s/include' % root_dir,
            '%s/contrib/include' % root_dir,
            pybind11.get_include()
        ],
        language = 'c++',
        # library_dirs = [''],
        libraries = ['m', 'z', 'ssl', 'stdc++', 'crypto', 'pthread'],
        extra_compile_args = ['-std=c++11', '-O2', '-fno-permissive', '-Wno-pedantic', '-Wno-unknown-attributes']
    )
]

setuptools.setup(
    name = "anyks-lm",
    version = "2.1.6",
    author = "Yuriy Lobarev",
    author_email = "forman@anyks.com",
    description = "Smart language model",
    long_description = description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/anyks/alm",
    download_url = 'https://github.com/anyks/alm/archive/release.tar.gz',
    ext_modules = ext_modules,
    packages = setuptools.find_packages(),
    data_files = pakage_files,
    keywords = ['nlp', 'lm', 'alm', 'language-model'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD"
    ],
    requires = ['pybind11'],
    python_requires = '>=3.6',
    include_package_data = True
)
