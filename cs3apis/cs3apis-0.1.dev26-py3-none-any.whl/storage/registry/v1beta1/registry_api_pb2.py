# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cs3/storage/registry/v1beta1/registry_api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cs3.rpc.v1beta1 import status_pb2 as cs3_dot_rpc_dot_v1beta1_dot_status__pb2
from cs3.storage.provider.v1beta1 import resources_pb2 as cs3_dot_storage_dot_provider_dot_v1beta1_dot_resources__pb2
from cs3.storage.registry.v1beta1 import resources_pb2 as cs3_dot_storage_dot_registry_dot_v1beta1_dot_resources__pb2
from cs3.types.v1beta1 import types_pb2 as cs3_dot_types_dot_v1beta1_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cs3/storage/registry/v1beta1/registry_api.proto',
  package='cs3.storage.registry.v1beta1',
  syntax='proto3',
  serialized_options=_b('\n com.cs3.storage.registry.v1beta1B\020RegistryApiProtoP\001Z\017registryv1beta1\242\002\003CSR\252\002\034Cs3.Storage.Registry.V1Beta1\312\002\034Cs3\\Storage\\Registry\\V1Beta1'),
  serialized_pb=_b('\n/cs3/storage/registry/v1beta1/registry_api.proto\x12\x1c\x63s3.storage.registry.v1beta1\x1a\x1c\x63s3/rpc/v1beta1/status.proto\x1a,cs3/storage/provider/v1beta1/resources.proto\x1a,cs3/storage/registry/v1beta1/resources.proto\x1a\x1d\x63s3/types/v1beta1/types.proto\";\n\x0eGetHomeRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\"\xa3\x01\n\x0fGetHomeResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12<\n\x08provider\x18\x03 \x01(\x0b\x32*.cs3.storage.registry.v1beta1.ProviderInfo\"|\n\x19GetStorageProviderRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12\x34\n\x03ref\x18\x02 \x01(\x0b\x32\'.cs3.storage.provider.v1beta1.Reference\"\xae\x01\n\x1aGetStorageProviderResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12<\n\x08provider\x18\x03 \x01(\x0b\x32*.cs3.storage.registry.v1beta1.ProviderInfo\"H\n\x1bListStorageProvidersRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\"\xb1\x01\n\x1cListStorageProvidersResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12=\n\tproviders\x18\x03 \x03(\x0b\x32*.cs3.storage.registry.v1beta1.ProviderInfo2\x8f\x03\n\x0bRegistryAPI\x12\x87\x01\n\x12GetStorageProvider\x12\x37.cs3.storage.registry.v1beta1.GetStorageProviderRequest\x1a\x38.cs3.storage.registry.v1beta1.GetStorageProviderResponse\x12\x8d\x01\n\x14ListStorageProviders\x12\x39.cs3.storage.registry.v1beta1.ListStorageProvidersRequest\x1a:.cs3.storage.registry.v1beta1.ListStorageProvidersResponse\x12\x66\n\x07GetHome\x12,.cs3.storage.registry.v1beta1.GetHomeRequest\x1a-.cs3.storage.registry.v1beta1.GetHomeResponseB\x8b\x01\n com.cs3.storage.registry.v1beta1B\x10RegistryApiProtoP\x01Z\x0fregistryv1beta1\xa2\x02\x03\x43SR\xaa\x02\x1c\x43s3.Storage.Registry.V1Beta1\xca\x02\x1c\x43s3\\Storage\\Registry\\V1Beta1b\x06proto3')
  ,
  dependencies=[cs3_dot_rpc_dot_v1beta1_dot_status__pb2.DESCRIPTOR,cs3_dot_storage_dot_provider_dot_v1beta1_dot_resources__pb2.DESCRIPTOR,cs3_dot_storage_dot_registry_dot_v1beta1_dot_resources__pb2.DESCRIPTOR,cs3_dot_types_dot_v1beta1_dot_types__pb2.DESCRIPTOR,])




_GETHOMEREQUEST = _descriptor.Descriptor(
  name='GetHomeRequest',
  full_name='cs3.storage.registry.v1beta1.GetHomeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.GetHomeRequest.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=234,
  serialized_end=293,
)


_GETHOMERESPONSE = _descriptor.Descriptor(
  name='GetHomeResponse',
  full_name='cs3.storage.registry.v1beta1.GetHomeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.storage.registry.v1beta1.GetHomeResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.GetHomeResponse.opaque', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provider', full_name='cs3.storage.registry.v1beta1.GetHomeResponse.provider', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=296,
  serialized_end=459,
)


_GETSTORAGEPROVIDERREQUEST = _descriptor.Descriptor(
  name='GetStorageProviderRequest',
  full_name='cs3.storage.registry.v1beta1.GetStorageProviderRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.GetStorageProviderRequest.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ref', full_name='cs3.storage.registry.v1beta1.GetStorageProviderRequest.ref', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=461,
  serialized_end=585,
)


_GETSTORAGEPROVIDERRESPONSE = _descriptor.Descriptor(
  name='GetStorageProviderResponse',
  full_name='cs3.storage.registry.v1beta1.GetStorageProviderResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.storage.registry.v1beta1.GetStorageProviderResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.GetStorageProviderResponse.opaque', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='provider', full_name='cs3.storage.registry.v1beta1.GetStorageProviderResponse.provider', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=588,
  serialized_end=762,
)


_LISTSTORAGEPROVIDERSREQUEST = _descriptor.Descriptor(
  name='ListStorageProvidersRequest',
  full_name='cs3.storage.registry.v1beta1.ListStorageProvidersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.ListStorageProvidersRequest.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=764,
  serialized_end=836,
)


_LISTSTORAGEPROVIDERSRESPONSE = _descriptor.Descriptor(
  name='ListStorageProvidersResponse',
  full_name='cs3.storage.registry.v1beta1.ListStorageProvidersResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.storage.registry.v1beta1.ListStorageProvidersResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.storage.registry.v1beta1.ListStorageProvidersResponse.opaque', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='providers', full_name='cs3.storage.registry.v1beta1.ListStorageProvidersResponse.providers', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=839,
  serialized_end=1016,
)

_GETHOMEREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GETHOMERESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_GETHOMERESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GETHOMERESPONSE.fields_by_name['provider'].message_type = cs3_dot_storage_dot_registry_dot_v1beta1_dot_resources__pb2._PROVIDERINFO
_GETSTORAGEPROVIDERREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GETSTORAGEPROVIDERREQUEST.fields_by_name['ref'].message_type = cs3_dot_storage_dot_provider_dot_v1beta1_dot_resources__pb2._REFERENCE
_GETSTORAGEPROVIDERRESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_GETSTORAGEPROVIDERRESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GETSTORAGEPROVIDERRESPONSE.fields_by_name['provider'].message_type = cs3_dot_storage_dot_registry_dot_v1beta1_dot_resources__pb2._PROVIDERINFO
_LISTSTORAGEPROVIDERSREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_LISTSTORAGEPROVIDERSRESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_LISTSTORAGEPROVIDERSRESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_LISTSTORAGEPROVIDERSRESPONSE.fields_by_name['providers'].message_type = cs3_dot_storage_dot_registry_dot_v1beta1_dot_resources__pb2._PROVIDERINFO
DESCRIPTOR.message_types_by_name['GetHomeRequest'] = _GETHOMEREQUEST
DESCRIPTOR.message_types_by_name['GetHomeResponse'] = _GETHOMERESPONSE
DESCRIPTOR.message_types_by_name['GetStorageProviderRequest'] = _GETSTORAGEPROVIDERREQUEST
DESCRIPTOR.message_types_by_name['GetStorageProviderResponse'] = _GETSTORAGEPROVIDERRESPONSE
DESCRIPTOR.message_types_by_name['ListStorageProvidersRequest'] = _LISTSTORAGEPROVIDERSREQUEST
DESCRIPTOR.message_types_by_name['ListStorageProvidersResponse'] = _LISTSTORAGEPROVIDERSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetHomeRequest = _reflection.GeneratedProtocolMessageType('GetHomeRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETHOMEREQUEST,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.GetHomeRequest)
  })
_sym_db.RegisterMessage(GetHomeRequest)

GetHomeResponse = _reflection.GeneratedProtocolMessageType('GetHomeResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETHOMERESPONSE,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.GetHomeResponse)
  })
_sym_db.RegisterMessage(GetHomeResponse)

GetStorageProviderRequest = _reflection.GeneratedProtocolMessageType('GetStorageProviderRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSTORAGEPROVIDERREQUEST,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.GetStorageProviderRequest)
  })
_sym_db.RegisterMessage(GetStorageProviderRequest)

GetStorageProviderResponse = _reflection.GeneratedProtocolMessageType('GetStorageProviderResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSTORAGEPROVIDERRESPONSE,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.GetStorageProviderResponse)
  })
_sym_db.RegisterMessage(GetStorageProviderResponse)

ListStorageProvidersRequest = _reflection.GeneratedProtocolMessageType('ListStorageProvidersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSTORAGEPROVIDERSREQUEST,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.ListStorageProvidersRequest)
  })
_sym_db.RegisterMessage(ListStorageProvidersRequest)

ListStorageProvidersResponse = _reflection.GeneratedProtocolMessageType('ListStorageProvidersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSTORAGEPROVIDERSRESPONSE,
  '__module__' : 'cs3.storage.registry.v1beta1.registry_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.storage.registry.v1beta1.ListStorageProvidersResponse)
  })
_sym_db.RegisterMessage(ListStorageProvidersResponse)


DESCRIPTOR._options = None

_REGISTRYAPI = _descriptor.ServiceDescriptor(
  name='RegistryAPI',
  full_name='cs3.storage.registry.v1beta1.RegistryAPI',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1019,
  serialized_end=1418,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetStorageProvider',
    full_name='cs3.storage.registry.v1beta1.RegistryAPI.GetStorageProvider',
    index=0,
    containing_service=None,
    input_type=_GETSTORAGEPROVIDERREQUEST,
    output_type=_GETSTORAGEPROVIDERRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ListStorageProviders',
    full_name='cs3.storage.registry.v1beta1.RegistryAPI.ListStorageProviders',
    index=1,
    containing_service=None,
    input_type=_LISTSTORAGEPROVIDERSREQUEST,
    output_type=_LISTSTORAGEPROVIDERSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetHome',
    full_name='cs3.storage.registry.v1beta1.RegistryAPI.GetHome',
    index=2,
    containing_service=None,
    input_type=_GETHOMEREQUEST,
    output_type=_GETHOMERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_REGISTRYAPI)

DESCRIPTOR.services_by_name['RegistryAPI'] = _REGISTRYAPI

# @@protoc_insertion_point(module_scope)
