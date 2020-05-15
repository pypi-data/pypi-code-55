# ---------------------------------------------------------------------------
# mockify/_engine/call.py
#
# Copyright (C) 2018 - 2020 Maciej Wiatrzyk
#
# This file is part of Mockify library and is released under the terms of the
# MIT license: http://opensource.org/licenses/mit-license.php.
#
# See LICENSE for details.
# ---------------------------------------------------------------------------
import os
import keyword
import traceback

from .. import exc, _utils, _globals


class LocationInfo:
    """A placeholder for file name and line number obtained from the stack.

    Used by :class:`Call` objects to get their location in the code. That
    information is later used in assertion messages.

    .. versionadded:: 0.6

    :param filename:
        Name of the file

    :param lineno:
        Line number in given file
    """

    def __init__(self, filename, lineno):
        self._filename = filename
        self._lineno = lineno

    def __eq__(self, other):
        return type(self) is type(other) and\
            self._filename == other._filename and\
            self._lineno == other._lineno

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "{}:{}".format(self._filename, self._lineno)

    @property
    def filename(self):
        """File name from stack."""
        return self._filename

    @property
    def lineno(self):
        """Line number form stack."""
        return self._lineno

    @classmethod
    def get_external(cls):
        """Factory method for creating instances of this class.

        It extracts stack and finds (in reversed order) first frame that is
        **outside** of the Mockify library. Thanks to this all mock calls or
        expectation recordings will point to test function or tested code
        that uses Mockify, not to Mockify's internals.

        :rtype: LocationInfo
        """
        stack = traceback.extract_stack()
        for frame in reversed(stack):
            if not frame.filename.startswith(_globals.ROOT_DIR) and\
               not frame.filename.startswith('/usr/lib'):  # FIXME: make this better
                return cls(frame.filename, frame.lineno)


class Call:
    """An object representing mock call.

    Instances of this class are created when expectations are recorded or
    when mock is called. Call objects are comparable. Two call objects are
    equal if and only if:

    * mock names are the same,
    * args are the same,
    * and keyword args are the same.

    :param _name_:
        The name of a mock
    """

    def __init__(self, _name_, *args, **kwargs):
        self._name = _name_
        self._args = args
        self._kwargs = kwargs
        self._location = LocationInfo.get_external()
        _utils.validate_mock_name(self._name)

    def __str__(self):
        return "{}({})".format(self._name, self._format_params(*self._args, **self._kwargs))

    def __repr__(self):
        return "<mockify.{}({})>".format(self.__class__.__name__, self._format_params(self._name, *self._args, **self._kwargs))

    def __eq__(self, other):
        return self._name == other._name and\
            self._args == other._args and\
            self._kwargs == other._kwargs

    def __ne__(self, other):
        return not self.__eq__(other)

    def _format_params(self, *args, **kwargs):
        return _utils.format_args_kwargs(args, kwargs)

    @property
    def name(self):
        """The name of a mock."""
        return self._name

    @property
    def args(self):
        """Positional args mock was called with or is expected to be called
        with."""
        return self._args

    @property
    def kwargs(self):
        """Keyword args mock was called with or is expected to be called
        with."""
        return self._kwargs

    @property
    def location(self):
        """Information of place in test or tested code where this call object
        was created.

        .. versionadded:: 0.6

        :rtype: LocationInfo
        """
        return self._location
