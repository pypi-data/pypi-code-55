# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cs3/storage/registry/v1beta1/resources.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cs3.types.v1beta1 import types_pb2 as cs3_dot_types_dot_v1beta1_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cs3/storage/registry/v1beta1/resources.proto',
  package='cs3.storage.registry.v1beta1',
  syntax='proto3',
  serialized_options=_b('\n com.cs3.storage.registry.v1beta1B\016ResourcesProtoP\001Z\017registryv1beta1\242\002\003CSR\252\002\034Cs3.Storage.Registry.V1Beta1\312\002\034Cs3\\Storage\\Registry\\V1Beta1'),
  serialized_pb=_b('\n,cs3/storage/registry/v1beta1/resources.proto\x12\x1c\x63s3.storage.registry.v1beta1\x1a\x1d\x63s3/types/v1beta1/types.proto\"\x86\x02\n\x0cProviderInfo\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12\x13\n\x0bprovider_id\x18\x02 \x01(\t\x12\x15\n\rprovider_path\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x45\n\x08\x66\x65\x61tures\x18\x06 \x01(\x0b\x32\x33.cs3.storage.registry.v1beta1.ProviderInfo.Features\x1a\x32\n\x08\x46\x65\x61tures\x12\x0f\n\x07recycle\x18\x01 \x01(\x08\x12\x15\n\rfile_versions\x18\x02 \x01(\x08\x42\x89\x01\n com.cs3.storage.registry.v1beta1B\x0eResourcesProtoP\x01Z\x0fregistryv1beta1\xa2\x02\x03\x43SR\xaa\x02\x1c\x43s3.Storage.Registry.V1Beta1\xca\x02\x1c\x43s3\\Storage\\Registry\\V1Beta1b\x06proto3')
  ,
  dependencies=[cs3_dot_types_dot_v1beta1_dot_types__pb2.DESCRIPTOR,])




_PROVIDERINFO_FEATURES = _descriptor.Descriptor(
  name='Features',
  full_name='cs3.storage.registry.v1beta1.ProviderInfo.Features',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='recycle', full_name='cs3.storage.registry.v1beta1.ProviderInfo.Features.recycle', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file_versions', full_name='cs3.storage.registry.v1beta1.ProviderInfo.Features.file_versions', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=322,
  serialized_end=372,
)

_PROVIDERINFO = _descriptor.Descriptor(
  name='ProviderInfo',
  full_name='cs3.storage.registry.v1beta1.ProviderInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.ProviderInfo.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provider_id', full_name='cs3.storage.registry.v1beta1.ProviderInfo.provider_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provider_path', full_name='cs3.storage.registry.v1beta1.ProviderInfo.provider_path', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='cs3.storage.registry.v1beta1.ProviderInfo.address', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='cs3.storage.registry.v1beta1.ProviderInfo.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='features', full_name='cs3.storage.registry.v1beta1.ProviderInfo.features', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PROVIDERINFO_FEATURES, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=110,
  serialized_end=372,
)

_PROVIDERINFO_FEATURES.containing_type = _PROVIDERINFO
_PROVIDERINFO.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_PROVIDERINFO.fields_by_name['features'].message_type = _PROVIDERINFO_FEATURES
DESCRIPTOR.message_types_by_name['ProviderInfo'] = _PROVIDERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProviderInfo = _reflection.GeneratedProtocolMessageType('ProviderInfo', (_message.Message,), {

  'Features' : _reflection.GeneratedProtocolMessageType('Features', (_message.Message,), {
    'DESCRIPTOR' : _PROVIDERINFO_FEATURES,
    '__module__' : 'cs3.storage.registry.v1beta1.resources_pb2'
    # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.ProviderInfo.Features)
    })
  ,
  'DESCRIPTOR' : _PROVIDERINFO,
  '__module__' : 'cs3.storage.registry.v1beta1.resources_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.ProviderInfo)
  })
_sym_db.RegisterMessage(ProviderInfo)
_sym_db.RegisterMessage(ProviderInfo.Features)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
