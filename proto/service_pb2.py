# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x07tech_ex\"(\n\x07Message\x12\x0c\n\x04role\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"|\n\x0b\x43hatRequest\x12\"\n\x08messages\x18\x01 \x03(\x0b\x32\x10.tech_ex.Message\x12\r\n\x05model\x18\x02 \x01(\t\x12\x12\n\nmax_tokens\x18\x03 \x01(\x05\x12\x13\n\x0btemperature\x18\x04 \x01(\x02\x12\x11\n\tapi_token\x18\x05 \x01(\t\"T\n\x0c\x43hatResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1b\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\r.tech_ex.Data\x12\x16\n\x0e\x65xecution_time\x18\x03 \x01(\x02\"&\n\x04\x44\x61ta\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\t2B\n\x0b\x43hatService\x12\x33\n\x04\x43hat\x12\x14.tech_ex.ChatRequest\x1a\x15.tech_ex.ChatResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MESSAGE']._serialized_start=26
  _globals['_MESSAGE']._serialized_end=66
  _globals['_CHATREQUEST']._serialized_start=68
  _globals['_CHATREQUEST']._serialized_end=192
  _globals['_CHATRESPONSE']._serialized_start=194
  _globals['_CHATRESPONSE']._serialized_end=278
  _globals['_DATA']._serialized_start=280
  _globals['_DATA']._serialized_end=318
  _globals['_CHATSERVICE']._serialized_start=320
  _globals['_CHATSERVICE']._serialized_end=386
# @@protoc_insertion_point(module_scope)
