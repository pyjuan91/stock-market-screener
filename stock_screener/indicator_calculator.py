import pandas_ta as ta
import pandas as pd

def add_macd(data: pd.DataFrame):
    """
    Calculates the MACD indicator and appends it to the DataFrame with simple names.
    """
    if data is not None:
        # This will append columns: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        data.ta.macd(append=True)
        # Rename to simple, predictable names for the frontend
        data.rename(columns={
            'MACD_12_26_9': 'MACD',
            'MACDs_12_26_9': 'MACD_Signal'
        }, inplace=True)
    return data

def add_rsi(data: pd.DataFrame):
    """
    Calculates the RSI indicator and appends it to the DataFrame with a simple name.
    """
    if data is not None:
        # This will append a column like 'RSI_14'
        data.ta.rsi(append=True)
        # Rename to a simple, predictable name
        data.rename(columns={'RSI_14': 'RSI'}, inplace=True)
    return data

def add_moving_averages(data: pd.DataFrame):
    """
    Calculates Simple Moving Averages (SMA) and appends them with simple names.
    """
    if data is not None:
        # Calculate SMA for 20 and 50 periods
        data.ta.sma(length=20, append=True)
        data.ta.sma(length=50, append=True)
        # Rename to simple, predictable names
        data.rename(columns={
            'SMA_20': 'MA20',
            'SMA_50': 'MA50'
        }, inplace=True)
    return data

def add_bollinger_bands(data: pd.DataFrame):
    """
    Calculates Bollinger Bands and appends them with simple names.
    """
    if data is not None:
        # This will append columns: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0, BBB_20_2.0, BBP_20_2.0
        data.ta.bbands(append=True)
        # Rename to simple, predictable names
        data.rename(columns={
            'BBL_20_2.0': 'BB_Lower',
            'BBM_20_2.0': 'BB_Middle',
            'BBU_20_2.0': 'BB_Upper'
        }, inplace=True)
    return data