from __future__ import annotations

import numpy as np


def call_payoff(spot_prices: np.ndarray, strike: float) -> np.ndarray:
    """
    Calculate call option payoff at expiration.
    
    Payoff = max(S_T - K, 0)
    
    Parameters
    ----------
    spot_prices : np.ndarray
        Terminal stock prices (at expiration).
    strike : float
        Strike price.
        
    Returns
    -------
    np.ndarray
        Call option payoffs.
    """
    return np.maximum(spot_prices - strike, 0)


def put_payoff(spot_prices: np.ndarray, strike: float) -> np.ndarray:
    """
    Calculate put option payoff at expiration.
    
    Payoff = max(K - S_T, 0)
    
    Parameters
    ----------
    spot_prices : np.ndarray
        Terminal stock prices (at expiration).
    strike : float
        Strike price.
        
    Returns
    -------
    np.ndarray
        Put option payoffs.
    """
    return np.maximum(strike - spot_prices, 0)


def calculate_option_payoff(
    terminal_prices: np.ndarray,
    strike: float,
    option_type: str,
) -> np.ndarray:
    """
    Calculate option payoffs for a given option type.
    
    Parameters
    ----------
    terminal_prices : np.ndarray
        Array of terminal stock prices.
    strike : float
        Strike price.
    option_type : str
        "call" or "put".
        
    Returns
    -------
    np.ndarray
        Array of option payoffs.
    """
    if option_type.lower() == "call":
        return call_payoff(terminal_prices, strike)
    elif option_type.lower() == "put":
        return put_payoff(terminal_prices, strike)
    else:
        raise ValueError(f"Unknown option type: {option_type}. Use 'call' or 'put'.")
