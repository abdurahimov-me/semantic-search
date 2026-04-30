from utils.customs import IntEnum


class LogModel(IntEnum):
    ORDER = 1, "Order"
    USER = 2, "User"
    CLIENT = 3, "Client"
    OFFER = 5, "Offer"
    DemurrageFee = 6, "Demurrage fee"
    INVOICE = 7, "Invoice"
    ORDER_CHECK = 8, "Order check"
    EXTRA_CASH_FLOW = 9, "Extra cash flow"
    AGENT_CASH_FLOW = 10, "Agent cash flow"
    UN_LOADING_POINT = 11, "Un loading point"
    LOADING_POINT = 12, "Loading point"
    CONTRACT = 13, "Contract"


class LogAction(IntEnum):
    CREATE = 1, "Yaratildi"
    UPDATE = 2, "O'zgartirildi"
    DELETE = 3, "O'chirildi"
    LOGIN = 4, "Kirish"
    LOGOUT = 5, "Chiqish"
