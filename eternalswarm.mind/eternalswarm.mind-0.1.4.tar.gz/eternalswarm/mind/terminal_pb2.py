# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: terminal.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import models_pb2 as models__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='terminal.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0eterminal.proto\x1a\x0cmodels.proto\"c\n\x08Terminal\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05label\x18\x02 \x01(\t\x12\x0f\n\x07running\x18\x03 \x01(\x08\x12\x0e\n\x06log_id\x18\x04 \x01(\x05\x12\x1b\n\x04size\x18\x05 \x01(\x0b\x32\r.TerminalSize\",\n\x0cTerminalList\x12\x1c\n\tterminals\x18\x01 \x03(\x0b\x32\t.Terminal\"*\n\rTerminalInput\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05input\x18\x02 \x01(\x0c\",\n\x0eTerminalOutput\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06output\x18\x03 \x01(\x0c\"F\n\x0cTerminalSize\x12\x0c\n\x04rows\x18\x01 \x01(\x05\x12\x0c\n\x04\x63ols\x18\x02 \x01(\x05\x12\x0c\n\x04xpix\x18\x03 \x01(\x05\x12\x0c\n\x04ypix\x18\x04 \x01(\x05\x32\xc2\x02\n\x0fTerminalService\x12/\n\rListTerminals\x12\r.EmptyRequest\x1a\r.TerminalList\"\x00\x12%\n\x0bGetTerminal\x12\t.Terminal\x1a\t.Terminal\"\x00\x12)\n\x0bNewTerminal\x12\r.EmptyRequest\x1a\t.Terminal\"\x00\x12*\n\x0cStopTerminal\x12\t.Terminal\x1a\r.EmptyMessage\"\x00\x12,\n\tSendInput\x12\x0e.TerminalInput\x1a\r.EmptyMessage\"\x00\x12(\n\x0eUpdateTerminal\x12\t.Terminal\x1a\t.Terminal\"\x00\x12(\n\x0eResizeTerminal\x12\t.Terminal\x1a\t.Terminal\"\x00\x62\x06proto3'
  ,
  dependencies=[models__pb2.DESCRIPTOR,])




_TERMINAL = _descriptor.Descriptor(
  name='Terminal',
  full_name='Terminal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Terminal.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='Terminal.label', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='running', full_name='Terminal.running', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='log_id', full_name='Terminal.log_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='Terminal.size', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=131,
)


_TERMINALLIST = _descriptor.Descriptor(
  name='TerminalList',
  full_name='TerminalList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='terminals', full_name='TerminalList.terminals', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=133,
  serialized_end=177,
)


_TERMINALINPUT = _descriptor.Descriptor(
  name='TerminalInput',
  full_name='TerminalInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='TerminalInput.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input', full_name='TerminalInput.input', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=221,
)


_TERMINALOUTPUT = _descriptor.Descriptor(
  name='TerminalOutput',
  full_name='TerminalOutput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='TerminalOutput.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output', full_name='TerminalOutput.output', index=1,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=267,
)


_TERMINALSIZE = _descriptor.Descriptor(
  name='TerminalSize',
  full_name='TerminalSize',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rows', full_name='TerminalSize.rows', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cols', full_name='TerminalSize.cols', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='xpix', full_name='TerminalSize.xpix', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ypix', full_name='TerminalSize.ypix', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=269,
  serialized_end=339,
)

_TERMINAL.fields_by_name['size'].message_type = _TERMINALSIZE
_TERMINALLIST.fields_by_name['terminals'].message_type = _TERMINAL
DESCRIPTOR.message_types_by_name['Terminal'] = _TERMINAL
DESCRIPTOR.message_types_by_name['TerminalList'] = _TERMINALLIST
DESCRIPTOR.message_types_by_name['TerminalInput'] = _TERMINALINPUT
DESCRIPTOR.message_types_by_name['TerminalOutput'] = _TERMINALOUTPUT
DESCRIPTOR.message_types_by_name['TerminalSize'] = _TERMINALSIZE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Terminal = _reflection.GeneratedProtocolMessageType('Terminal', (_message.Message,), {
  'DESCRIPTOR' : _TERMINAL,
  '__module__' : 'terminal_pb2'
  # @@protoc_insertion_point(class_scope:Terminal)
  })
_sym_db.RegisterMessage(Terminal)

TerminalList = _reflection.GeneratedProtocolMessageType('TerminalList', (_message.Message,), {
  'DESCRIPTOR' : _TERMINALLIST,
  '__module__' : 'terminal_pb2'
  # @@protoc_insertion_point(class_scope:TerminalList)
  })
_sym_db.RegisterMessage(TerminalList)

TerminalInput = _reflection.GeneratedProtocolMessageType('TerminalInput', (_message.Message,), {
  'DESCRIPTOR' : _TERMINALINPUT,
  '__module__' : 'terminal_pb2'
  # @@protoc_insertion_point(class_scope:TerminalInput)
  })
_sym_db.RegisterMessage(TerminalInput)

TerminalOutput = _reflection.GeneratedProtocolMessageType('TerminalOutput', (_message.Message,), {
  'DESCRIPTOR' : _TERMINALOUTPUT,
  '__module__' : 'terminal_pb2'
  # @@protoc_insertion_point(class_scope:TerminalOutput)
  })
_sym_db.RegisterMessage(TerminalOutput)

TerminalSize = _reflection.GeneratedProtocolMessageType('TerminalSize', (_message.Message,), {
  'DESCRIPTOR' : _TERMINALSIZE,
  '__module__' : 'terminal_pb2'
  # @@protoc_insertion_point(class_scope:TerminalSize)
  })
_sym_db.RegisterMessage(TerminalSize)



_TERMINALSERVICE = _descriptor.ServiceDescriptor(
  name='TerminalService',
  full_name='TerminalService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=342,
  serialized_end=664,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListTerminals',
    full_name='TerminalService.ListTerminals',
    index=0,
    containing_service=None,
    input_type=models__pb2._EMPTYREQUEST,
    output_type=_TERMINALLIST,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetTerminal',
    full_name='TerminalService.GetTerminal',
    index=1,
    containing_service=None,
    input_type=_TERMINAL,
    output_type=_TERMINAL,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='NewTerminal',
    full_name='TerminalService.NewTerminal',
    index=2,
    containing_service=None,
    input_type=models__pb2._EMPTYREQUEST,
    output_type=_TERMINAL,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StopTerminal',
    full_name='TerminalService.StopTerminal',
    index=3,
    containing_service=None,
    input_type=_TERMINAL,
    output_type=models__pb2._EMPTYMESSAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendInput',
    full_name='TerminalService.SendInput',
    index=4,
    containing_service=None,
    input_type=_TERMINALINPUT,
    output_type=models__pb2._EMPTYMESSAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateTerminal',
    full_name='TerminalService.UpdateTerminal',
    index=5,
    containing_service=None,
    input_type=_TERMINAL,
    output_type=_TERMINAL,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ResizeTerminal',
    full_name='TerminalService.ResizeTerminal',
    index=6,
    containing_service=None,
    input_type=_TERMINAL,
    output_type=_TERMINAL,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TERMINALSERVICE)

DESCRIPTOR.services_by_name['TerminalService'] = _TERMINALSERVICE

# @@protoc_insertion_point(module_scope)
