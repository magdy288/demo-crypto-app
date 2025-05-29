from fasthtml.common import *
from monsterui.all import *

from components.layout import page_layout
from components.backtest_values import indicator_backtest

from lib.backtest import backtest_data, bbands_strategy, macd_strategy

def backtest_routes(rt):

    @rt('/backtest')
    def get():
        
        form = Form(
            LabelInput('Symbol', name="symbol",
                   ),
            # Br(),

            LabelSelect(
                Option("1m", value="1m"),
                Option("5m", value="5m"),
                Option("15m", value="15m"),
                Option("30m", value="30m"),
                Option("1h", value="1h"),
                Option("4h", value="4h"),
                Option("1d", value="1d"),
                name="interval",
                label='TimeFrame',

            ),

            Br(),

            LabelSelect(
                Option('Bollinger-Bands', value='BBands'),
                Option('MACD', value='MACD'),
                label='Indicators: ',
                name='indicator',
                ),
            
            LabelInput('Number of Days', type='number', name='num_days'),
            
            LabelInput('Cash', type='number', name='cash'),
            
            
            LabelInput('Stop-Loss Percentage', type='float', name='sl_percent'),
            
            LabelInput('Take-Profit Percentage', type='float', name='tp_percent'),
            
            
            Br(),
            
            
            
            DivCentered(Button('Load Chart', type='submit',
                   cls=ButtonT.primary)),

            hx_post='/backtest/values',
            hx_target = '#backtest-area',
            cls='space-y-4'
        )

        content = [
        H1('Crypto Backtest'),
        Br(),
        form,
        Div(id='backtest-area')
        ]
        
        return page_layout('Backtesting', *content)


    @rt('/backtest/values')
    def post(symbol: str, interval: str, num_days: int, cash: int, sl_percent: float, tp_percent: float, indicator: str):
        
        return indicator_backtest(symbol, interval, num_days,
                                  cash, sl_percent, 
                                  tp_percent, indicator)