# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/internal/descriptor_pool_test2.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf.internal import descriptor_pool_test1_pb2 as google_dot_protobuf_dot_internal_dot_descriptor__pool__test1__pb2
from google.protobuf.internal import more_messages_pb2 as google_dot_protobuf_dot_internal_dot_more__messages__pb2

from google.protobuf.internal.more_messages_pb2 import *

DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/protobuf/internal/descriptor_pool_test2.proto',
  package='google.protobuf.python.internal',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4google/protobuf/internal/descriptor_pool_test2.proto\x12\x1fgoogle.protobuf.python.internal\x1a\x34google/protobuf/internal/descriptor_pool_test1.proto\x1a,google/protobuf/internal/more_messages.proto\"\xef\x06\n\x13\x44\x65scriptorPoolTest3\x12X\n\x0bnested_enum\x18\x01 \x01(\x0e\x32?.google.protobuf.python.internal.DescriptorPoolTest3.NestedEnum:\x02XI\x12Z\n\x0enested_message\x18\x02 \x01(\x0b\x32\x42.google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage\x1a\xf7\x03\n\rNestedMessage\x12\x66\n\x0bnested_enum\x18\x01 \x01(\x0e\x32M.google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.NestedEnum:\x02PI\x12\x18\n\x0cnested_field\x18\x02 \x01(\t:\x02nu\x12q\n\x13\x64\x65\x65p_nested_message\x18\x03 \x01(\x0b\x32T.google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage\x1a\xcd\x01\n\x11\x44\x65\x65pNestedMessage\x12y\n\x0bnested_enum\x18\x01 \x01(\x0e\x32_.google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage.NestedEnum:\x03RHO\x12\x1b\n\x0cnested_field\x18\x02 \x01(\t:\x05sigma\" \n\nNestedEnum\x12\x07\n\x03RHO\x10\x11\x12\t\n\x05SIGMA\x10\x12\"!\n\nNestedEnum\x12\x0b\n\x07OMICRON\x10\x0f\x12\x06\n\x02PI\x10\x10\"\x1c\n\nNestedEnum\x12\x06\n\x02NU\x10\r\x12\x06\n\x02XI\x10\x0e\x32\x89\x01\n\x14\x64\x65scriptor_pool_test\x12\x34.google.protobuf.python.internal.DescriptorPoolTest1\x18\xe9\x07 \x01(\x0b\x32\x34.google.protobuf.python.internal.DescriptorPoolTest3P\x01'
  ,
  dependencies=[google_dot_protobuf_dot_internal_dot_descriptor__pool__test1__pb2.DESCRIPTOR,google_dot_protobuf_dot_internal_dot_more__messages__pb2.DESCRIPTOR,],
  public_dependencies=[google_dot_protobuf_dot_internal_dot_more__messages__pb2.DESCRIPTOR,])



_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE_NESTEDENUM = _descriptor.EnumDescriptor(
  name='NestedEnum',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage.NestedEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RHO', index=0, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIGMA', index=1, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=832,
  serialized_end=864,
)
_sym_db.RegisterEnumDescriptor(_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE_NESTEDENUM)

_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_NESTEDENUM = _descriptor.EnumDescriptor(
  name='NestedEnum',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.NestedEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OMICRON', index=0, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PI', index=1, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=866,
  serialized_end=899,
)
_sym_db.RegisterEnumDescriptor(_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_NESTEDENUM)

_DESCRIPTORPOOLTEST3_NESTEDENUM = _descriptor.EnumDescriptor(
  name='NestedEnum',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedEnum',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NU', index=0, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='XI', index=1, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=901,
  serialized_end=929,
)
_sym_db.RegisterEnumDescriptor(_DESCRIPTORPOOLTEST3_NESTEDENUM)


_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE = _descriptor.Descriptor(
  name='DeepNestedMessage',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nested_enum', full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage.nested_enum', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=17,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_field', full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage.nested_field', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"sigma".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE_NESTEDENUM,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=659,
  serialized_end=864,
)

_DESCRIPTORPOOLTEST3_NESTEDMESSAGE = _descriptor.Descriptor(
  name='NestedMessage',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nested_enum', full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.nested_enum', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=16,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_field', full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.nested_field', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"nu".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deep_nested_message', full_name='google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.deep_nested_message', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE, ],
  enum_types=[
    _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_NESTEDENUM,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=396,
  serialized_end=899,
)

_DESCRIPTORPOOLTEST3 = _descriptor.Descriptor(
  name='DescriptorPoolTest3',
  full_name='google.protobuf.python.internal.DescriptorPoolTest3',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nested_enum', full_name='google.protobuf.python.internal.DescriptorPoolTest3.nested_enum', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=14,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nested_message', full_name='google.protobuf.python.internal.DescriptorPoolTest3.nested_message', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='descriptor_pool_test', full_name='google.protobuf.python.internal.DescriptorPoolTest3.descriptor_pool_test', index=0,
      number=1001, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  nested_types=[_DESCRIPTORPOOLTEST3_NESTEDMESSAGE, ],
  enum_types=[
    _DESCRIPTORPOOLTEST3_NESTEDENUM,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=1069,
)

_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE.fields_by_name['nested_enum'].enum_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE_NESTEDENUM
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE.containing_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE_NESTEDENUM.containing_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE.fields_by_name['nested_enum'].enum_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_NESTEDENUM
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE.fields_by_name['deep_nested_message'].message_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE.containing_type = _DESCRIPTORPOOLTEST3
_DESCRIPTORPOOLTEST3_NESTEDMESSAGE_NESTEDENUM.containing_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE
_DESCRIPTORPOOLTEST3.fields_by_name['nested_enum'].enum_type = _DESCRIPTORPOOLTEST3_NESTEDENUM
_DESCRIPTORPOOLTEST3.fields_by_name['nested_message'].message_type = _DESCRIPTORPOOLTEST3_NESTEDMESSAGE
_DESCRIPTORPOOLTEST3_NESTEDENUM.containing_type = _DESCRIPTORPOOLTEST3
DESCRIPTOR.message_types_by_name['DescriptorPoolTest3'] = _DESCRIPTORPOOLTEST3
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DescriptorPoolTest3 = _reflection.GeneratedProtocolMessageType('DescriptorPoolTest3', (_message.Message,), {

  'NestedMessage' : _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), {

    'DeepNestedMessage' : _reflection.GeneratedProtocolMessageType('DeepNestedMessage', (_message.Message,), {
      'DESCRIPTOR' : _DESCRIPTORPOOLTEST3_NESTEDMESSAGE_DEEPNESTEDMESSAGE,
      '__module__' : 'google.protobuf.internal.descriptor_pool_test2_pb2'
      # @@protoc_insertion_point(class_scope:google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage.DeepNestedMessage)
      })
    ,
    'DESCRIPTOR' : _DESCRIPTORPOOLTEST3_NESTEDMESSAGE,
    '__module__' : 'google.protobuf.internal.descriptor_pool_test2_pb2'
    # @@protoc_insertion_point(class_scope:google.protobuf.python.internal.DescriptorPoolTest3.NestedMessage)
    })
  ,
  'DESCRIPTOR' : _DESCRIPTORPOOLTEST3,
  '__module__' : 'google.protobuf.internal.descriptor_pool_test2_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.python.internal.DescriptorPoolTest3)
  })
_sym_db.RegisterMessage(DescriptorPoolTest3)
_sym_db.RegisterMessage(DescriptorPoolTest3.NestedMessage)
_sym_db.RegisterMessage(DescriptorPoolTest3.NestedMessage.DeepNestedMessage)

_DESCRIPTORPOOLTEST3.extensions_by_name['descriptor_pool_test'].message_type = _DESCRIPTORPOOLTEST3
google_dot_protobuf_dot_internal_dot_descriptor__pool__test1__pb2.DescriptorPoolTest1.RegisterExtension(_DESCRIPTORPOOLTEST3.extensions_by_name['descriptor_pool_test'])

# @@protoc_insertion_point(module_scope)
