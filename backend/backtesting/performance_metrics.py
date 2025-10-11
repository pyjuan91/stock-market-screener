"""
Performance Metrics Module
Calculates trading strategy performance metrics
"""
import numpy as np
import pandas as pd
from typing import List, Dict
from loguru import logger


class PerformanceMetrics:
    """Calculate various performance metrics for trading strategies"""

    @staticmethod
    def calculate_returns(equity_curve: pd.Series) -> pd.Series:
        """
        Calculate period returns from equity curve

        Args:
            equity_curve: Series of portfolio values over time

        Returns:
            Series of period returns
        """
        return equity_curve.pct_change().fillna(0)

    @staticmethod
    def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02, periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe Ratio

        Args:
            returns: Series of period returns
            risk_free_rate: Annual risk-free rate (default: 2%)
            periods_per_year: Number of trading periods per year (default: 252 for daily)

        Returns:
            Sharpe ratio
        """
        if len(returns) == 0 or returns.std() == 0:
            return 0.0

        # Convert annual risk-free rate to period rate
        period_rf_rate = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

        # Calculate excess returns
        excess_returns = returns - period_rf_rate

        # Annualize
        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)

        return float(sharpe)

    @staticmethod
    def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02, periods_per_year: int = 252) -> float:
        """
        Calculate Sortino Ratio (like Sharpe but only considers downside volatility)

        Args:
            returns: Series of period returns
            risk_free_rate: Annual risk-free rate
            periods_per_year: Number of trading periods per year

        Returns:
            Sortino ratio
        """
        if len(returns) == 0:
            return 0.0

        period_rf_rate = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
        excess_returns = returns - period_rf_rate

        # Only consider negative returns for downside deviation
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0

        sortino = (excess_returns.mean() / downside_returns.std()) * np.sqrt(periods_per_year)

        return float(sortino)

    @staticmethod
    def max_drawdown(equity_curve: pd.Series) -> Dict:
        """
        Calculate maximum drawdown

        Args:
            equity_curve: Series of portfolio values

        Returns:
            Dict with max_drawdown, max_drawdown_pct, peak, trough
        """
        if len(equity_curve) == 0:
            return {
                "max_drawdown": 0.0,
                "max_drawdown_pct": 0.0,
                "peak": 0.0,
                "trough": 0.0,
                "peak_date": None,
                "trough_date": None
            }

        # Calculate running maximum
        running_max = equity_curve.expanding().max()

        # Calculate drawdown
        drawdown = equity_curve - running_max
        drawdown_pct = (drawdown / running_max) * 100

        # Find maximum drawdown
        max_dd_idx = drawdown.idxmin()
        max_dd = drawdown[max_dd_idx]
        max_dd_pct = drawdown_pct[max_dd_idx]

        # Find peak before drawdown
        peak_idx = equity_curve[:max_dd_idx].idxmax()
        peak = equity_curve[peak_idx]
        trough = equity_curve[max_dd_idx]

        return {
            "max_drawdown": float(max_dd),
            "max_drawdown_pct": float(max_dd_pct),
            "peak": float(peak),
            "trough": float(trough),
            "peak_date": str(peak_idx) if peak_idx is not None else None,
            "trough_date": str(max_dd_idx) if max_dd_idx is not None else None
        }

    @staticmethod
    def win_rate(trades: List[Dict]) -> float:
        """
        Calculate win rate

        Args:
            trades: List of trade dictionaries with 'profit' key

        Returns:
            Win rate as percentage
        """
        if not trades:
            return 0.0

        winning_trades = sum(1 for trade in trades if trade.get("profit", 0) > 0)
        return (winning_trades / len(trades)) * 100

    @staticmethod
    def profit_factor(trades: List[Dict]) -> float:
        """
        Calculate profit factor (gross profit / gross loss)

        Args:
            trades: List of trade dictionaries with 'profit' key

        Returns:
            Profit factor
        """
        if not trades:
            return 0.0

        gross_profit = sum(trade.get("profit", 0) for trade in trades if trade.get("profit", 0) > 0)
        gross_loss = abs(sum(trade.get("profit", 0) for trade in trades if trade.get("profit", 0) < 0))

        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0

        return gross_profit / gross_loss

    @staticmethod
    def calculate_all_metrics(
        equity_curve: pd.Series,
        trades: List[Dict],
        initial_capital: float = 10000,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> Dict:
        """
        Calculate all performance metrics

        Args:
            equity_curve: Series of portfolio values
            trades: List of completed trades
            initial_capital: Starting capital
            risk_free_rate: Annual risk-free rate
            periods_per_year: Trading periods per year

        Returns:
            Dict with all performance metrics
        """
        if len(equity_curve) == 0:
            return {
                "total_return": 0.0,
                "total_return_pct": 0.0,
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
                "max_drawdown": 0.0,
                "max_drawdown_pct": 0.0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0
            }

        # Calculate returns
        returns = PerformanceMetrics.calculate_returns(equity_curve)

        # Total return
        total_return = equity_curve.iloc[-1] - initial_capital
        total_return_pct = (total_return / initial_capital) * 100

        # Risk-adjusted returns
        sharpe = PerformanceMetrics.sharpe_ratio(returns, risk_free_rate, periods_per_year)
        sortino = PerformanceMetrics.sortino_ratio(returns, risk_free_rate, periods_per_year)

        # Drawdown
        dd_metrics = PerformanceMetrics.max_drawdown(equity_curve)

        # Trade statistics
        win_rate = PerformanceMetrics.win_rate(trades)
        profit_factor = PerformanceMetrics.profit_factor(trades)

        winning_trades = sum(1 for trade in trades if trade.get("profit", 0) > 0)
        losing_trades = sum(1 for trade in trades if trade.get("profit", 0) < 0)

        # Average trade metrics
        if trades:
            avg_profit = np.mean([trade.get("profit", 0) for trade in trades])
            avg_win = np.mean([trade.get("profit", 0) for trade in trades if trade.get("profit", 0) > 0]) if winning_trades > 0 else 0
            avg_loss = np.mean([trade.get("profit", 0) for trade in trades if trade.get("profit", 0) < 0]) if losing_trades > 0 else 0
        else:
            avg_profit = 0
            avg_win = 0
            avg_loss = 0

        return {
            "total_return": float(total_return),
            "total_return_pct": float(total_return_pct),
            "annualized_return": float(total_return_pct * (periods_per_year / len(equity_curve)) if len(equity_curve) > 0 else 0),
            "sharpe_ratio": float(sharpe),
            "sortino_ratio": float(sortino),
            "max_drawdown": float(dd_metrics["max_drawdown"]),
            "max_drawdown_pct": float(dd_metrics["max_drawdown_pct"]),
            "peak": float(dd_metrics["peak"]),
            "trough": float(dd_metrics["trough"]),
            "win_rate": float(win_rate),
            "profit_factor": float(profit_factor),
            "total_trades": len(trades),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "avg_profit": float(avg_profit),
            "avg_win": float(avg_win),
            "avg_loss": float(avg_loss),
            "final_equity": float(equity_curve.iloc[-1]) if len(equity_curve) > 0 else initial_capital
        }
