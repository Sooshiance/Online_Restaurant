from enum import  Enum


class Role(Enum):

    VENDOR = 1
    CUSTOMER = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
