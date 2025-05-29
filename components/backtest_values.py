from fasthtml.common import *
from monsterui.all import *
from fh_plotly import plotly2fasthtml
import pandas as pd
from mistletoe import markdown, HTMLRenderer

from lib.backtest import bbands_strategy, macd_strategy



def indicator_backtest(symbol: str, interval: str, 
                    num_days: int, cash: int,
                    sl_percent: float, tp_percent: float,
                    indicator):

    if indicator == 'BBands':
        bband = bbands_strategy(symbol, interval, num_days,
                cash, sl_percent, tp_percent)
        
        val = bband[1]
        chart = plotly2fasthtml(bband[0].plot())
        
    elif indicator == 'MACD':
        macd = macd_strategy(symbol, interval, num_days,
                cash, sl_percent, tp_percent)
        
        val = macd[1]
        chart = plotly2fasthtml(macd[0].plot())
        

    return DivCentered(chart, cls='w-full h-full screen-size: 100px; max-height: 1000px;'),(
        # Display in a div with styling  
        DivCentered(NotStr(val.to_frame().to_html(classes='table')), cls=TableT.striped)
    )