# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow/rpc/rpc_options.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='minknow/rpc/rpc_options.proto',
  package='ont.rpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1dminknow/rpc/rpc_options.proto\x12\x07ont.rpc\x1a google/protobuf/descriptor.proto:5\n\x0crpc_required\x12\x1d.google.protobuf.FieldOptions\x18\xd1\x86\x03 \x01(\x08:3\n\nrpc_unwrap\x12\x1d.google.protobuf.FieldOptions\x18\xd2\x86\x03 \x01(\x08\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])


RPC_REQUIRED_FIELD_NUMBER = 50001
rpc_required = _descriptor.FieldDescriptor(
  name='rpc_required', full_name='ont.rpc.rpc_required', index=0,
  number=50001, type=8, cpp_type=7, label=1,
  has_default_value=False, default_value=False,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)
RPC_UNWRAP_FIELD_NUMBER = 50002
rpc_unwrap = _descriptor.FieldDescriptor(
  name='rpc_unwrap', full_name='ont.rpc.rpc_unwrap', index=1,
  number=50002, type=8, cpp_type=7, label=1,
  has_default_value=False, default_value=False,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR)

DESCRIPTOR.extensions_by_name['rpc_required'] = rpc_required
DESCRIPTOR.extensions_by_name['rpc_unwrap'] = rpc_unwrap
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(rpc_required)
google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(rpc_unwrap)

# @@protoc_insertion_point(module_scope)
