#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

DEFAULT_VALUES = ( '1', 'able', 'active', 'allow', 'allowed', 'enabled', 'in', 'ok', 'on', 'running', 't', 'true', 'up', 'y', 'yes' )

def boolify(raw=None, custom_values=None, *, non_str=True, raise_exc=False):
  def _boolify(raw, custom_values=None, *, non_str=True, raise_exc=False):
    def is_str(raw):
      try:
        return isinstance(raw, basestring)
      except NameError:
        try:
          from six import string_types
        except ImportError:
          return isinstance(raw, str)
        else:
          return isinstance(raw, string_types)
    if isinstance(raw, bool):
      return raw
    if not non_str and not is_str(raw):
      return bool(raw)
    try:
      from distutils.util import strtobool
    except ImportError:
      pass
    if isinstance(raw, float):
      raw = round(raw) #int(raw)
    raw = str(raw).strip().lower()
    try:
      return bool(strtobool(raw))
    except (NameError, ValueError, AttributeError):
      if raise_exc and not raw in (custom_values or DEFAULT_VALUES):
        raise ValueError('Invalid value %r. Expected values are : \'%s\'' % (raw, '\', \''.join((custom_values or DEFAULT_VALUES))))
      return raw in (custom_values or DEFAULT_VALUES)
  if isinstance(raw, (list, dict, tuple, set)) and len(raw) > 0:
    if hasattr(raw, 'iteritems') or hasattr(raw, 'items'):
      return {k: _boolify(raw=_, custom_values=custom_values, non_str=non_str, raise_exc=raise_exc) for k,_ in (raw.items() if hasattr(raw, 'items') else raw.iteritems())}
    return [_boolify(raw=_, custom_values=custom_values, non_str=non_str, raise_exc=raise_exc) for _ in raw]
  return _boolify(raw=raw, custom_values=custom_values, non_str=non_str, raise_exc=raise_exc)

boolify.__doc__ = """Function that will translate common strings into bool values.

  Case is ignored for strings. These string values are handled:
    True -> {DEF}
    False -> any other string

  {PARAM3}:
    Non-string values are passed to bool.

  When '{PARAM3}' is passed as False, Objects other than string will be transformed using built-in bool() function.

  Raises ValueError when '{PARAM4}' is passed as True and it gets a string it doesn't handle.""".format(DEF='\', \''.join(DEFAULT_VALUES), PARAM3=boolify.__code__.co_varnames[-2], PARAM4=boolify.__code__.co_varnames[-1])
