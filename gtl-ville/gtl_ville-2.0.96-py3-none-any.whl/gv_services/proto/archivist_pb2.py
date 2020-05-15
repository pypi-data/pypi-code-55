# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gv_services/proto/archivist.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gv_services/proto/archivist.proto',
  package='gv_services.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n!gv_services/proto/archivist.proto\x12\x11gv_services.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xbc\x01\n\x12TrafficDataRequest\x12\x10\n\x08\x64\x61tatype\x18\x01 \x01(\t\x12,\n\x08\x66romdate\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06todate\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04\x66req\x18\x04 \x01(\x05\x12\x0e\n\x06noeids\x18\x05 \x01(\x08\x12\x0c\n\x04\x61rea\x18\x06 \x01(\x0c\x12\x0e\n\x06window\x18\x07 \x01(\x05\"3\n\x0bTrafficData\x12\x13\n\x0btrafficdata\x18\x01 \x01(\x0c\x12\x0f\n\x07\x61pplyto\x18\x02 \x01(\t\"&\n\x12\x44\x61taQualityRequest\x12\x10\n\x08\x64\x61tatype\x18\x01 \x01(\t\"\"\n\x0b\x44\x61taQuality\x12\x13\n\x0b\x64\x61taquality\x18\x01 \x01(\x0c\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_TRAFFICDATAREQUEST = _descriptor.Descriptor(
  name='TrafficDataRequest',
  full_name='gv_services.proto.TrafficDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='datatype', full_name='gv_services.proto.TrafficDataRequest.datatype', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fromdate', full_name='gv_services.proto.TrafficDataRequest.fromdate', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='todate', full_name='gv_services.proto.TrafficDataRequest.todate', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='freq', full_name='gv_services.proto.TrafficDataRequest.freq', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='noeids', full_name='gv_services.proto.TrafficDataRequest.noeids', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='area', full_name='gv_services.proto.TrafficDataRequest.area', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window', full_name='gv_services.proto.TrafficDataRequest.window', index=6,
      number=7, type=5, cpp_type=1, label=1,
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
  serialized_start=90,
  serialized_end=278,
)


_TRAFFICDATA = _descriptor.Descriptor(
  name='TrafficData',
  full_name='gv_services.proto.TrafficData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trafficdata', full_name='gv_services.proto.TrafficData.trafficdata', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='applyto', full_name='gv_services.proto.TrafficData.applyto', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=280,
  serialized_end=331,
)


_DATAQUALITYREQUEST = _descriptor.Descriptor(
  name='DataQualityRequest',
  full_name='gv_services.proto.DataQualityRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='datatype', full_name='gv_services.proto.DataQualityRequest.datatype', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=333,
  serialized_end=371,
)


_DATAQUALITY = _descriptor.Descriptor(
  name='DataQuality',
  full_name='gv_services.proto.DataQuality',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dataquality', full_name='gv_services.proto.DataQuality.dataquality', index=0,
      number=1, type=12, cpp_type=9, label=1,
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
  serialized_start=373,
  serialized_end=407,
)

_TRAFFICDATAREQUEST.fields_by_name['fromdate'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_TRAFFICDATAREQUEST.fields_by_name['todate'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['TrafficDataRequest'] = _TRAFFICDATAREQUEST
DESCRIPTOR.message_types_by_name['TrafficData'] = _TRAFFICDATA
DESCRIPTOR.message_types_by_name['DataQualityRequest'] = _DATAQUALITYREQUEST
DESCRIPTOR.message_types_by_name['DataQuality'] = _DATAQUALITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrafficDataRequest = _reflection.GeneratedProtocolMessageType('TrafficDataRequest', (_message.Message,), dict(
  DESCRIPTOR = _TRAFFICDATAREQUEST,
  __module__ = 'gv_services.proto.archivist_pb2'
  # @@protoc_insertion_point(class_scope:gv_services.proto.TrafficDataRequest)
  ))
_sym_db.RegisterMessage(TrafficDataRequest)

TrafficData = _reflection.GeneratedProtocolMessageType('TrafficData', (_message.Message,), dict(
  DESCRIPTOR = _TRAFFICDATA,
  __module__ = 'gv_services.proto.archivist_pb2'
  # @@protoc_insertion_point(class_scope:gv_services.proto.TrafficData)
  ))
_sym_db.RegisterMessage(TrafficData)

DataQualityRequest = _reflection.GeneratedProtocolMessageType('DataQualityRequest', (_message.Message,), dict(
  DESCRIPTOR = _DATAQUALITYREQUEST,
  __module__ = 'gv_services.proto.archivist_pb2'
  # @@protoc_insertion_point(class_scope:gv_services.proto.DataQualityRequest)
  ))
_sym_db.RegisterMessage(DataQualityRequest)

DataQuality = _reflection.GeneratedProtocolMessageType('DataQuality', (_message.Message,), dict(
  DESCRIPTOR = _DATAQUALITY,
  __module__ = 'gv_services.proto.archivist_pb2'
  # @@protoc_insertion_point(class_scope:gv_services.proto.DataQuality)
  ))
_sym_db.RegisterMessage(DataQuality)


# @@protoc_insertion_point(module_scope)
