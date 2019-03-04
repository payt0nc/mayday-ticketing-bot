CATEGORY_MAPPING = {
    1: '原價轉讓',
    2: '換飛'
}

DATE_MAPPING = {
    504: '5.4(Fri)',
    505: '5.5(Sat)',
    506: '5.6(Sun)',
    511: '5.11(Fri)',
    512: '5.12(Sat)',
    513: '5.13(Sun)'
}

PRICE_MAPPING = {
    1: '$1180座位',
    2: '$880座位',
    3: '$680座位',
    4: '$680企位',
    5: '$480座位'
}

STATUS_MAPPING = {
    1: '待交易',
    2: '洽談中',
    3: '已交易',
    4: '已取消'
}

TICKET_MAPPING = {
    'category_id': '門票類型',
    'status_id': '門票狀態',
    'date': '日期',
    'price_id': '票面價格',
    'quantity': '數量',
    'section': '座位區域',
    'row': '座位行數',
    'remarks': '備註',
    'update_at': '更新時間',
    'wish_date': '希望交換的日期',
    'wish_price_id': '希望交換的價格種類',
    'wish_quantity': '希望交換的數量'
}


class Query:

    def __init__(self, user_id, username):
        self.category_id = ''
        self.date = []
        self.price_id = []
        self.status = ''
        self.quantity = []
        self.user_id = int(user_id)
        self.username = str(username)

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'date': self.date,
            'price_id': self.price_id,
            'quantity': self.quantity,
            'status_id': self.status,
            'username': self.username,
            'user_id': self.user_id,
        }


class Ticket:
    def __init__(self, user_id, username):
        self.category_id = ''
        self.date = ''
        self.price_id = ''
        self.quantity = ''
        self.section = ''
        self.row = ''
        self.seat = ''
        self.wish_date = []
        self.wish_price_id = []
        self.wish_quantity = []
        self.status = 1
        self.remarks = ''
        self.user_id = int(user_id)
        self.username = str(username)

    def to_dict(self):
        return {
            'category_id': self.category_id,
            'date': self.date,
            'price_id': self.price_id,
            'quantity': self.quantity,
            'section': self.section,
            'row': self.row,
            'seat': self.seat,
            'status_id': self.status,
            'remarks': self.remarks,
            'wish_date': self.wish_date,
            'wish_price_id': self.wish_price_id,
            'wish_quantity': self.wish_quantity,
            'user_id': int(self.user_id),
            'username': str(self.username)
        }
