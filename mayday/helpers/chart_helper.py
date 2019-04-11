import os
from collections import OrderedDict
from datetime import datetime

import pytz
from mayday.constants import CATEGORY_MAPPING, DATE_MAPPING, PRICE_MAPPING
from plotly import io as pio
from plotly.graph_objs import Bar, Figure, Layout
from plotly.graph_objs.layout import Title

TIMEZONE = pytz.timezone('Asia/Taipei')
# X -> Amount
# Y -> Date
# Color -> Prices

PRICE_COLORS = [
    'rgba(255, 0, 0, 1)', 'rgba(255, 127, 0, 1)',
    'rgba(255, 255, 0, 1)', 'rgba(0, 255, 0, 1)',
    'rgba(0, 0, 255, 1)', 'rgba(75, 0, 130, 1)',
    'rgba(143, 0, 255, 1)']

TITLE_TEXT = '{category}待交易數量分佈<br>更新時間: {updated_at}'


def sorting_stats_data(stats: dict) -> OrderedDict:
    return OrderedDict(sorted(stats.items(), key=lambda x: x[0]))


def generate_bar(data: dict) -> Bar:
    for price_id, stats in data.items():
        dates = sorted(stats.keys())
        amounts = [stats.get(x) for x in dates]
        yield Bar(
            y=list(map(DATE_MAPPING.get, dates)),
            x=amounts,
            name=PRICE_MAPPING.get(price_id),
            orientation='h',
            marker=dict(color=PRICE_COLORS[price_id - 1]))


def generate_ticket_graphs(ticket_distribution: dict, updated_at: int) -> list:
    os.makedirs('img', exist_ok=True)
    paths = list()
    for category_id, stats in sorting_stats_data(ticket_distribution).items():
        img_path = os.path.abspath('img/{}.png'.format(category_id))
        pio.write_image(
            file=img_path,
            fig=Figure(
                data=[bar for bar in generate_bar(stats)],
                layout=Layout(
                    barmode='stack',
                    title=Title(
                        text=TITLE_TEXT.format(
                            category=CATEGORY_MAPPING.get(category_id),
                            updated_at=datetime.fromtimestamp(updated_at).astimezone(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')),
                        xref='paper', x=0),
                )))
        if os.path.isfile(img_path):
            paths.append(img_path)
    return paths
