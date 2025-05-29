import pandas as pd
import ccxt
from datetime import datetime, timedelta
import vectorbt as vbt



client = ccxt.binance()

def backtest_data(symbol: str, interval: str, num_days: int):
    now = datetime.now().date()
    start = str(now - timedelta(days=num_days))
    
    data = client.fetch_ohlcv(symbol, interval)    
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index.tz_localize('UTC').tz_convert('Africa/Cairo')

    df = df[(df.index >= start)]

    return df



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

def macd_strategy(symbol: str, interval: str, num_days: int, cash: int, sl_percent: float, tp_percent: float):
    data = backtest_data(symbol, interval, num_days)
    macd_v = macd(data, 12, 26, 9)

    data['Entry'] = (macd_v['macd'] > macd_v['macdSignal']) & (macd_v['macd'].shift(1) < 0) & (macd_v['macdSignal'] > 0)
    data['Exit'] = (macd_v['macd'] < macd_v['macdSignal']) & (macd_v['macd'].shift(1) > 0) & (macd_v['macdSignal'] < 0)
    
    pf = vbt.Portfolio.from_signals(
    close=data['close'],
    entries=data['Entry'],
    exits=data['Exit'],
    init_cash=cash,
    fees=0.001,
    slippage=0.02,
    freq=interval,
    sl_stop=sl_percent,
    tp_stop=tp_percent
)
    val = pf.stats().to_dict()

    val = pd.DataFrame({'keys': list(val.keys()),
                       'values': list(val.values())})
    return pf, val



def bbands_strategy(symbol: str, interval: str, num_days: int, cash: int, sl_percent: float, tp_percent: float):
    data = backtest_data(symbol, interval, num_days)
    bbands_v = bbands(data, 15)
    
    data['Entry'] = (bbands_v['UB'] > bbands_v['LB'])
    data['Exit'] = (bbands_v['UB'] < bbands_v['LB'])
    
    pf = vbt.Portfolio.from_signals(
    close=data['close'],
    entries=data['Entry'],
    exits=data['Exit'],
    init_cash=cash,
    fees=0.001,
    slippage=0.02,
    freq=interval,
    sl_stop=sl_percent,
    tp_stop=tp_percent,
    short_entries=data['Exit'],
    short_exits=data['Entry']
)
    val = pf.stats().to_dict()

    # val = {'keys': list(val.keys()), 'values': list(val.values())}
    val = pd.Series(data=val, index=val.keys())

    # val = pd.DataFrame({'keys': list(val.keys()),
    #                    'values': list(val.values())})
    #
    # val = val.set_index('keys')

    return pf, val

# data = bbands_strategy('BTC/USDT', '30m', 50, 5555, 0.5, 0.5)

# df = data[1]
# plot = data[0].plot()

# print(df)