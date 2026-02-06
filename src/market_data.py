from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import yfinance as yf


def fetch_price_history(
    ticker: str,
    start: date,
    end: date,
) -> pd.DataFrame:
    """
    Fetch historical price data using yfinance.
    
    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    start : date
        Start date.
    end : date
        End date.
        
    Returns
    -------
    pd.DataFrame
        Historical OHLCV data.
    """
    df = yf.download(
        ticker,
        start=start.isoformat(),
        end=end.isoformat(),
        interval="1d",
        auto_adjust=False,
        progress=False,
    )
    
    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}.")
    
    return df.sort_index()


def estimate_volatility(prices: pd.Series, annualization_factor: int = 252) -> float:
    """
    Estimate annualized volatility from historical prices.
    
    Parameters
    ----------
    prices : pd.Series
        Historical price series.
    annualization_factor : int
        Factor to annualize volatility (252 for daily data).
        
    Returns
    -------
    float
        Annualized volatility (standard deviation of log returns).
    """
    log_returns = np.log(prices / prices.shift(1)).dropna()
    daily_volatility = log_returns.std()
    annualized_volatility = daily_volatility * np.sqrt(annualization_factor)
    return float(annualized_volatility)


def get_current_price_and_volatility(ticker: str, start: date, end: date) -> tuple[float, float]:
    """
    Fetch current price and estimate volatility for a ticker.
    
    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    start : date
        Start date for historical data.
    end : date
        End date for historical data.
        
    Returns
    -------
    current_price : float
        Most recent closing price.
    volatility : float
        Estimated annualized volatility.
    """
    df = fetch_price_history(ticker, start, end)
    current_price = float(df["Close"].iloc[-1])
    volatility = estimate_volatility(df["Close"])
    return current_price, volatility
