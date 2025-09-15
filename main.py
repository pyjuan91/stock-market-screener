import pandas as pd
from loguru import logger
from stock_screener.data_fetcher import fetch_stock_data
from stock_screener.indicator_calculator import add_macd

# Set pandas options for better display
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)


def run_analysis():
    logger.info("Starting analysis run...")
    ticker = "AAPL"

    # 1. Fetch data (now with flexible period and interval)
    # Let's get the last month of hourly data as an example
    data = fetch_stock_data(ticker, period="1mo", interval="1h")

    # 2. Calculate indicators
    data_with_macd = add_macd(data)

    if data_with_macd is not None:
        logger.info(f"Displaying the last 5 hours of data for {ticker} with MACD:")
        print(data_with_macd.tail())

    logger.success("Analysis run finished.")


if __name__ == "__main__":
    run_analysis()
