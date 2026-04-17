from google.protobuf.struct_pb2 import Struct


def dict_to_struct(data: dict) -> Struct:
    s = Struct()
    s.update(data or {})
    return s