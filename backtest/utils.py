import pandas as pd

def moving_average(df, short_window,long_window,resample_interval='1h'):
    df['date'] = pd.to_datetime(df['date'])
    
    # Set the 'date' column as the index for resampling
    df.set_index('date', inplace=True)
    
    # Resample data to the specified interval
    ohlc_resampled = df.resample(resample_interval).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    
    # Reset the index after resampling
    ohlc_resampled.reset_index(inplace=True)
    
    # Calculate moving averages on the resampled data
    ohlc_resampled['short_ma'] = ohlc_resampled['close'].rolling(window=short_window).mean()
    ohlc_resampled['long_ma'] = ohlc_resampled['close'].rolling(window=long_window).mean()
    
    # Add buy/sell signal columns
    ohlc_resampled['signal'] = 0
    ohlc_resampled.loc[ohlc_resampled['short_ma'] > ohlc_resampled['long_ma'], 'signal'] = 1
    ohlc_resampled.loc[ohlc_resampled['short_ma'] < ohlc_resampled['long_ma'], 'signal'] = -1

    return ohlc_resampled

    