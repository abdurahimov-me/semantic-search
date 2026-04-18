from utils.customs import IntEnum


class LogModel(IntEnum):
    ORDER = 1
    USER = 2
    CLIENT = 3
    OFFER = 5


class LogAction(IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    LOGIN = 4
    LOGOUT = 5
