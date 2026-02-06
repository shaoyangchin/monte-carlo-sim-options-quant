from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .black_scholes import black_scholes_price
from .config import DefaultConfig
from .monte_carlo import calculate_monte_carlo_stats, monte_carlo_option_price


@dataclass
class OptionPricingResults:
    """Container for option pricing results."""
    
    # Input parameters
    spot_price: float
    strike_price: float
    time_to_expiration: float
    risk_free_rate: float
    volatility: float
    option_type: str
    num_simulations: int
    
    # Monte Carlo results
    mc_price: float
    mc_price_paths: np.ndarray
    mc_payoffs: np.ndarray
    mc_std_error: float
    mc_ci_lower: float
    mc_ci_upper: float
    
    # Black-Scholes results
    bs_price: float
    
    # Comparison
    price_difference: float
    percentage_difference: float


def price_option_monte_carlo(
    spot_price: float | None = None,
    strike_price: float | None = None,
    time_to_expiration: float | None = None,
    risk_free_rate: float | None = None,
    volatility: float | None = None,
    option_type: str | None = None,
    num_simulations: int | None = None,
    num_steps: int | None = None,
) -> OptionPricingResults:
    """
    Price an option using Monte Carlo simulation and compare with Black-Scholes.
    
    Parameters
    ----------
    spot_price : float, optional
        Current stock price (S0).
    strike_price : float, optional
        Strike price (K).
    time_to_expiration : float, optional
        Time to expiration in years (T).
    risk_free_rate : float, optional
        Risk-free interest rate (r).
    volatility : float, optional
        Annualized volatility (sigma).
    option_type : str, optional
        "call" or "put".
    num_simulations : int, optional
        Number of Monte Carlo simulations.
    num_steps : int, optional
        Number of time steps per simulation.
        
    Returns
    -------
    OptionPricingResults
        Complete pricing results including Monte Carlo and Black-Scholes prices.
    """
    cfg = DefaultConfig()
    
    # Use defaults if not provided
    S0 = spot_price if spot_price is not None else cfg.spot_price
    K = strike_price if strike_price is not None else cfg.strike_price
    T = time_to_expiration if time_to_expiration is not None else cfg.time_to_expiration
    r = risk_free_rate if risk_free_rate is not None else cfg.risk_free_rate
    sigma = volatility if volatility is not None else cfg.volatility
    opt_type = option_type if option_type is not None else cfg.option_type
    n_sims = num_simulations if num_simulations is not None else cfg.num_simulations
    n_steps = num_steps if num_steps is not None else cfg.num_steps
    
    # Monte Carlo pricing
    mc_price, price_paths, payoffs = monte_carlo_option_price(
        S0=S0,
        K=K,
        T=T,
        r=r,
        sigma=sigma,
        option_type=opt_type,
        num_simulations=n_sims,
        num_steps=n_steps,
        random_seed=42,
    )
    
    # Calculate Monte Carlo statistics
    mc_stats = calculate_monte_carlo_stats(payoffs, r, T)
    
    # Black-Scholes pricing
    bs_price = black_scholes_price(S0, K, T, r, sigma, opt_type)
    
    # Comparison
    price_diff = abs(mc_price - bs_price)
    pct_diff = (price_diff / bs_price * 100) if bs_price != 0 else 0
    
    return OptionPricingResults(
        spot_price=S0,
        strike_price=K,
        time_to_expiration=T,
        risk_free_rate=r,
        volatility=sigma,
        option_type=opt_type,
        num_simulations=n_sims,
        mc_price=mc_price,
        mc_price_paths=price_paths,
        mc_payoffs=payoffs,
        mc_std_error=mc_stats["std_error"],
        mc_ci_lower=mc_stats["ci_lower"],
        mc_ci_upper=mc_stats["ci_upper"],
        bs_price=bs_price,
        price_difference=price_diff,
        percentage_difference=pct_diff,
    )


def summarize_results(results: OptionPricingResults) -> str:
    """
    Create a human-readable summary of pricing results.
    
    Parameters
    ----------
    results : OptionPricingResults
        Pricing results object.
        
    Returns
    -------
    str
        Formatted summary string.
    """
    lines = [
        "=" * 60,
        "Monte Carlo Options Pricing Results",
        "=" * 60,
        "",
        "Option Parameters:",
        f"  Type:                  {results.option_type.upper()}",
        f"  Spot Price (S0):       ${results.spot_price:.2f}",
        f"  Strike Price (K):      ${results.strike_price:.2f}",
        f"  Time to Expiration:    {results.time_to_expiration:.2f} years",
        f"  Risk-Free Rate:        {results.risk_free_rate * 100:.2f}%",
        f"  Volatility (σ):        {results.volatility * 100:.2f}%",
        "",
        "Simulation Parameters:",
        f"  Number of Simulations: {results.num_simulations:,}",
        "",
        "Monte Carlo Results:",
        f"  Estimated Price:       ${results.mc_price:.4f}",
        f"  Standard Error:        ${results.mc_std_error:.4f}",
        f"  95% Confidence Interval: [${results.mc_ci_lower:.4f}, ${results.mc_ci_upper:.4f}]",
        "",
        "Black-Scholes Results:",
        f"  Theoretical Price:     ${results.bs_price:.4f}",
        "",
        "Comparison:",
        f"  Absolute Difference:   ${results.price_difference:.4f}",
        f"  Percentage Difference: {results.percentage_difference:.2f}%",
        "",
        "Interpretation:",
        f"  The Monte Carlo simulation estimates the {results.option_type} option price",
        f"  at ${results.mc_price:.4f}, which differs from the Black-Scholes theoretical",
        f"  price by {results.percentage_difference:.2f}%. This difference is due to",
        f"  Monte Carlo sampling error and typically decreases with more simulations.",
        "",
        "=" * 60,
    ]
    return "\n".join(lines)
