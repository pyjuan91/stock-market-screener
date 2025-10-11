from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from loguru import logger
import uvicorn

from stock_screener.screener import run_ticker_analysis, get_historical_analysis
from stock_screener.data_fetcher import fetch_stock_data
from data_sources.news_fetcher import NewsFetcher
from ml_models.sentiment_analyzer import get_sentiment_analyzer
from backtesting.strategy_engine import BacktestEngine, STRATEGIES
from backtesting.advanced_strategies import ADVANCED_STRATEGIES

app = FastAPI(
    title="Stock Screener API",
    description="An API to fetch stock data, calculate technical indicators, and screen stocks.",
    version="1.0.0",
)

# --- CORS Middleware Setup ---
# This allows the frontend to communicate with the backend in both development and production.
import os

# Allow multiple origins for development and production
origins = [
    "http://localhost:3000",  # Local development
    "https://localhost:3000",  # Local development with HTTPS
]

# Add production frontend URL from environment variable
FRONTEND_URL = os.getenv("FRONTEND_URL")
if FRONTEND_URL:
    origins.append(FRONTEND_URL)

# For Render deployment, also allow the common patterns
RENDER_FRONTEND_URL = os.getenv("RENDER_EXTERNAL_URL")
if RENDER_FRONTEND_URL:
    origins.append(RENDER_FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)


@app.get("/", tags=["General"])
def read_root():
    """Returns a welcome message."""
    return {"message": "Welcome to the Stock Screener API! Visit /docs for documentation."}

@app.post("/api/scan", tags=["Screening"])
def scan_tickers(
    tickers: List[str] = Body(..., description="A list of stock tickers to analyze.", embed=True),
    period: str = "1mo",
    interval: str = "1h",
):
    """
    Analyzes a list of stock tickers and returns the latest data with technical indicators.
    """
    logger.info(f"Received scan request for tickers: {tickers}")
    results = []
    for ticker in tickers:
        analysis_result = run_ticker_analysis(ticker, period, interval)
        if analysis_result:
            results.append(analysis_result)
    
    logger.info(f"Successfully analyzed {len(results)} out of {len(tickers)} tickers.")
    return results

@app.get("/api/history/{ticker}", tags=["Screening"])
def get_ticker_history(
    ticker: str,
    interval: str = "1h",
):
    """
    Fetches historical analysis for a single stock ticker.
    """
    logger.info(f"Received history request for ticker: {ticker}")

    history = get_historical_analysis(ticker=ticker, interval=interval)

    if history is None or len(history) == 0:
        raise HTTPException(status_code=404, detail=f"Could not fetch historical data for {ticker}.")

    return history

@app.get("/api/sentiment/{ticker}", tags=["Sentiment Analysis"])
def get_sentiment(
    ticker: str,
    days: int = 7,
    max_articles: int = 20
):
    """
    Fetch news and analyze sentiment for a stock ticker using FinBERT.

    Args:
        ticker: Stock ticker symbol
        days: Number of days to look back for news (default: 7)
        max_articles: Maximum number of articles to analyze (default: 20)

    Returns:
        Sentiment analysis with overall score, article breakdown, and news sources
    """
    logger.info(f"Received sentiment request for ticker: {ticker}")

    try:
        # Fetch news articles
        news_fetcher = NewsFetcher()
        articles = news_fetcher.fetch_all_sources(ticker, days=days)

        if not articles:
            logger.warning(f"No news articles found for {ticker}")
            return {
                "ticker": ticker,
                "overall_sentiment": "neutral",
                "overall_score": 0.0,
                "confidence": 0.0,
                "article_count": 0,
                "articles": []
            }

        # Limit articles to max_articles
        articles = articles[:max_articles]

        # Analyze sentiment
        analyzer = get_sentiment_analyzer()
        sentiment_result = analyzer.analyze_articles(articles)

        # Add ticker to result
        sentiment_result["ticker"] = ticker

        logger.info(f"Sentiment analysis for {ticker}: {sentiment_result['overall_sentiment']} ({sentiment_result['overall_score']:.3f})")

        return sentiment_result

    except Exception as e:
        logger.error(f"Error analyzing sentiment for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.post("/api/sentiment/batch", tags=["Sentiment Analysis"])
def get_batch_sentiment(
    tickers: List[str] = Body(..., description="List of stock tickers to analyze", embed=True),
    days: int = 7
):
    """
    Analyze sentiment for multiple tickers at once.

    Args:
        tickers: List of stock ticker symbols
        days: Number of days to look back for news

    Returns:
        List of sentiment analyses for each ticker
    """
    logger.info(f"Received batch sentiment request for tickers: {tickers}")

    results = []
    news_fetcher = NewsFetcher()
    analyzer = get_sentiment_analyzer()

    for ticker in tickers:
        try:
            articles = news_fetcher.fetch_all_sources(ticker, days=days)

            if articles:
                articles = articles[:20]  # Limit to 20 articles per ticker
                sentiment_result = analyzer.analyze_articles(articles)
                sentiment_result["ticker"] = ticker
                results.append(sentiment_result)
            else:
                results.append({
                    "ticker": ticker,
                    "overall_sentiment": "neutral",
                    "overall_score": 0.0,
                    "confidence": 0.0,
                    "article_count": 0,
                    "articles": []
                })
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {ticker}: {e}")
            results.append({
                "ticker": ticker,
                "error": str(e),
                "overall_sentiment": "neutral",
                "overall_score": 0.0
            })

    logger.info(f"Completed batch sentiment analysis for {len(results)} tickers")
    return results

@app.post("/api/backtest", tags=["Backtesting"])
def run_backtest(
    ticker: str = Body(..., description="Stock ticker symbol"),
    strategy: str = Body("rsi", description="Strategy name (rsi, macd, ma_crossover)"),
    period: str = Body("1y", description="Historical period (1mo, 3mo, 6mo, 1y, 2y, 5y)"),
    interval: str = Body("1d", description="Data interval (1d, 1h)"),
    initial_capital: float = Body(10000, description="Initial capital"),
    strategy_params: Optional[dict] = Body(None, description="Additional strategy parameters")
):
    """
    Run backtest for a trading strategy on historical data

    Args:
        ticker: Stock ticker symbol
        strategy: Strategy name
        period: Historical data period
        interval: Data interval
        initial_capital: Starting capital
        strategy_params: Additional parameters for strategy

    Returns:
        Backtest results with performance metrics and equity curve
    """
    logger.info(f"Received backtest request for {ticker} with strategy {strategy}")

    try:
        # Validate strategy
        all_strategies = {**STRATEGIES, **ADVANCED_STRATEGIES}
        if strategy not in all_strategies:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid strategy. Available: {', '.join(all_strategies.keys())}"
            )

        # Fetch historical data with indicators
        df = fetch_stock_data(ticker, period=period, interval=interval)

        if df is None or len(df) < 20:
            raise HTTPException(
                status_code=404,
                detail=f"Insufficient historical data for {ticker}"
            )

        # Run backtest
        engine = BacktestEngine(initial_capital=initial_capital)
        strategy_func = all_strategies[strategy]

        params = strategy_params or {}
        results = engine.run_backtest(df, strategy_func, **params)

        # Add metadata
        results["ticker"] = ticker
        results["strategy"] = strategy
        results["period"] = period
        results["interval"] = interval

        logger.info(f"Backtest completed for {ticker}: Return {results['metrics']['total_return_pct']:.2f}%")

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running backtest for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error running backtest: {str(e)}")

@app.post("/api/backtest/compare", tags=["Backtesting"])
def compare_strategies(
    ticker: str = Body(..., description="Stock ticker symbol"),
    strategies: List[str] = Body(..., description="List of strategies to compare"),
    period: str = Body("1y", description="Historical period"),
    interval: str = Body("1d", description="Data interval"),
    initial_capital: float = Body(10000, description="Initial capital")
):
    """
    Compare multiple strategies on the same ticker

    Args:
        ticker: Stock ticker symbol
        strategies: List of strategy names to compare
        period: Historical data period
        interval: Data interval
        initial_capital: Starting capital

    Returns:
        Comparison of all strategies with performance metrics
    """
    logger.info(f"Comparing strategies for {ticker}: {strategies}")

    try:
        # Fetch data once
        df = fetch_stock_data(ticker, period=period, interval=interval)

        if df is None or len(df) < 20:
            raise HTTPException(
                status_code=404,
                detail=f"Insufficient historical data for {ticker}"
            )

        all_strategies = {**STRATEGIES, **ADVANCED_STRATEGIES}
        results = []

        for strategy_name in strategies:
            if strategy_name not in all_strategies:
                logger.warning(f"Unknown strategy: {strategy_name}, skipping")
                continue

            try:
                engine = BacktestEngine(initial_capital=initial_capital)
                strategy_func = all_strategies[strategy_name]

                backtest_result = engine.run_backtest(df, strategy_func)

                results.append({
                    "strategy": strategy_name,
                    "metrics": backtest_result["metrics"],
                    "trade_count": len(backtest_result["trades"])
                })

            except Exception as e:
                logger.error(f"Error backtesting {strategy_name}: {e}")
                results.append({
                    "strategy": strategy_name,
                    "error": str(e)
                })

        # Sort by Sharpe ratio
        results.sort(key=lambda x: x.get("metrics", {}).get("sharpe_ratio", -999), reverse=True)

        logger.info(f"Strategy comparison completed for {ticker}")

        return {
            "ticker": ticker,
            "period": period,
            "strategies": results,
            "best_strategy": results[0]["strategy"] if results else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing strategies for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=f"Error comparing strategies: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting API server...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)