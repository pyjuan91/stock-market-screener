import yfinance as yf
from loguru import logger


def fetch_stock_data(ticker_symbol: str, period: str = "max", interval: str = "1d"):
    """
    Fetches historical stock data for a given ticker symbol and interval.

    :param ticker_symbol: The stock ticker (e.g., 'AAPL').
    :param period: The time period to fetch (e.g., '1mo', '1y', 'max').
    :param interval: The data interval (e.g., '1m', '15m', '1h', '1d').
    """
    logger.info(f"Fetching {interval} data for {ticker_symbol} (Period: {period})...")
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period=period, interval=interval)

    if data.empty:
        logger.warning(f"No data found for {ticker_symbol} with the given parameters.")
        return None

    logger.success(f"Successfully fetched {len(data)} rows of data.")
    return data
