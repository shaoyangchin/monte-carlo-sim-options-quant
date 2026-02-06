from __future__ import annotations

import numpy as np

from .gbm import simulate_gbm_paths
from .options import calculate_option_payoff


def monte_carlo_option_price(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str,
    num_simulations: int = 10000,
    num_steps: int = 252,
    random_seed: int | None = None,
) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Price a European option using Monte Carlo simulation with Geometric Brownian Motion.
    
    Process:
    1. Simulate stock price paths using GBM
    2. Calculate option payoff for each terminal price
    3. Average all payoffs
    4. Discount back to present value
    
    Parameters
    ----------
    S0 : float
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
    num_simulations : int
        Number of Monte Carlo simulations.
    num_steps : int
        Number of time steps per simulation.
    random_seed : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    option_price : float
        Estimated option price.
    price_paths : np.ndarray
        Simulated stock price paths (shape: num_simulations x num_steps+1).
    payoffs : np.ndarray
        Option payoffs for each simulation (shape: num_simulations).
    """
    # Simulate stock price paths using GBM
    # Use risk-free rate as drift for risk-neutral pricing
    price_paths = simulate_gbm_paths(
        S0=S0,
        mu=r,  # Risk-neutral drift
        sigma=sigma,
        T=T,
        num_steps=num_steps,
        num_simulations=num_simulations,
        random_seed=random_seed,
    )
    
    # Extract terminal prices (last column)
    terminal_prices = price_paths[:, -1]
    
    # Calculate option payoffs
    payoffs = calculate_option_payoff(terminal_prices, K, option_type)
    
    # Average payoffs and discount to present value
    average_payoff = np.mean(payoffs)
    option_price = average_payoff * np.exp(-r * T)
    
    return float(option_price), price_paths, payoffs


def calculate_monte_carlo_stats(payoffs: np.ndarray, r: float, T: float) -> dict[str, float]:
    """
    Calculate statistics for Monte Carlo option pricing.
    
    Parameters
    ----------
    payoffs : np.ndarray
        Array of option payoffs from simulations.
    r : float
        Risk-free rate.
    T : float
        Time to expiration in years.
        
    Returns
    -------
    dict
        Statistics including mean, std, confidence interval, etc.
    """
    discount_factor = np.exp(-r * T)
    
    mean_payoff = np.mean(payoffs)
    std_payoff = np.std(payoffs)
    
    # Present value statistics
    pv_mean = mean_payoff * discount_factor
    pv_std = std_payoff * discount_factor
    
    # 95% confidence interval for the option price estimate
    standard_error = pv_std / np.sqrt(len(payoffs))
    ci_lower = pv_mean - 1.96 * standard_error
    ci_upper = pv_mean + 1.96 * standard_error
    
    return {
        "mean_payoff": float(mean_payoff),
        "std_payoff": float(std_payoff),
        "option_price": float(pv_mean),
        "std_error": float(standard_error),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "num_simulations": len(payoffs),
    }
