import pandas as pd

def moving_average(df, short_window,long_window):
    df['short_ma']=df['close'].rolling(window=short_window).mean()
    df['long_ma']=df['close'].rolling(window=long_window).mean()
    return df
    