# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: image_gen.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'image_gen.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fimage_gen.proto\x12\x08imagegen\"K\n\x0bTextRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontext\x18\x02 \x01(\t\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\".\n\rImageResponse\x12\r\n\x05image\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\"\x1d\n\x0cVideoRequest\x12\r\n\x05image\x18\x01 \x01(\t\".\n\rVideoResponse\x12\r\n\x05video\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t2\x93\x01\n\x0eImageGenerator\x12?\n\rGenerateImage\x12\x15.imagegen.TextRequest\x1a\x17.imagegen.ImageResponse\x12@\n\rGenerateVideo\x12\x16.imagegen.VideoRequest\x1a\x17.imagegen.VideoResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'image_gen_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TEXTREQUEST']._serialized_start=29
  _globals['_TEXTREQUEST']._serialized_end=104
  _globals['_IMAGERESPONSE']._serialized_start=106
  _globals['_IMAGERESPONSE']._serialized_end=152
  _globals['_VIDEOREQUEST']._serialized_start=154
  _globals['_VIDEOREQUEST']._serialized_end=183
  _globals['_VIDEORESPONSE']._serialized_start=185
  _globals['_VIDEORESPONSE']._serialized_end=231
  _globals['_IMAGEGENERATOR']._serialized_start=234
  _globals['_IMAGEGENERATOR']._serialized_end=381
# @@protoc_insertion_point(module_scope)
