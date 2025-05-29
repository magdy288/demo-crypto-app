import pandas as pd
from fasthtml.common import *
from monsterui.all import *
from fh_plotly import plotly2fasthtml

from lib.dataframe import (
    plot_data
)
from lib.indicators import (
    rsi, rsi_plot, rsi_rbm,
    macd, macd_plot,
    bbands, bbands_plot,
    fibo_plot
)

def price_chart(df: pd.DataFrame, symbol: str):
    candle_chart = plotly2fasthtml(plot_data(df, symbol))

    return Div(candle_chart,
               cls='w-full h-full bg-red-500 screen-size: 100px; max-height: 1000px;')



def indicator_chart(df: pd.DataFrame, symbol: str, indicator):


    if indicator == 'RSI':
        chart = plotly2fasthtml(rsi_plot(df, rsi(df, 14), symbol))
        
        

    elif indicator == 'BBands':
        chart = plotly2fasthtml(bbands_plot(df, bbands(df, 14), symbol))

    elif indicator == 'MACD':
        chart = plotly2fasthtml(macd_plot(df, macd(df, 12, 26, 9), symbol))

    elif indicator == 'Fibonacci':
        chart = plotly2fasthtml(fibo_plot(df, symbol))

    return Div(chart, cls='w-full h-full bg-red-500 screen-size: 100px; max-height: 1000px;')