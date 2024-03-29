# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: measurements.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="measurements.proto",
    package="",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x12measurements.proto"\x85\x04\n\x16MeasurementApiProtobuf\x12/\n\x07\x63olumns\x18\x01 \x03(\x0b\x32\x1e.MeasurementApiProtobuf.Column\x12\x12\n\nrows_count\x18\x02 \x01(\r\x12\x14\n\x0c\x63urrent_page\x18\x03 \x01(\r\x12\x15\n\rrows_per_page\x18\x04 \x01(\r\x1aH\n\x06\x43olumn\x12\x0e\n\x06\x63olumn\x18\x01 \x01(\t\x12.\n\x06values\x18\x02 \x01(\x0b\x32\x1e.MeasurementApiProtobuf.Values\x1a\xc5\x01\n\x06Values\x12\x39\n\x07strings\x18\x01 \x01(\x0b\x32&.MeasurementApiProtobuf.RepeatedStringH\x00\x12\x37\n\x06\x66loats\x18\x02 \x01(\x0b\x32%.MeasurementApiProtobuf.RepeatedFloatH\x00\x12\x37\n\x06ints64\x18\x03 \x01(\x0b\x32%.MeasurementApiProtobuf.RepeatedInt64H\x00\x42\x0e\n\x0coneof_values\x1a\x1f\n\x0eRepeatedString\x12\r\n\x05\x61rray\x18\x01 \x03(\t\x1a"\n\rRepeatedFloat\x12\x11\n\x05\x61rray\x18\x01 \x03(\x02\x42\x02\x10\x01\x1a"\n\rRepeatedInt64\x12\x11\n\x05\x61rray\x18\x01 \x03(\x03\x42\x02\x10\x01\x62\x06proto3',
)


_MEASUREMENTAPIPROTOBUF_COLUMN = _descriptor.Descriptor(
    name="Column",
    full_name="MeasurementApiProtobuf.Column",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="column",
            full_name="MeasurementApiProtobuf.Column.column",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="values",
            full_name="MeasurementApiProtobuf.Column.values",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=163,
    serialized_end=235,
)

_MEASUREMENTAPIPROTOBUF_VALUES = _descriptor.Descriptor(
    name="Values",
    full_name="MeasurementApiProtobuf.Values",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="strings",
            full_name="MeasurementApiProtobuf.Values.strings",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="floats",
            full_name="MeasurementApiProtobuf.Values.floats",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="ints64",
            full_name="MeasurementApiProtobuf.Values.ints64",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="oneof_values",
            full_name="MeasurementApiProtobuf.Values.oneof_values",
            index=0,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        ),
    ],
    serialized_start=238,
    serialized_end=435,
)

_MEASUREMENTAPIPROTOBUF_REPEATEDSTRING = _descriptor.Descriptor(
    name="RepeatedString",
    full_name="MeasurementApiProtobuf.RepeatedString",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="array",
            full_name="MeasurementApiProtobuf.RepeatedString.array",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=437,
    serialized_end=468,
)

_MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT = _descriptor.Descriptor(
    name="RepeatedFloat",
    full_name="MeasurementApiProtobuf.RepeatedFloat",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="array",
            full_name="MeasurementApiProtobuf.RepeatedFloat.array",
            index=0,
            number=1,
            type=2,
            cpp_type=6,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\020\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=470,
    serialized_end=504,
)

_MEASUREMENTAPIPROTOBUF_REPEATEDINT64 = _descriptor.Descriptor(
    name="RepeatedInt64",
    full_name="MeasurementApiProtobuf.RepeatedInt64",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="array",
            full_name="MeasurementApiProtobuf.RepeatedInt64.array",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\020\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=506,
    serialized_end=540,
)

_MEASUREMENTAPIPROTOBUF = _descriptor.Descriptor(
    name="MeasurementApiProtobuf",
    full_name="MeasurementApiProtobuf",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="columns",
            full_name="MeasurementApiProtobuf.columns",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="rows_count",
            full_name="MeasurementApiProtobuf.rows_count",
            index=1,
            number=2,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="current_page",
            full_name="MeasurementApiProtobuf.current_page",
            index=2,
            number=3,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="rows_per_page",
            full_name="MeasurementApiProtobuf.rows_per_page",
            index=3,
            number=4,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[
        _MEASUREMENTAPIPROTOBUF_COLUMN,
        _MEASUREMENTAPIPROTOBUF_VALUES,
        _MEASUREMENTAPIPROTOBUF_REPEATEDSTRING,
        _MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT,
        _MEASUREMENTAPIPROTOBUF_REPEATEDINT64,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=23,
    serialized_end=540,
)

_MEASUREMENTAPIPROTOBUF_COLUMN.fields_by_name[
    "values"
].message_type = _MEASUREMENTAPIPROTOBUF_VALUES
_MEASUREMENTAPIPROTOBUF_COLUMN.containing_type = _MEASUREMENTAPIPROTOBUF
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "strings"
].message_type = _MEASUREMENTAPIPROTOBUF_REPEATEDSTRING
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "floats"
].message_type = _MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "ints64"
].message_type = _MEASUREMENTAPIPROTOBUF_REPEATEDINT64
_MEASUREMENTAPIPROTOBUF_VALUES.containing_type = _MEASUREMENTAPIPROTOBUF
_MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"].fields.append(
    _MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name["strings"]
)
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "strings"
].containing_oneof = _MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"]
_MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"].fields.append(
    _MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name["floats"]
)
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "floats"
].containing_oneof = _MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"]
_MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"].fields.append(
    _MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name["ints64"]
)
_MEASUREMENTAPIPROTOBUF_VALUES.fields_by_name[
    "ints64"
].containing_oneof = _MEASUREMENTAPIPROTOBUF_VALUES.oneofs_by_name["oneof_values"]
_MEASUREMENTAPIPROTOBUF_REPEATEDSTRING.containing_type = _MEASUREMENTAPIPROTOBUF
_MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT.containing_type = _MEASUREMENTAPIPROTOBUF
_MEASUREMENTAPIPROTOBUF_REPEATEDINT64.containing_type = _MEASUREMENTAPIPROTOBUF
_MEASUREMENTAPIPROTOBUF.fields_by_name[
    "columns"
].message_type = _MEASUREMENTAPIPROTOBUF_COLUMN
DESCRIPTOR.message_types_by_name["MeasurementApiProtobuf"] = _MEASUREMENTAPIPROTOBUF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MeasurementApiProtobuf = _reflection.GeneratedProtocolMessageType(
    "MeasurementApiProtobuf",
    (_message.Message,),
    {
        "Column": _reflection.GeneratedProtocolMessageType(
            "Column",
            (_message.Message,),
            {
                "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF_COLUMN,
                "__module__": "measurements_pb2"
                # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf.Column)
            },
        ),
        "Values": _reflection.GeneratedProtocolMessageType(
            "Values",
            (_message.Message,),
            {
                "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF_VALUES,
                "__module__": "measurements_pb2"
                # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf.Values)
            },
        ),
        "RepeatedString": _reflection.GeneratedProtocolMessageType(
            "RepeatedString",
            (_message.Message,),
            {
                "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF_REPEATEDSTRING,
                "__module__": "measurements_pb2"
                # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf.RepeatedString)
            },
        ),
        "RepeatedFloat": _reflection.GeneratedProtocolMessageType(
            "RepeatedFloat",
            (_message.Message,),
            {
                "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT,
                "__module__": "measurements_pb2"
                # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf.RepeatedFloat)
            },
        ),
        "RepeatedInt64": _reflection.GeneratedProtocolMessageType(
            "RepeatedInt64",
            (_message.Message,),
            {
                "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF_REPEATEDINT64,
                "__module__": "measurements_pb2"
                # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf.RepeatedInt64)
            },
        ),
        "DESCRIPTOR": _MEASUREMENTAPIPROTOBUF,
        "__module__": "measurements_pb2"
        # @@protoc_insertion_point(class_scope:MeasurementApiProtobuf)
    },
)
_sym_db.RegisterMessage(MeasurementApiProtobuf)
_sym_db.RegisterMessage(MeasurementApiProtobuf.Column)
_sym_db.RegisterMessage(MeasurementApiProtobuf.Values)
_sym_db.RegisterMessage(MeasurementApiProtobuf.RepeatedString)
_sym_db.RegisterMessage(MeasurementApiProtobuf.RepeatedFloat)
_sym_db.RegisterMessage(MeasurementApiProtobuf.RepeatedInt64)


_MEASUREMENTAPIPROTOBUF_REPEATEDFLOAT.fields_by_name["array"]._options = None
_MEASUREMENTAPIPROTOBUF_REPEATEDINT64.fields_by_name["array"]._options = None
# @@protoc_insertion_point(module_scope)
