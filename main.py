import argparse
import pandas as pd
from loguru import logger

from stock_screener.screener import run_ticker_analysis

def main():
    """
    Main function to parse arguments and run the stock analysis.
    """
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Stock Screener CLI")
    parser.add_argument(
        "ticker",
        type=str,
        help="The stock ticker symbol to analyze (e.g., 'AAPL')."
    )
    parser.add_argument(
        "--period",
        type=str,
        default="1mo",
        help="The time period to fetch (e.g., '1d', '5d', '1mo', '1y', 'max')."
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="1h",
        help="The data interval (e.g., '1m', '15m', '1h', '1d')."
    )
    args = parser.parse_args()

    # --- Display Settings ---
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    logger.info("Starting analysis run...")

    # --- Run Analysis ---
    run_ticker_analysis(
        ticker=args.ticker,
        period=args.period,
        interval=args.interval
    )

    logger.success("Analysis run finished.")


if __name__ == "__main__":
    main()