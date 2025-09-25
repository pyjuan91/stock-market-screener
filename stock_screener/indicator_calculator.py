import pandas_ta as ta
import pandas as pd

def add_macd(data: pd.DataFrame):
    """
    Calculates the MACD indicator and appends it to the DataFrame.
    """
    if data is not None:
        # Calculate MACD using pandas_ta
        # This will append columns: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        data.ta.macd(append=True)
    return data

def add_rsi(data: pd.DataFrame):
    """
    Calculates the RSI indicator and appends it to the DataFrame.
    """
    if data is not None:
        # Calculate RSI using pandas_ta
        # This will append a column like 'RSI_14'
        data.ta.rsi(append=True)
    return data

def add_moving_averages(data: pd.DataFrame):
    """
    Calculates Simple Moving Averages (SMA) and appends them to the DataFrame.
    """
    if data is not None:
        # Calculate SMA for 20 and 50 periods
        data.ta.sma(length=20, append=True)
        data.ta.sma(length=50, append=True)
    return data