from utils.customs import IntEnum


class LogModel(IntEnum):
    ORDER = 1, "Buyurtmalar"
    USER = 2, "Foydalanuvchilar"
    CLIENT = 3, "Klientlar"
    OFFER = 5, "Takliflar"


class LogAction(IntEnum):
    CREATE = 1, "Yaratildi"
    UPDATE = 2, "O'zgartirildi"
    DELETE = 3, "O'chirildi"
    LOGIN = 4, "Kirish"
    LOGOUT = 5, "Chiqish"
