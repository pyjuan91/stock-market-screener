"""
Strategy Engine Module
Backtesting framework for trading strategies
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable
from datetime import datetime
from loguru import logger

from backtesting.performance_metrics import PerformanceMetrics


class Trade:
    """Represents a single trade"""

    def __init__(self, entry_date, entry_price, shares, trade_type="long"):
        self.entry_date = entry_date
        self.entry_price = entry_price
        self.shares = shares
        self.trade_type = trade_type  # "long" or "short"
        self.exit_date = None
        self.exit_price = None
        self.profit = 0.0
        self.profit_pct = 0.0

    def close(self, exit_date, exit_price):
        """Close the trade"""
        self.exit_date = exit_date
        self.exit_price = exit_price

        if self.trade_type == "long":
            self.profit = (exit_price - self.entry_price) * self.shares
            self.profit_pct = ((exit_price - self.entry_price) / self.entry_price) * 100
        else:  # short
            self.profit = (self.entry_price - exit_price) * self.shares
            self.profit_pct = ((self.entry_price - exit_price) / self.entry_price) * 100

    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            "entry_date": str(self.entry_date),
            "entry_price": float(self.entry_price),
            "exit_date": str(self.exit_date) if self.exit_date else None,
            "exit_price": float(self.exit_price) if self.exit_price else None,
            "shares": float(self.shares),
            "trade_type": self.trade_type,
            "profit": float(self.profit),
            "profit_pct": float(self.profit_pct)
        }


class BacktestEngine:
    """
    Backtesting engine for trading strategies
    """

    def __init__(
        self,
        initial_capital: float = 10000,
        commission: float = 0.001,  # 0.1% commission
        slippage: float = 0.0005     # 0.05% slippage
    ):
        """
        Initialize backtest engine

        Args:
            initial_capital: Starting capital
            commission: Commission rate (default: 0.1%)
            slippage: Slippage rate (default: 0.05%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.reset()

    def reset(self):
        """Reset backtesting state"""
        self.cash = self.initial_capital
        self.position = None
        self.trades = []
        self.equity_curve = []
        self.dates = []

    def run_backtest(
        self,
        data: pd.DataFrame,
        strategy_func: Callable,
        **strategy_params
    ) -> Dict:
        """
        Run backtest on historical data

        Args:
            data: DataFrame with OHLCV data and indicators
            strategy_func: Function that returns trading signals
            **strategy_params: Additional parameters for strategy

        Returns:
            Backtest results with performance metrics
        """
        self.reset()

        logger.info(f"Running backtest with {len(data)} periods")

        # Ensure data is sorted by date
        data = data.sort_index()

        for i in range(len(data)):
            current_date = data.index[i]
            current_row = data.iloc[i]

            # Get trading signal from strategy
            signal = strategy_func(data, i, **strategy_params)

            # Execute trade based on signal
            if signal == "buy" and self.position is None:
                self._enter_long(current_date, current_row["Close"])

            elif signal == "sell" and self.position is not None:
                self._exit_position(current_date, current_row["Close"])

            # Calculate current portfolio value
            portfolio_value = self._calculate_portfolio_value(current_row["Close"])

            self.equity_curve.append(portfolio_value)
            self.dates.append(current_date)

        # Close any open position at the end
        if self.position is not None:
            last_date = data.index[-1]
            last_price = data.iloc[-1]["Close"]
            self._exit_position(last_date, last_price)

        # Calculate performance metrics
        equity_series = pd.Series(self.equity_curve, index=self.dates)
        metrics = PerformanceMetrics.calculate_all_metrics(
            equity_series,
            [trade.to_dict() for trade in self.trades],
            self.initial_capital
        )

        # Add equity curve to results
        equity_curve_data = [
            {"date": str(date), "value": float(value)}
            for date, value in zip(self.dates, self.equity_curve)
        ]

        logger.info(f"Backtest completed: {len(self.trades)} trades, " +
                   f"Return: {metrics['total_return_pct']:.2f}%, " +
                   f"Sharpe: {metrics['sharpe_ratio']:.2f}")

        return {
            "metrics": metrics,
            "equity_curve": equity_curve_data,
            "trades": [trade.to_dict() for trade in self.trades],
            "parameters": {
                "initial_capital": self.initial_capital,
                "commission": self.commission,
                "slippage": self.slippage,
                **strategy_params
            }
        }

    def _enter_long(self, date, price):
        """Enter long position"""
        # Apply slippage
        execution_price = price * (1 + self.slippage)

        # Calculate shares (leave some cash for commission)
        max_investment = self.cash * 0.98  # 98% to leave room for commission
        shares = max_investment / execution_price

        # Calculate commission
        cost = shares * execution_price
        commission_cost = cost * self.commission

        total_cost = cost + commission_cost

        if total_cost > self.cash:
            logger.warning(f"Insufficient cash for trade on {date}")
            return

        self.position = Trade(date, execution_price, shares, "long")
        self.cash -= total_cost

        logger.debug(f"Entered long: {shares:.2f} shares @ ${execution_price:.2f} on {date}")

    def _exit_position(self, date, price):
        """Exit current position"""
        if self.position is None:
            return

        # Apply slippage
        execution_price = price * (1 - self.slippage)

        # Close trade
        self.position.close(date, execution_price)

        # Calculate proceeds
        proceeds = self.position.shares * execution_price
        commission_cost = proceeds * self.commission

        self.cash += (proceeds - commission_cost)

        # Add to completed trades
        self.trades.append(self.position)

        logger.debug(f"Exited position: Profit ${self.position.profit:.2f} ({self.position.profit_pct:.2f}%) on {date}")

        self.position = None

    def _calculate_portfolio_value(self, current_price):
        """Calculate current portfolio value"""
        if self.position is None:
            return self.cash
        else:
            position_value = self.position.shares * current_price
            return self.cash + position_value


# Strategy functions

def rsi_strategy(data: pd.DataFrame, index: int, rsi_oversold: int = 30, rsi_overbought: int = 70) -> str:
    """
    Simple RSI strategy

    Args:
        data: DataFrame with RSI indicator
        index: Current index
        rsi_oversold: RSI oversold threshold (buy signal)
        rsi_overbought: RSI overbought threshold (sell signal)

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1 or "RSI" not in data.columns:
        return "hold"

    current_rsi = data.iloc[index]["RSI"]
    prev_rsi = data.iloc[index - 1]["RSI"]

    # Buy when RSI crosses above oversold
    if prev_rsi <= rsi_oversold and current_rsi > rsi_oversold:
        return "buy"

    # Sell when RSI crosses above overbought
    if current_rsi >= rsi_overbought:
        return "sell"

    return "hold"


def macd_strategy(data: pd.DataFrame, index: int) -> str:
    """
    MACD crossover strategy

    Args:
        data: DataFrame with MACD and MACD_Signal
        index: Current index

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1 or "MACD" not in data.columns or "MACD_Signal" not in data.columns:
        return "hold"

    current_macd = data.iloc[index]["MACD"]
    current_signal = data.iloc[index]["MACD_Signal"]
    prev_macd = data.iloc[index - 1]["MACD"]
    prev_signal = data.iloc[index - 1]["MACD_Signal"]

    # Buy when MACD crosses above signal line
    if prev_macd <= prev_signal and current_macd > current_signal:
        return "buy"

    # Sell when MACD crosses below signal line
    if prev_macd >= prev_signal and current_macd < current_signal:
        return "sell"

    return "hold"


def ma_crossover_strategy(data: pd.DataFrame, index: int) -> str:
    """
    Moving average crossover strategy

    Args:
        data: DataFrame with MA20 and MA50
        index: Current index

    Returns:
        Trading signal: "buy", "sell", or "hold"
    """
    if index < 1 or "MA20" not in data.columns or "MA50" not in data.columns:
        return "hold"

    current_ma20 = data.iloc[index]["MA20"]
    current_ma50 = data.iloc[index]["MA50"]
    prev_ma20 = data.iloc[index - 1]["MA20"]
    prev_ma50 = data.iloc[index - 1]["MA50"]

    # Buy when MA20 crosses above MA50 (golden cross)
    if prev_ma20 <= prev_ma50 and current_ma20 > current_ma50:
        return "buy"

    # Sell when MA20 crosses below MA50 (death cross)
    if prev_ma20 >= prev_ma50 and current_ma20 < current_ma50:
        return "sell"

    return "hold"


# Strategy registry
STRATEGIES = {
    "rsi": rsi_strategy,
    "macd": macd_strategy,
    "ma_crossover": ma_crossover_strategy
}
