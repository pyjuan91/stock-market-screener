from loguru import logger

from .data_fetcher import fetch_stock_data
from .indicator_calculator import add_macd, add_rsi, add_moving_averages, add_bollinger_bands


def run_ticker_analysis(ticker: str, period: str, interval: str):
    """
    Runs the analysis for a single stock ticker.
    1. Fetches data.
    2. Calculates indicators.
    3. Returns the latest data point with indicators.
    """
    logger.info(f"Starting analysis for {ticker}...")

    # 1. Fetch data
    data = fetch_stock_data(ticker, period=period, interval=interval)

    if data is None or data.empty:
        logger.warning(f"No data fetched for {ticker}. Skipping.")
        return None

    # 2. Calculate indicators
    data_with_indicators = add_macd(data)
    data_with_indicators = add_rsi(data_with_indicators)
    data_with_indicators = add_moving_averages(data_with_indicators)
    data_with_indicators = add_bollinger_bands(data_with_indicators)

    # 3. Return the last row of data as a dictionary
    if data_with_indicators is not None and not data_with_indicators.empty:
        logger.success(f"Analysis for {ticker} finished.")
        latest_data = data_with_indicators.iloc[-1].to_dict()
        latest_data['ticker'] = ticker # Add ticker symbol to the result
        return latest_data
    
    logger.warning(f"Indicator calculation failed for {ticker}.")
    return None


def get_historical_analysis(ticker: str, interval: str, tail: int = 60):
    """
    Runs analysis for a single stock and returns the trailing data points for charting.
    1. Fetches data for a fixed period suitable for charting.
    2. Calculates indicators.
    3. Returns the last N data points with indicators.
    """
    logger.info(f"Starting historical analysis for {ticker}...")

    # 1. Fetch data - use a longer, fixed period for meaningful charts
    data = fetch_stock_data(ticker, period="6mo", interval=interval)

    if data is None or data.empty:
        logger.warning(f"No data fetched for {ticker}. Skipping.")
        return None

    # 2. Calculate indicators
    data_with_indicators = add_macd(data)
    data_with_indicators = add_rsi(data_with_indicators)
    data_with_indicators = add_moving_averages(data_with_indicators)
    data_with_indicators = add_bollinger_bands(data_with_indicators)

    # 3. Prepare and return the last N rows
    if data_with_indicators is not None and not data_with_indicators.empty:
        # Drop rows with NaN from initial indicator calculations for cleaner chart data
        data_with_indicators = data_with_indicators.dropna()
        
        if data_with_indicators.empty:
            logger.warning(f"Not enough data for {ticker} after cleaning. Skipping.")
            return None

        # Reset index to make the datetime a column, and format it
        data_with_indicators = data_with_indicators.reset_index()
        
        # yfinance typically names the column 'Datetime' or 'Date'
        if 'Datetime' in data_with_indicators.columns:
             data_with_indicators['time'] = data_with_indicators['Datetime'].dt.strftime('%Y-%m-%d %H:%M')
             data_with_indicators = data_with_indicators.drop(columns=['Datetime'])
        elif 'Date' in data_with_indicators.columns:
             data_with_indicators['time'] = data_with_indicators['Date'].dt.strftime('%Y-%m-%d')
             data_with_indicators = data_with_indicators.drop(columns=['Date'])

        logger.success(f"Historical analysis for {ticker} finished.")
        # Return the last `tail` number of records
        return data_with_indicators.tail(tail).to_dict(orient='records')
    
    logger.warning(f"Indicator calculation failed for {ticker}.")
    return None