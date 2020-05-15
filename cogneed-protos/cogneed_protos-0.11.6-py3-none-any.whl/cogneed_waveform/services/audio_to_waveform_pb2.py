# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cogneed-protos/cogneed-waveform/services/audio_to_waveform.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cogneed-protos/cogneed-waveform/services/audio_to_waveform.proto',
  package='ai.cogneed.cloud.speech.v1',
  syntax='proto3',
  serialized_options=_b('\n\032ai.cogneed.cloud.speech.v1P\001'),
  serialized_pb=_b('\n@cogneed-protos/cogneed-waveform/services/audio_to_waveform.proto\x12\x1a\x61i.cogneed.cloud.speech.v1\".\n\x0fWaveformRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x1f\n\x10WaveformResponse\x12\x0b\n\x03ret\x18\x01 \x01(\x05\x32~\n\x16WaveformStoringService\x12\x64\n\x05store\x12+.ai.cogneed.cloud.speech.v1.WaveformRequest\x1a,.ai.cogneed.cloud.speech.v1.WaveformResponse(\x01\x42\x1e\n\x1a\x61i.cogneed.cloud.speech.v1P\x01\x62\x06proto3')
)




_WAVEFORMREQUEST = _descriptor.Descriptor(
  name='WaveformRequest',
  full_name='ai.cogneed.cloud.speech.v1.WaveformRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ai.cogneed.cloud.speech.v1.WaveformRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='ai.cogneed.cloud.speech.v1.WaveformRequest.content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=96,
  serialized_end=142,
)


_WAVEFORMRESPONSE = _descriptor.Descriptor(
  name='WaveformResponse',
  full_name='ai.cogneed.cloud.speech.v1.WaveformResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ret', full_name='ai.cogneed.cloud.speech.v1.WaveformResponse.ret', index=0,
      number=1, type=5, cpp_type=1, label=1,
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
  serialized_start=144,
  serialized_end=175,
)

DESCRIPTOR.message_types_by_name['WaveformRequest'] = _WAVEFORMREQUEST
DESCRIPTOR.message_types_by_name['WaveformResponse'] = _WAVEFORMRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

WaveformRequest = _reflection.GeneratedProtocolMessageType('WaveformRequest', (_message.Message,), dict(
  DESCRIPTOR = _WAVEFORMREQUEST,
  __module__ = 'cogneed_protos.cogneed_waveform.services.audio_to_waveform_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.cloud.speech.v1.WaveformRequest)
  ))
_sym_db.RegisterMessage(WaveformRequest)

WaveformResponse = _reflection.GeneratedProtocolMessageType('WaveformResponse', (_message.Message,), dict(
  DESCRIPTOR = _WAVEFORMRESPONSE,
  __module__ = 'cogneed_protos.cogneed_waveform.services.audio_to_waveform_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.cloud.speech.v1.WaveformResponse)
  ))
_sym_db.RegisterMessage(WaveformResponse)


DESCRIPTOR._options = None

_WAVEFORMSTORINGSERVICE = _descriptor.ServiceDescriptor(
  name='WaveformStoringService',
  full_name='ai.cogneed.cloud.speech.v1.WaveformStoringService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=177,
  serialized_end=303,
  methods=[
  _descriptor.MethodDescriptor(
    name='store',
    full_name='ai.cogneed.cloud.speech.v1.WaveformStoringService.store',
    index=0,
    containing_service=None,
    input_type=_WAVEFORMREQUEST,
    output_type=_WAVEFORMRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_WAVEFORMSTORINGSERVICE)

DESCRIPTOR.services_by_name['WaveformStoringService'] = _WAVEFORMSTORINGSERVICE

# @@protoc_insertion_point(module_scope)
