import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


## Calculate Bollinger-Bands
def bbands(data: pd.DataFrame, period: int):
    bbands = pd.DataFrame()
    # Calculate the 20-period Simple Moving Averages (SMA)
    bbands['SMA'] = data['close'].rolling(window=period).mean()

    # Calculate the 20-period Standard Deviation (SD)
    sd = data['close'].rolling(window=period).std()

    # Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
    bbands['UB'] = bbands['SMA'] + 2 * sd
    bbands['LB'] = bbands['SMA'] - 2 * sd

    # bbands = pd.concat([upper, lower], axis=1, names=['UB', 'LB'])
    # bbands.dropna(inplace=True)

    return bbands


def bbands_plot(data: pd.DataFrame, bbands: pd.DataFrame, symbol: str):
    # Create a Plotly figure
    fig = go.Figure()

    # Add the price chart
    fig.add_trace(go.Candlestick(
        x=data.index,  # date values
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']))

    # Add the Upper Bollinger Band (UB) and shade the area
    fig.add_trace(
        go.Scatter(x=data.index, y=bbands['UB'], mode='lines', name='Upper Bollinger Band', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data.index, y=bbands['LB'], fill='tonexty', mode='lines', name='Lower Bollinger Band',
                             line=dict(color='green')))

    # Add the Middle Bollinger Band (MA)
    fig.add_trace(
        go.Scatter(x=data.index, y=bbands['SMA'], mode='lines', name='Middle Bollinger Band', line=dict(color='blue')))

    # Customize the chart layout
    fig.update_layout(title=f'{symbol} Price with Bollinger Bands',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      showlegend=True)

    # Show the chart
    return fig





## Calculate MACD
def macd(data: pd.DataFrame, fast_preiod: int, slow_period: int, signal_period: int):
    slow_ema = data['close'].ewm(span=slow_period, adjust=False).mean()
    fast_ema = data['close'].ewm(span=fast_preiod, adjust=False).mean()

    macd = pd.DataFrame()

    macd['macd'] = fast_ema - slow_ema
    macd['macdSignal'] = macd['macd'].ewm(span=signal_period, adjust=False).mean()
    macd['macdHist'] = macd['macd'] - macd['macdSignal']

    macd.dropna(inplace=True)

    return macd


def macd_plot(data: pd.DataFrame, macd: pd.DataFrame, symbol: str):
    # Construct a 2 x 1 Plotly figure
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.4,
                        horizontal_spacing=0.1)

    # Candlestick chart for pricing
    fig.append_trace(go.Candlestick(x=data.index, open=data['open'], high=data['high'], low=data['low'],
                                    close=data['close'], showlegend=False), row=1, col=1)

    # Fast Signal (%k)
    fig.append_trace(go.Scatter(x=data.index, y=macd['macd'], line=dict(color='#C42836', width=1),
                                name='MACD Line'), row=2, col=1)

    # Slow signal (%d)
    fig.append_trace(go.Scatter(x=data.index, y=macd['macdSignal'], line=dict(color='limegreen', width=1),
                                name='Signal Line'), row=2, col=1)

    # Colorize the histogram values
    colors = np.where(macd['macd'] < 0, '#EA071C', '#57F219')

    # Plot the histogram
    fig.append_trace(go.Bar(x=data.index, y=macd['macdHist'], name='Histogram', marker_color=colors), row=2, col=1)

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


## Calculate RSI
def rsi(data: pd.DataFrame, period: int):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = pd.DataFrame()
    rsi['RSI'] = 100 - (100 / (1 + rs))
    rsi.dropna(inplace=True)

    return rsi


def rsi_plot(data: pd.DataFrame, rsi: pd.DataFrame, symbol: str):
    # Create a subplot figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        subplot_titles=("Price", "RSI"))

    # Add Close Price plot
    fig.add_trace(go.Candlestick(
        x=data.index,  # date values
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close']
    ), row=1, col=1)

    # Add RSI plot
    fig.add_trace(go.Scatter(
        x=data.index,
        y=rsi['RSI'],
        mode='lines',
        name='RSI',
        line=dict(color='orange')
    ), row=2, col=1)

    # Add horizontal lines for RSI thresholds
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)", row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f"{symbol} Price and RSI",
        xaxis2=dict(title="Date"),
        yaxis=dict(title="Price"),
        yaxis2=dict(title="RSI Value"),
        template="plotly_white",
        height=700
    )

    # show plot
    return fig


def rsi_rbm(rsi: pd.DataFrame):
    last_rsi = rsi['RSI'].iloc[-1]
    
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = last_rsi,
    title = {'text': "RSI"},
    domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    return fig

## Calculate fibonacci
def fibo(data: pd.DataFrame):
    low = data['close'].min()
    high = data['close'].max()
    diff = high - low

    fibonacci = pd.DataFrame()

    fibonacci['fib100'] = high
    fibonacci['fib764'] = low + (diff * 0.764)
    fibonacci['fib618'] = low + (diff * 0.618)
    fibonacci['fib50'] = low + (diff * 0.5)
    fibonacci['fib382'] = low + (diff * 0.382)
    fibonacci['fib236'] = low + (diff * 0.236)
    fibonacci['fib0'] = low

    return fibonacci


def fibo_plot(data: pd.DataFrame, symbol: str):
    # Create candlestick chart
    fig = go.Figure()

    # Add candlestick trace
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name="OHLC"
        )
    )

    # Calculate Fibonacci retracement levels
    # Find the highest high and lowest low in your dataset
    max_price = data['high'].max()
    min_price = data['low'].min()
    diff = max_price - min_price

    # Fibonacci retracement levels (standard levels: 0%, 23.6%, 38.2%, 50%, 61.8%, 100%)
    fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.764, 1]
    fib_prices = [max_price - level * diff for level in fib_levels]

    # Add Fibonacci retracement lines
    for i, (level, price) in enumerate(zip(fib_levels, fib_prices)):
        fig.add_shape(
            type="line",
            x0=data.index[0],
            y0=price,
            x1=data.index[-1],
            y1=price,
            line=dict(
                color="purple",
                width=1,
                dash="dash",
            ),
        )

        # Add labels for each Fibonacci level
        fig.add_annotation(
            x=data.index[-1],
            y=price,
            text=f"{level * 100}%: {price:.2f}",
            showarrow=False,
            xshift=50,
            font=dict(size=10, color="purple"),
        )

        # Update layout
    fig.update_layout(
        title=f"Fibonacci Retracement for {symbol} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        showlegend=False
    )

    # Show the figure
    return fig


