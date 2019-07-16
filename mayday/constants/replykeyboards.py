from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from mayday.constants import STAT_URL


class ReplyKeyboards:

    def __init__(self):

        self._actions_keyboard = [
            [
                InlineKeyboardButton('搵門票🎫', callback_data='search'),
                InlineKeyboardButton('轉讓門票🤝', callback_data='post')
            ],
            [
                InlineKeyboardButton('快速搜索🔍', callback_data='quick_search'),
                InlineKeyboardButton('我的飛💎', callback_data='my_ticket'),
            ],
            [
                InlineKeyboardButton('門票總覽📊', url=STAT_URL),
                InlineKeyboardButton('五迷自發活動🙋', callback_data='events'),
            ],
            [
                InlineKeyboardButton('演唱會資訊ℹ️', callback_data='info')
            ]
        ]

        self._conditions_keyboard_mapping = {
            'date': InlineKeyboardMarkup([
                [InlineKeyboardButton('5.3(Fri)', callback_data=503),
                 InlineKeyboardButton('5.4(Sat)', callback_data=504),
                 InlineKeyboardButton('5.5(Sun)', callback_data=505)],
                [InlineKeyboardButton('5.10(Fri)', callback_data=510),
                 InlineKeyboardButton('5.11(Sat)', callback_data=511),
                 InlineKeyboardButton('5.12(Sun)', callback_data=512)],
            ], one_time_keyboard=True),

            'price': InlineKeyboardMarkup([
                [InlineKeyboardButton('$1180座位', callback_data=1),
                 InlineKeyboardButton('$880座位', callback_data=2)],
                [InlineKeyboardButton('$680座位', callback_data=3),
                 InlineKeyboardButton('$480座位', callback_data=4)],
                [InlineKeyboardButton('$680企位', callback_data=5)],
                [InlineKeyboardButton('$1180 無障礙通道座位', callback_data=6),
                 InlineKeyboardButton('$880 無障礙通道座位', callback_data=7)]
            ], one_time_keyboard=True),

            'quantity': InlineKeyboardMarkup([
                [InlineKeyboardButton('1', callback_data=1),
                 InlineKeyboardButton('2', callback_data=2)],
                [InlineKeyboardButton('3', callback_data=3),
                 InlineKeyboardButton('4', callback_data=4)],
            ], one_time_keyboard=True),

            'wish_dates': InlineKeyboardMarkup([
                [InlineKeyboardButton('5.3(Fri)', callback_data=503),
                 InlineKeyboardButton('5.4(Sat)', callback_data=504),
                 InlineKeyboardButton('5.5(Sun)', callback_data=505)],
                [InlineKeyboardButton('5.10(Fri)', callback_data=510),
                 InlineKeyboardButton('5.11(Sat)', callback_data=511),
                 InlineKeyboardButton('5.12(Sun)', callback_data=512)],
            ], one_time_keyboard=True),

            'wish_price_ids': InlineKeyboardMarkup([
                [InlineKeyboardButton('$1180座位', callback_data=1),
                 InlineKeyboardButton('$880座位', callback_data=2)],
                [InlineKeyboardButton('$680座位', callback_data=3),
                 InlineKeyboardButton('$480座位', callback_data=4)],
                [InlineKeyboardButton('$680企位', callback_data=5)],
                [InlineKeyboardButton('$1180 無障礙通道座位', callback_data=6),
                 InlineKeyboardButton('$880 無障礙通道座位', callback_data=7)]
            ], one_time_keyboard=True),

            'wish_quantities': InlineKeyboardMarkup([
                [InlineKeyboardButton('1', callback_data=1),
                 InlineKeyboardButton('2', callback_data=2)],
                [InlineKeyboardButton('3', callback_data=3),
                 InlineKeyboardButton('4', callback_data=4)],
            ], one_time_keyboard=True),

            'status': InlineKeyboardMarkup([
                [InlineKeyboardButton('待交易', callback_data=1),
                 InlineKeyboardButton('洽談中', callback_data=2)],
                [InlineKeyboardButton('已交易', callback_data=3),
                 InlineKeyboardButton('已取消', callback_data=4)],
            ], one_time_keyboard=True),

            'section': {
                # FIXME: Update Latest Seating Plan.
                1: InlineKeyboardMarkup([
                    [InlineKeyboardButton('A1', callback_data='A1'),
                     InlineKeyboardButton('A2', callback_data='A2')],
                    [InlineKeyboardButton('A3', callback_data='A3'),
                     InlineKeyboardButton('A4', callback_data='A4')],
                    [InlineKeyboardButton('B1', callback_data='B1'),
                     InlineKeyboardButton('B2', callback_data='B2')],
                    [InlineKeyboardButton('B3', callback_data='B3'),
                     InlineKeyboardButton('B4', callback_data='B4')]
                ]),
                2: InlineKeyboardMarkup([
                    [InlineKeyboardButton('C1', callback_data='C1'),
                     InlineKeyboardButton('F1', callback_data='F1'),
                     InlineKeyboardButton('F3', callback_data='F3')],
                    [InlineKeyboardButton('D1', callback_data='D1'),
                     InlineKeyboardButton('E1', callback_data='E1')],
                    [InlineKeyboardButton('D2', callback_data='D2'),
                     InlineKeyboardButton('E2', callback_data='E2')],
                    [InlineKeyboardButton('D3', callback_data='D3'),
                     InlineKeyboardButton('E3', callback_data='E3')],
                    [InlineKeyboardButton('D4', callback_data='D4'),
                     InlineKeyboardButton('E4', callback_data='E4')],
                    [InlineKeyboardButton('C2', callback_data='C2'),
                     InlineKeyboardButton('F2', callback_data='F2'),
                     InlineKeyboardButton('F4', callback_data='F4')],
                ]),
                3: InlineKeyboardMarkup([
                    [InlineKeyboardButton('H1', callback_data='H1'),
                     InlineKeyboardButton('K1', callback_data='K1')],
                ]),
                4: InlineKeyboardMarkup([
                    [InlineKeyboardButton('H1', callback_data='H1'),
                     InlineKeyboardButton('K2', callback_data='K2')],
                ]),
                5: InlineKeyboardMarkup([
                    [InlineKeyboardButton('G1', callback_data='G1'),
                     InlineKeyboardButton('G2', callback_data='G2')],
                ]),
                6: InlineKeyboardMarkup(
                    [InlineKeyboardButton('W-D1(輪椅區)', callback_data='W-D1'),
                     InlineKeyboardButton('W-D2(輪椅區)', callback_data='W-D2'),
                     InlineKeyboardButton('W-E1(輪椅區)', callback_data='W-E1')]
                ),
                7: InlineKeyboardMarkup([InlineKeyboardButton('W-A4(輪椅區)', callback_data='W-A4')]),
            },
            'source': InlineKeyboardMarkup([
                [InlineKeyboardButton('東亞信用卡', callback_data=1),
                 InlineKeyboardButton('特高娛樂內部認購', callback_data=2)],
                [InlineKeyboardButton('公開發售', callback_data=3),
                 InlineKeyboardButton('其他途徑', callback_data=4)],
            ],  one_time_keyboard=True),

            'category': InlineKeyboardMarkup([
                [InlineKeyboardButton('原價轉讓', callback_data=1),
                 InlineKeyboardButton('換飛', callback_data=2)]
            ],  one_time_keyboard=True)
        }

        self._search_ticket_keyboard = [
            [
                InlineKeyboardButton('門票類別', callback_data='category'),
                InlineKeyboardButton('門票狀態', callback_data='status'),
            ],
            [
                InlineKeyboardButton('日期', callback_data='date'),
                InlineKeyboardButton('票面價格', callback_data='price'),
                InlineKeyboardButton('數量', callback_data='quantity')
            ],
            [
                InlineKeyboardButton('重置', callback_data='reset'),
                InlineKeyboardButton('覆核', callback_data='check')
            ],
        ]

        self._update_ticket_keyboard = [
            [
                InlineKeyboardButton('門票狀態', callback_data='status'),
                InlineKeyboardButton('門票來源', callback_data='source'),
            ],
            [
                InlineKeyboardButton('日期', callback_data='date'),
                InlineKeyboardButton('票面價格', callback_data='price'),
                InlineKeyboardButton('數量', callback_data='quantity')
            ],
            [
                InlineKeyboardButton('區域', callback_data='section'),
                InlineKeyboardButton('行數', callback_data='row'),
                InlineKeyboardButton('備註', callback_data='remarks')
            ],
            [
                InlineKeyboardButton('覆核', callback_data='check')
            ]
        ]

        self._post_ticket_keyboard_mapping = {
            # 1: Selling
            1: InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('門票類別', callback_data='category'),
                        InlineKeyboardButton('門票來源', callback_data='source'),
                    ],
                    [
                        InlineKeyboardButton('日期', callback_data='date'),
                        InlineKeyboardButton('票面價格', callback_data='price'),
                        InlineKeyboardButton('數量', callback_data='quantity')
                    ],
                    [
                        InlineKeyboardButton('區域', callback_data='section'),
                        InlineKeyboardButton('行數', callback_data='row'),
                        InlineKeyboardButton('備註', callback_data='remarks')
                    ],
                    [
                        InlineKeyboardButton('重置', callback_data='reset'),
                        InlineKeyboardButton('覆核', callback_data='check')
                    ],
                ], one_time_keyboard=True),
            # 2: Exchange
            2: InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('門票類別', callback_data='category'),
                        InlineKeyboardButton('門票來源', callback_data='source'),
                    ],
                    [
                        InlineKeyboardButton('日期', callback_data='date'),
                        InlineKeyboardButton('票面價格', callback_data='price'),
                        InlineKeyboardButton('數量', callback_data='quantity')
                    ],
                    [
                        InlineKeyboardButton('區域', callback_data='section'),
                        InlineKeyboardButton('行數', callback_data='row'),
                        InlineKeyboardButton('備註', callback_data='remarks')
                    ],
                    [
                        InlineKeyboardButton('交換日期', callback_data='wish_dates'),
                        InlineKeyboardButton('交換價格類別', callback_data='wish_price_ids'),
                        InlineKeyboardButton('交換數量', callback_data='wish_quantities')
                    ],
                    [
                        InlineKeyboardButton('重置', callback_data='reset'),
                        InlineKeyboardButton('覆核', callback_data='check')
                    ],
                ], one_time_keyboard=True)
        }

        self._quick_search_start_keyboard = [
            [
                InlineKeyboardButton('用已儲存的條件搜索', callback_data='cached_condition'),
                InlineKeyboardButton('自動匹配門票交換', callback_data='matching_my_ticket')],
        ]

        self._quick_search_keyboard = [[InlineKeyboardButton('送出', callback_data='submit')]]

        self._before_post_submit_keyboard = [
            [
                InlineKeyboardButton('重置', callback_data='reset'),
                InlineKeyboardButton('送出', callback_data='submit')
            ]
        ]

        self._before_search_submit_keyboard = [
            [
                InlineKeyboardButton('儲存到快速搜索', callback_data='quick_search')
            ],
            [
                InlineKeyboardButton('重置', callback_data='reset'),
                InlineKeyboardButton('送出', callback_data='submit')
            ]
        ]

        self._after_submit_keyboard = [
            [
                InlineKeyboardButton('返上一層', callback_data='backward')
            ]
        ]
        self._support_events = [
            [InlineKeyboardButton('523上班餘興節目', callback_data='event_1')],
            [InlineKeyboardButton('《五月之約》尋回專屬HOME KONG場的感動', callback_data='event_2')],
        ]

    @property
    def actions_keyboard_markup(self):
        return InlineKeyboardMarkup(self._actions_keyboard)

    @property
    def search_ticket_keyboard_markup(self):
        return InlineKeyboardMarkup(self._search_ticket_keyboard, one_time_keyboard=True)

    @property
    def support_event_keyboard_markup(self):
        return InlineKeyboardMarkup(self._support_events, one_time_keyboard=True)

    @property
    def conditions_keyboard_mapping(self):
        return self._conditions_keyboard_mapping

    @property
    def post_ticket_keyboard_markup(self):
        return self._post_ticket_keyboard_mapping

    @property
    def quick_search_start_keyboard_markup(self):
        return InlineKeyboardMarkup(self._quick_search_start_keyboard, one_time_keyboard=True)

    @property
    def quick_search_keyboard_markup(self):
        return InlineKeyboardMarkup(self._quick_search_keyboard, one_time_keyboard=True)

    @property
    def update_ticket_keyboard_markup(self):
        return InlineKeyboardMarkup(self._update_ticket_keyboard, one_time_keyboard=True)

    @property
    def after_submit_keyboard(self):
        return InlineKeyboardMarkup(self._after_submit_keyboard, one_time_keyboard=True)

    @property
    def before_submit_post_keyboard_markup(self):
        return InlineKeyboardMarkup(self._before_post_submit_keyboard, one_time_keyboard=True)

    @property
    def before_submit_search_keyboard_markup(self):
        return InlineKeyboardMarkup(self._before_search_submit_keyboard, one_time_keyboard=True)


KEYBOARDS = ReplyKeyboards()
