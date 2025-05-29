from fasthtml.common import *
from monsterui.all import *

from components.layout import page_layout
from components.charts import indicator_chart

from lib.indicators import (
    rsi,macd,bbands,fibo
)

from lib.dataframe import get_data

def analysis_routes(rt):

    @rt('/analysis')
    def get():

        form = Form(
            Div(
                LabelInput("Stock Symbol:", name="symbol", placeholder="e.g., BTC/USDT"),

                Br(),


                LabelSelect(
                  Option("1m", value="1m"),
                  Option("5m", value="5m"),
                  Option("15m", value="15m"),
                  Option("30m", value="30m"),
                  Option("1h", value="1h"),
                  Option("4h", value="4h"),
                  Option("1d", value="1d"),
                  label="Interval:",
                  name="interval",
                  cls = 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                ),

                Br(),

                LabelSelect(
                    Option('RSI', value='RSI'),
                    Option('Bollinger-Bands', value='BBands'),
                    Option('MACD', value='MACD'),
                    Option('Fibonacci', value='Fibonacci'),
                    label='Indicators: ',
                    name='indicator',
                    cls = 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ),

                Br(),

                # LabelSelect(
                #     Option('RSI ', value='RSI'),
                #     Option('Bollinger-Bands', value='BBands'),
                #     Option('MACD', value='MACD'),
                #     Option('Fibonacci', value='Fibonacci'),
                #     label='Indicators: ',
                #     name='indicator',
                #     cls = 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500'
                #     ),
                
                Button('View Data', type='submit',
                       hx_target='#analysis-area',
                       hx_post='/analysis/chart',
                       cls=ButtonT.primary)
                ),

        )


        contenet = [
            H1("Technical Analysis"),
            Br(),
            P("Select a stock and indicators to analyze",
              cls=TextPresets.bold_lg),
            Br(),
            form,
            Br(),
            Div(id="analysis-area")
        ]

        return page_layout(
            'Technical Analysis',
            *contenet
        )


    @rt('/analysis/chart')
    def post(symbol: str, interval: str, indicator: str):
            crypto_data = get_data(symbol, interval)

            return indicator_chart(crypto_data, symbol, indicator)