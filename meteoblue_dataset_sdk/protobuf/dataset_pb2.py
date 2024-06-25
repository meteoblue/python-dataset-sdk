# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: dataset.proto
# Protobuf Python Version: 5.27.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    0,
    '',
    'dataset.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rdataset.proto\"\xdc\x05\n\x12\x44\x61tasetApiProtobuf\x12\x30\n\ngeometries\x18\x01 \x03(\x0b\x32\x1c.DatasetApiProtobuf.Geometry\x1a\xed\x01\n\x08Geometry\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0c\n\x04lats\x18\x02 \x03(\x02\x12\x0c\n\x04lons\x18\x03 \x03(\x02\x12\x0c\n\x04\x61sls\x18\x04 \x03(\x02\x12\x15\n\rlocationNames\x18\x05 \x03(\t\x12\n\n\x02nx\x18\x06 \x01(\x12\x12\n\n\x02ny\x18\x07 \x01(\x12\x12\x16\n\x0etimeResolution\x18\x08 \x01(\t\x12\x37\n\rtimeIntervals\x18\t \x03(\x0b\x32 .DatasetApiProtobuf.TimeInterval\x12\'\n\x05\x63odes\x18\n \x03(\x0b\x32\x18.DatasetApiProtobuf.Code\x1aO\n\x0cTimeInterval\x12\x13\n\x0btimestrings\x18\x01 \x03(\t\x12\r\n\x05start\x18\x02 \x01(\x12\x12\x0b\n\x03\x65nd\x18\x03 \x01(\x12\x12\x0e\n\x06stride\x18\x04 \x01(\x03\x1a\xa6\x02\n\x04\x43ode\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\r\n\x05level\x18\x02 \x01(\t\x12\x10\n\x08variable\x18\x03 \x01(\t\x12\x0c\n\x04unit\x18\x04 \x01(\t\x12\x13\n\x0b\x61ggregation\x18\x05 \x01(\t\x12/\n\rtimeIntervals\x18\x06 \x03(\x0b\x32\x18.DatasetApiProtobuf.Time\x12\x0f\n\x07gddBase\x18\x07 \x01(\x02\x12\x10\n\x08gddLimit\x18\x08 \x01(\x02\x12\r\n\x05slope\x18\t \x01(\x02\x12\x0e\n\x06\x66\x61\x63ing\x18\n \x01(\x02\x12\x0e\n\x06kwPeak\x18\x0b \x01(\x02\x12\x12\n\nstartDepth\x18\x0c \x01(\x03\x12\x10\n\x08\x65ndDepth\x18\r \x01(\x03\x12\x12\n\nefficiency\x18\x0e \x01(\x02\x12\x0f\n\x07tracker\x18\x0f \x01(\x03\x1a*\n\x04Time\x12\x14\n\x0cgapFillRatio\x18\x01 \x01(\x02\x12\x0c\n\x04\x64\x61ta\x18\x02 \x03(\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dataset_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATASETAPIPROTOBUF']._serialized_start=18
  _globals['_DATASETAPIPROTOBUF']._serialized_end=750
  _globals['_DATASETAPIPROTOBUF_GEOMETRY']._serialized_start=91
  _globals['_DATASETAPIPROTOBUF_GEOMETRY']._serialized_end=328
  _globals['_DATASETAPIPROTOBUF_TIMEINTERVAL']._serialized_start=330
  _globals['_DATASETAPIPROTOBUF_TIMEINTERVAL']._serialized_end=409
  _globals['_DATASETAPIPROTOBUF_CODE']._serialized_start=412
  _globals['_DATASETAPIPROTOBUF_CODE']._serialized_end=706
  _globals['_DATASETAPIPROTOBUF_TIME']._serialized_start=708
  _globals['_DATASETAPIPROTOBUF_TIME']._serialized_end=750
# @@protoc_insertion_point(module_scope)
