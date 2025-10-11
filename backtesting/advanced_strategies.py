"""
Advanced Trading Strategies
Combines technical indicators with sentiment analysis
"""
import pandas as pd
from typing import Optional
from loguru import logger


def rsi_sentiment_strategy(
    data: pd.DataFrame,
    index: int,
    sentiment_score: float = 0.0,
    rsi_oversold: int = 30,
    rsi_overbought: int = 70,
    sentiment_threshold: float = 0.2
) -> str:
    """
    RSI strategy enhanced with sentiment analysis

    Buy when:
    - RSI crosses above oversold AND sentiment is positive
    - Or RSI is oversold and sentiment is very positive

    Sell when:
    - RSI is overbought OR sentiment turns very negative

    Args:
        data: DataFrame with RSI indicator
        index: Current index
        sentiment_score: Current sentiment score (-1 to 1)
        rsi_oversold: RSI oversold threshold
        rsi_overbought: RSI overbought threshold
        sentiment_threshold: Sentiment threshold for signals

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1 or "RSI" not in data.columns:
        return "hold"

    current_rsi = data.iloc[index]["RSI"]
    prev_rsi = data.iloc[index - 1]["RSI"]

    # Enhanced buy signal: RSI recovery + positive sentiment
    if prev_rsi <= rsi_oversold and current_rsi > rsi_oversold:
        if sentiment_score > sentiment_threshold:
            return "buy"

    # Aggressive buy: very positive sentiment during oversold
    if current_rsi < rsi_oversold and sentiment_score > 0.5:
        return "buy"

    # Sell signal: overbought OR very negative sentiment
    if current_rsi >= rsi_overbought or sentiment_score < -0.5:
        return "sell"

    # Early exit: sentiment turns negative while holding
    if sentiment_score < -sentiment_threshold and current_rsi > 50:
        return "sell"

    return "hold"


def macd_sentiment_strategy(
    data: pd.DataFrame,
    index: int,
    sentiment_score: float = 0.0,
    sentiment_threshold: float = 0.15
) -> str:
    """
    MACD strategy enhanced with sentiment filter

    Only take MACD signals when sentiment confirms the direction

    Args:
        data: DataFrame with MACD and MACD_Signal
        index: Current index
        sentiment_score: Current sentiment score (-1 to 1)
        sentiment_threshold: Minimum sentiment for trade confirmation

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1 or "MACD" not in data.columns or "MACD_Signal" not in data.columns:
        return "hold"

    current_macd = data.iloc[index]["MACD"]
    current_signal = data.iloc[index]["MACD_Signal"]
    prev_macd = data.iloc[index - 1]["MACD"]
    prev_signal = data.iloc[index - 1]["MACD_Signal"]

    # MACD bullish crossover + positive sentiment confirmation
    if prev_macd <= prev_signal and current_macd > current_signal:
        if sentiment_score > sentiment_threshold:
            return "buy"

    # MACD bearish crossover OR very negative sentiment
    if prev_macd >= prev_signal and current_macd < current_signal:
        return "sell"

    # Exit on negative sentiment even without MACD signal
    if sentiment_score < -0.4:
        return "sell"

    return "hold"


def multi_indicator_sentiment_strategy(
    data: pd.DataFrame,
    index: int,
    sentiment_score: float = 0.0,
    rsi_oversold: int = 35,
    rsi_overbought: int = 65
) -> str:
    """
    Advanced strategy combining RSI, MACD, MA, and sentiment

    Uses multiple confirmations for higher conviction trades

    Args:
        data: DataFrame with indicators
        index: Current index
        sentiment_score: Current sentiment score
        rsi_oversold: RSI oversold level
        rsi_overbought: RSI overbought level

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1:
        return "hold"

    # Required columns
    required_cols = ["RSI", "MACD", "MACD_Signal", "MA20", "MA50", "Close"]
    if not all(col in data.columns for col in required_cols):
        return "hold"

    current = data.iloc[index]
    prev = data.iloc[index - 1]

    # Calculate signals
    signals_bullish = 0
    signals_bearish = 0

    # 1. RSI signal
    if current["RSI"] < rsi_oversold:
        signals_bullish += 1
    elif current["RSI"] > rsi_overbought:
        signals_bearish += 1

    # 2. MACD signal
    if current["MACD"] > current["MACD_Signal"]:
        signals_bullish += 1
    elif current["MACD"] < current["MACD_Signal"]:
        signals_bearish += 1

    # 3. MA trend
    if current["Close"] > current["MA20"] > current["MA50"]:
        signals_bullish += 1
    elif current["Close"] < current["MA20"] < current["MA50"]:
        signals_bearish += 1

    # 4. Sentiment signal (strongest weight)
    if sentiment_score > 0.3:
        signals_bullish += 2
    elif sentiment_score > 0.1:
        signals_bullish += 1
    elif sentiment_score < -0.3:
        signals_bearish += 2
    elif sentiment_score < -0.1:
        signals_bearish += 1

    # Decision: need at least 3 confirming signals
    if signals_bullish >= 3 and signals_bearish == 0:
        return "buy"
    elif signals_bearish >= 2:  # More aggressive on sells
        return "sell"

    return "hold"


def momentum_sentiment_strategy(
    data: pd.DataFrame,
    index: int,
    sentiment_score: float = 0.0,
    lookback: int = 5
) -> str:
    """
    Momentum strategy with sentiment confirmation

    Looks for price momentum aligned with sentiment

    Args:
        data: DataFrame with price data
        index: Current index
        sentiment_score: Current sentiment score
        lookback: Lookback period for momentum

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < lookback or "Close" not in data.columns:
        return "hold"

    current_price = data.iloc[index]["Close"]
    past_price = data.iloc[index - lookback]["Close"]

    # Calculate momentum
    momentum = (current_price - past_price) / past_price

    # Strong upward momentum + positive sentiment
    if momentum > 0.02 and sentiment_score > 0.25:
        return "buy"

    # Strong downward momentum OR very negative sentiment
    if momentum < -0.02 or sentiment_score < -0.4:
        return "sell"

    # Sentiment-driven signals
    if sentiment_score > 0.5 and momentum > -0.01:
        return "buy"

    if sentiment_score < -0.3:
        return "sell"

    return "hold"


# Strategy registry for advanced strategies
ADVANCED_STRATEGIES = {
    "rsi_sentiment": rsi_sentiment_strategy,
    "macd_sentiment": macd_sentiment_strategy,
    "multi_indicator_sentiment": multi_indicator_sentiment_strategy,
    "momentum_sentiment": momentum_sentiment_strategy
}
