from enum import Enum
from typing import Literal


class BaseEnum(Enum):

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return getattr(self, "label", str(self.value))

    @classmethod
    def get_values(cls):
        return tuple(cls._value2member_map_.keys())

    @classmethod
    def literal(cls):
        return Literal[cls.get_values()]

    @classmethod
    def as_dict_list(cls):
        return [
            {
                "value": member.value,
                "label": getattr(member, "label", str(member.value))
            }
            for member in cls
        ]


class IntEnum(int, BaseEnum):

    def __new__(cls, value, label):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj


class StrEnum(str, BaseEnum):

    def __new__(cls, value, label):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj
