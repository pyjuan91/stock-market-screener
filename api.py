from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from loguru import logger
import uvicorn

from stock_screener.screener import run_ticker_analysis, get_historical_analysis

app = FastAPI(
    title="Stock Screener API",
    description="An API to fetch stock data, calculate technical indicators, and screen stocks.",
    version="1.0.0",
)

# --- CORS Middleware Setup ---
# This allows the frontend (running on localhost:3000) to communicate with the backend.
origins = [
    "http://localhost:3000",
]

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

if __name__ == "__main__":
    logger.info("Starting API server...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)