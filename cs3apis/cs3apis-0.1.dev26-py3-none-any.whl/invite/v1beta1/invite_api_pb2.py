# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cs3/invite/v1beta1/invite_api.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cs3.identity.user.v1beta1 import resources_pb2 as cs3_dot_identity_dot_user_dot_v1beta1_dot_resources__pb2
from cs3.invite.v1beta1 import resources_pb2 as cs3_dot_invite_dot_v1beta1_dot_resources__pb2
from cs3.rpc.v1beta1 import status_pb2 as cs3_dot_rpc_dot_v1beta1_dot_status__pb2
from cs3.sharing.ocm.v1beta1 import resources_pb2 as cs3_dot_sharing_dot_ocm_dot_v1beta1_dot_resources__pb2
from cs3.types.v1beta1 import types_pb2 as cs3_dot_types_dot_v1beta1_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cs3/invite/v1beta1/invite_api.proto',
  package='cs3.invite.v1beta1',
  syntax='proto3',
  serialized_options=_b('\n\026com.cs3.invite.v1beta1B\016InviteApiProtoP\001Z\rinvitev1beta1\242\002\003CIX\252\002\022Cs3.Invite.V1Beta1\312\002\022Cs3\\Invite\\V1Beta1'),
  serialized_pb=_b('\n#cs3/invite/v1beta1/invite_api.proto\x12\x12\x63s3.invite.v1beta1\x1a)cs3/identity/user/v1beta1/resources.proto\x1a\"cs3/invite/v1beta1/resources.proto\x1a\x1c\x63s3/rpc/v1beta1/status.proto\x1a\'cs3/sharing/ocm/v1beta1/resources.proto\x1a\x1d\x63s3/types/v1beta1/types.proto\"G\n\x1aGenerateInviteTokenRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\"\xa8\x01\n\x1bGenerateInviteTokenResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12\x35\n\x0cinvite_token\x18\x03 \x01(\x0b\x32\x1f.cs3.invite.v1beta1.InviteToken\"\xbf\x01\n\x14\x46orwardInviteRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12\x35\n\x0cinvite_token\x18\x02 \x01(\x0b\x32\x1f.cs3.invite.v1beta1.InviteToken\x12\x45\n\x16origin_system_provider\x18\x03 \x01(\x0b\x32%.cs3.sharing.ocm.v1beta1.ProviderInfo\"k\n\x15\x46orwardInviteResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\"\xf5\x01\n\x13\x41\x63\x63\x65ptInviteRequest\x12)\n\x06opaque\x18\x01 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque\x12\x35\n\x0cinvite_token\x18\x02 \x01(\x0b\x32\x1f.cs3.invite.v1beta1.InviteToken\x12\x32\n\x07user_id\x18\x03 \x01(\x0b\x32!.cs3.identity.user.v1beta1.UserId\x12H\n\x19recipient_system_provider\x18\x04 \x01(\x0b\x32%.cs3.sharing.ocm.v1beta1.ProviderInfo\"j\n\x14\x41\x63\x63\x65ptInviteResponse\x12\'\n\x06status\x18\x01 \x01(\x0b\x32\x17.cs3.rpc.v1beta1.Status\x12)\n\x06opaque\x18\x02 \x01(\x0b\x32\x19.cs3.types.v1beta1.Opaque2\xcc\x02\n\tInviteAPI\x12v\n\x13GenerateInviteToken\x12..cs3.invite.v1beta1.GenerateInviteTokenRequest\x1a/.cs3.invite.v1beta1.GenerateInviteTokenResponse\x12\x64\n\rForwardInvite\x12(.cs3.invite.v1beta1.ForwardInviteRequest\x1a).cs3.invite.v1beta1.ForwardInviteResponse\x12\x61\n\x0c\x41\x63\x63\x65ptInvite\x12\'.cs3.invite.v1beta1.AcceptInviteRequest\x1a(.cs3.invite.v1beta1.AcceptInviteResponseBi\n\x16\x63om.cs3.invite.v1beta1B\x0eInviteApiProtoP\x01Z\rinvitev1beta1\xa2\x02\x03\x43IX\xaa\x02\x12\x43s3.Invite.V1Beta1\xca\x02\x12\x43s3\\Invite\\V1Beta1b\x06proto3')
  ,
  dependencies=[cs3_dot_identity_dot_user_dot_v1beta1_dot_resources__pb2.DESCRIPTOR,cs3_dot_invite_dot_v1beta1_dot_resources__pb2.DESCRIPTOR,cs3_dot_rpc_dot_v1beta1_dot_status__pb2.DESCRIPTOR,cs3_dot_sharing_dot_ocm_dot_v1beta1_dot_resources__pb2.DESCRIPTOR,cs3_dot_types_dot_v1beta1_dot_types__pb2.DESCRIPTOR,])




_GENERATEINVITETOKENREQUEST = _descriptor.Descriptor(
  name='GenerateInviteTokenRequest',
  full_name='cs3.invite.v1beta1.GenerateInviteTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.GenerateInviteTokenRequest.opaque', index=0,
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
  serialized_start=240,
  serialized_end=311,
)


_GENERATEINVITETOKENRESPONSE = _descriptor.Descriptor(
  name='GenerateInviteTokenResponse',
  full_name='cs3.invite.v1beta1.GenerateInviteTokenResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.invite.v1beta1.GenerateInviteTokenResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.GenerateInviteTokenResponse.opaque', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='invite_token', full_name='cs3.invite.v1beta1.GenerateInviteTokenResponse.invite_token', index=2,
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
  serialized_start=314,
  serialized_end=482,
)


_FORWARDINVITEREQUEST = _descriptor.Descriptor(
  name='ForwardInviteRequest',
  full_name='cs3.invite.v1beta1.ForwardInviteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.ForwardInviteRequest.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='invite_token', full_name='cs3.invite.v1beta1.ForwardInviteRequest.invite_token', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='origin_system_provider', full_name='cs3.invite.v1beta1.ForwardInviteRequest.origin_system_provider', index=2,
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
  serialized_start=485,
  serialized_end=676,
)


_FORWARDINVITERESPONSE = _descriptor.Descriptor(
  name='ForwardInviteResponse',
  full_name='cs3.invite.v1beta1.ForwardInviteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.invite.v1beta1.ForwardInviteResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.ForwardInviteResponse.opaque', index=1,
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
  serialized_start=678,
  serialized_end=785,
)


_ACCEPTINVITEREQUEST = _descriptor.Descriptor(
  name='AcceptInviteRequest',
  full_name='cs3.invite.v1beta1.AcceptInviteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.AcceptInviteRequest.opaque', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='invite_token', full_name='cs3.invite.v1beta1.AcceptInviteRequest.invite_token', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='cs3.invite.v1beta1.AcceptInviteRequest.user_id', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recipient_system_provider', full_name='cs3.invite.v1beta1.AcceptInviteRequest.recipient_system_provider', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=788,
  serialized_end=1033,
)


_ACCEPTINVITERESPONSE = _descriptor.Descriptor(
  name='AcceptInviteResponse',
  full_name='cs3.invite.v1beta1.AcceptInviteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='cs3.invite.v1beta1.AcceptInviteResponse.status', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opaque', full_name='cs3.invite.v1beta1.AcceptInviteResponse.opaque', index=1,
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
  serialized_start=1035,
  serialized_end=1141,
)

_GENERATEINVITETOKENREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GENERATEINVITETOKENRESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_GENERATEINVITETOKENRESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_GENERATEINVITETOKENRESPONSE.fields_by_name['invite_token'].message_type = cs3_dot_invite_dot_v1beta1_dot_resources__pb2._INVITETOKEN
_FORWARDINVITEREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_FORWARDINVITEREQUEST.fields_by_name['invite_token'].message_type = cs3_dot_invite_dot_v1beta1_dot_resources__pb2._INVITETOKEN
_FORWARDINVITEREQUEST.fields_by_name['origin_system_provider'].message_type = cs3_dot_sharing_dot_ocm_dot_v1beta1_dot_resources__pb2._PROVIDERINFO
_FORWARDINVITERESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_FORWARDINVITERESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_ACCEPTINVITEREQUEST.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
_ACCEPTINVITEREQUEST.fields_by_name['invite_token'].message_type = cs3_dot_invite_dot_v1beta1_dot_resources__pb2._INVITETOKEN
_ACCEPTINVITEREQUEST.fields_by_name['user_id'].message_type = cs3_dot_identity_dot_user_dot_v1beta1_dot_resources__pb2._USERID
_ACCEPTINVITEREQUEST.fields_by_name['recipient_system_provider'].message_type = cs3_dot_sharing_dot_ocm_dot_v1beta1_dot_resources__pb2._PROVIDERINFO
_ACCEPTINVITERESPONSE.fields_by_name['status'].message_type = cs3_dot_rpc_dot_v1beta1_dot_status__pb2._STATUS
_ACCEPTINVITERESPONSE.fields_by_name['opaque'].message_type = cs3_dot_types_dot_v1beta1_dot_types__pb2._OPAQUE
DESCRIPTOR.message_types_by_name['GenerateInviteTokenRequest'] = _GENERATEINVITETOKENREQUEST
DESCRIPTOR.message_types_by_name['GenerateInviteTokenResponse'] = _GENERATEINVITETOKENRESPONSE
DESCRIPTOR.message_types_by_name['ForwardInviteRequest'] = _FORWARDINVITEREQUEST
DESCRIPTOR.message_types_by_name['ForwardInviteResponse'] = _FORWARDINVITERESPONSE
DESCRIPTOR.message_types_by_name['AcceptInviteRequest'] = _ACCEPTINVITEREQUEST
DESCRIPTOR.message_types_by_name['AcceptInviteResponse'] = _ACCEPTINVITERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GenerateInviteTokenRequest = _reflection.GeneratedProtocolMessageType('GenerateInviteTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _GENERATEINVITETOKENREQUEST,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.GenerateInviteTokenRequest)
  })
_sym_db.RegisterMessage(GenerateInviteTokenRequest)

GenerateInviteTokenResponse = _reflection.GeneratedProtocolMessageType('GenerateInviteTokenResponse', (_message.Message,), {
  'DESCRIPTOR' : _GENERATEINVITETOKENRESPONSE,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.GenerateInviteTokenResponse)
  })
_sym_db.RegisterMessage(GenerateInviteTokenResponse)

ForwardInviteRequest = _reflection.GeneratedProtocolMessageType('ForwardInviteRequest', (_message.Message,), {
  'DESCRIPTOR' : _FORWARDINVITEREQUEST,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.ForwardInviteRequest)
  })
_sym_db.RegisterMessage(ForwardInviteRequest)

ForwardInviteResponse = _reflection.GeneratedProtocolMessageType('ForwardInviteResponse', (_message.Message,), {
  'DESCRIPTOR' : _FORWARDINVITERESPONSE,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.ForwardInviteResponse)
  })
_sym_db.RegisterMessage(ForwardInviteResponse)

AcceptInviteRequest = _reflection.GeneratedProtocolMessageType('AcceptInviteRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPTINVITEREQUEST,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.AcceptInviteRequest)
  })
_sym_db.RegisterMessage(AcceptInviteRequest)

AcceptInviteResponse = _reflection.GeneratedProtocolMessageType('AcceptInviteResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPTINVITERESPONSE,
  '__module__' : 'cs3.invite.v1beta1.invite_api_pb2'
  # @@protoc_insertion_point(class_scope:cs3.invite.v1beta1.AcceptInviteResponse)
  })
_sym_db.RegisterMessage(AcceptInviteResponse)


DESCRIPTOR._options = None

_INVITEAPI = _descriptor.ServiceDescriptor(
  name='InviteAPI',
  full_name='cs3.invite.v1beta1.InviteAPI',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1144,
  serialized_end=1476,
  methods=[
  _descriptor.MethodDescriptor(
    name='GenerateInviteToken',
    full_name='cs3.invite.v1beta1.InviteAPI.GenerateInviteToken',
    index=0,
    containing_service=None,
    input_type=_GENERATEINVITETOKENREQUEST,
    output_type=_GENERATEINVITETOKENRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ForwardInvite',
    full_name='cs3.invite.v1beta1.InviteAPI.ForwardInvite',
    index=1,
    containing_service=None,
    input_type=_FORWARDINVITEREQUEST,
    output_type=_FORWARDINVITERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AcceptInvite',
    full_name='cs3.invite.v1beta1.InviteAPI.AcceptInvite',
    index=2,
    containing_service=None,
    input_type=_ACCEPTINVITEREQUEST,
    output_type=_ACCEPTINVITERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_INVITEAPI)

DESCRIPTOR.services_by_name['InviteAPI'] = _INVITEAPI

# @@protoc_insertion_point(module_scope)
