from fasthtml.common import *
from monsterui.all import *
from components.layout import page_layout
from components.charts import price_chart
from lib.dataframe import get_data

def crypto_routes(rt):

    @rt('/crypto')
    def get():


        form = Form(
            LabelInput('Symbol', name="symbol",
                   ),
            Br(),

            LabelSelect(
                Option("1m", value="1m"),
                Option("5m", value="5m"),
                Option("15m", value="15m"),
                Option("30m", value="30m"),
                Option("1h", value="1h"),
                Option("4h", value="4h"),
                Option("1d", value="1d"),
                name="interval",

            ),

            Br(),

            LabelInput('Date', type='number', name='num_days'),
            
            Button('Load Chart', type='submit',
                   cls=ButtonT.primary),

            hx_post='/crypto/chart',
            hx_target = '#chart-area'
        )

        content = [
            H1('Crypto Charts'),
            Br(),
            form,
            Div(id='chart-area')
        ]

        return page_layout('crypto', *content)

    @rt('/crypto/chart')
    def post(symbol: str, interval: str):
        crypto_data = get_data(symbol, interval)

        return price_chart(crypto_data, symbol)
    
    