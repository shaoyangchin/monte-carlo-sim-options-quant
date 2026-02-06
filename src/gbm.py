from __future__ import annotations

import numpy as np


def simulate_gbm_paths(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    num_steps: int,
    num_simulations: int,
    random_seed: int | None = None,
) -> np.ndarray:
    """
    Simulate stock price paths using Geometric Brownian Motion (GBM).
    
    The GBM model assumes:
        dS = mu * S * dt + sigma * S * dW
    
    Where:
    - S is the stock price
    - mu is the drift (expected return)
    - sigma is the volatility
    - dW is a Wiener process (Brownian motion)
    
    Parameters
    ----------
    S0 : float
        Initial stock price.
    mu : float
        Drift rate (expected return, typically risk-free rate for risk-neutral pricing).
    sigma : float
        Volatility (annualized standard deviation).
    T : float
        Time to expiration in years.
    num_steps : int
        Number of time steps to simulate.
    num_simulations : int
        Number of price paths to generate.
    random_seed : int, optional
        Random seed for reproducibility.
        
    Returns
    -------
    np.ndarray
        Array of shape (num_simulations, num_steps + 1) containing simulated price paths.
        Each row is one simulated path, starting with S0.
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    dt = T / num_steps
    
    # Initialize price paths array
    paths = np.zeros((num_simulations, num_steps + 1))
    paths[:, 0] = S0
    
    # Generate random normal increments
    Z = np.random.standard_normal((num_simulations, num_steps))
    
    # Simulate paths using the exact solution of GBM:
    # S(t + dt) = S(t) * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
    for t in range(1, num_steps + 1):
        paths[:, t] = paths[:, t - 1] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t - 1]
        )
    
    return paths
