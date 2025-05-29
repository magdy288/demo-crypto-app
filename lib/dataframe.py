import ccxt
import pandas as pd
import plotly.graph_objects as go

from fastlite import database

client = ccxt.bybit()

db = database('data/cryptos.db')
cryptos = db.t.cryptos

if cryptos not in db.t:
    cryptos.create(
        id=int,
        symbol=str,
        interval=str,
        date=str,
        open=float,
        high=float,
        low=float,
        close=float,
        volume=int,
        pk='id'
    )

def get_data(symbol: str, interval: str):
    data = client.fetch_ohlcv(symbol, interval)

    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index.tz_localize('UTC').tz_convert('Africa/Cairo')

    return df


def get_market_overview():

    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'TRUMP/USDT']
    overview = []

    for symbol in symbols:
        ticker = client.fetch_ticker(symbol)

        overview.append({
            'symbol': symbol,
            'ask': ticker['ask'],
            'bid': ticker['bid'],
            'last_price': ticker['last'],
            'pct_change': ticker['percentage'],
            'change': ticker['change'],
        })

    return overview


def get_available_symbols():
    """Get list of available stock symbols"""
    return ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'TRUMP/USDT']





def plot_data(data: pd.DataFrame, symbol: str):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,  # date values
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='purple',
        decreasing_line_color='orange',
        name='Candlesticks')])

    # Add a title
    fig.update_layout(
        title=f"{symbol} Price Candlestick Chart",
        title_x=0.5,  # Center the title

        # Customize the font and size of the title
        title_font=dict(size=24, family="Arial"),

        # Set the background color of the plot
        plot_bgcolor='white',

        # Customize the grid lines
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    )

    return fig