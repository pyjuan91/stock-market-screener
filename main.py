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
    # A mutually exclusive group to ensure either a ticker or a file is provided, but not both.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-t", "--ticker",
        type=str,
        help="A single stock ticker symbol to analyze (e.g., 'AAPL')."
    )
    group.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a file containing a list of ticker symbols (one per line)."
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
    if args.ticker:
        tickers_to_analyze = [args.ticker]
    else: # args.file is guaranteed to be not None by the mutually exclusive group
        try:
            with open(args.file, 'r') as f:
                tickers_to_analyze = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(tickers_to_analyze)} tickers from {args.file}")
        except FileNotFoundError:
            logger.error(f"Error: The file '{args.file}' was not found.")
            return

    for ticker in tickers_to_analyze:
        run_ticker_analysis(
            ticker=ticker,
            period=args.period,
            interval=args.interval
        )

    logger.success("Analysis run finished.")


if __name__ == "__main__":
    main()