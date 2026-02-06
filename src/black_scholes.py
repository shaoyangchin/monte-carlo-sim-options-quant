from __future__ import annotations

import numpy as np
from scipy.stats import norm


def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculate European call option price using Black-Scholes formula.
    
    Parameters
    ----------
    S : float
        Current stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized standard deviation).
        
    Returns
    -------
    float
        Call option price.
    """
    if T <= 0:
        # Option has expired
        return max(S - K, 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return float(call_price)


def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    Calculate European put option price using Black-Scholes formula.
    
    Parameters
    ----------
    S : float
        Current stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized standard deviation).
        
    Returns
    -------
    float
        Put option price.
    """
    if T <= 0:
        # Option has expired
        return max(K - S, 0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return float(put_price)


def black_scholes_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str,
) -> float:
    """
    Calculate European option price using Black-Scholes formula.
    
    Parameters
    ----------
    S : float
        Current stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized standard deviation).
    option_type : str
        "call" or "put".
        
    Returns
    -------
    float
        Option price.
    """
    if option_type.lower() == "call":
        return black_scholes_call(S, K, T, r, sigma)
    elif option_type.lower() == "put":
        return black_scholes_put(S, K, T, r, sigma)
    else:
        raise ValueError(f"Unknown option type: {option_type}. Use 'call' or 'put'.")
