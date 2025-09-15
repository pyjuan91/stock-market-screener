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