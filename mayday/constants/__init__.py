CATEGORY_MAPPING = {
    1: '原價轉讓',
    2: '換飛'
}

DATE_MAPPING = {
    503: '5.3(Fri)',
    504: '5.4(Sat)',
    505: '5.5(Sun)',
    510: '5.10(Fri)',
    511: '5.11(Sat)',
}

PRICE_MAPPING = {
    1: '$1180座位',
    2: '$880座位',
    3: '$680座位',
    4: '$480座位',
    5: '$680企位',
    6: '$1180 無障礙通道座位門票',
    7: '$880 無障礙通道座位門票'
}

STATUS_MAPPING = {
    1: '待交易',
    2: '洽談中',
    3: '已交易',
    4: '已取消',
    5: '黃牛飛'
}

TICKET_MAPPING = dict(
    category='門票類型',
    status='門票狀態',
    date='日期',
    price='票面價格',
    quantity='數量',
    section='座位區域',
    row='座位行數',
    remarks='備註',
    update_at='更新時間',
    wish_date='希望交換的日期',
    wish_price_id='希望交換的價格種類',
    wish_quantity='希望交換的數量'
)
