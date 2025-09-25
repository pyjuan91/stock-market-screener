from loguru import logger

from .data_fetcher import fetch_stock_data
from .indicator_calculator import add_macd, add_rsi, add_moving_averages


def run_ticker_analysis(ticker: str, period: str, interval: str):
    """
    Runs the analysis for a single stock ticker.
    1. Fetches data.
    2. Calculates indicators.
    3. Prints the results.
    """
    logger.info(f"Starting analysis for {ticker}...")

    # 1. Fetch data
    data = fetch_stock_data(ticker, period=period, interval=interval)

    if data is None:
        return  # Error already logged in fetch_stock_data

    # 2. Calculate indicators
    data_with_indicators = add_macd(data)
    data_with_indicators = add_rsi(data_with_indicators)
    data_with_indicators = add_moving_averages(data_with_indicators)

    # 3. Display results
    if data_with_indicators is not None:
        logger.info(f"Displaying the last 5 data points for {ticker} with indicators:")
        print(data_with_indicators.tail())

    logger.success(f"Analysis for {ticker} finished.")
