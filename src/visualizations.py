from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_price_paths(
    price_paths: np.ndarray,
    S0: float,
    K: float,
    T: float,
    num_paths_to_plot: int = 100,
    title: str = "Simulated Stock Price Paths (GBM)",
    figsize: tuple[int, int] = (12, 6),
) -> plt.Figure:
    """
    Plot a sample of simulated stock price paths.
    
    Parameters
    ----------
    price_paths : np.ndarray
        Array of simulated price paths (shape: num_simulations x num_steps+1).
    S0 : float
        Initial stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    num_paths_to_plot : int
        Number of paths to plot (randomly sampled).
    title : str
        Plot title.
    figsize : tuple
        Figure size.
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    num_simulations, num_steps = price_paths.shape
    time_grid = np.linspace(0, T, num_steps)
    
    # Randomly sample paths to plot
    indices = np.random.choice(num_simulations, min(num_paths_to_plot, num_simulations), replace=False)
    
    for idx in indices:
        ax.plot(time_grid, price_paths[idx, :], alpha=0.3, linewidth=0.8, color="steelblue")
    
    # Plot strike price
    ax.axhline(K, color="red", linestyle="--", linewidth=2, label=f"Strike Price K={K}")
    
    # Plot initial price
    ax.axhline(S0, color="green", linestyle="--", linewidth=2, label=f"Initial Price S0={S0}")
    
    ax.set_xlabel("Time (years)", fontsize=12)
    ax.set_ylabel("Stock Price", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_payoff_distribution(
    payoffs: np.ndarray,
    option_price: float,
    bs_price: float | None = None,
    option_type: str = "call",
    title: str = "Option Payoff Distribution",
    figsize: tuple[int, int] = (10, 6),
) -> plt.Figure:
    """
    Plot histogram of option payoffs from Monte Carlo simulation.
    
    Parameters
    ----------
    payoffs : np.ndarray
        Array of option payoffs.
    option_price : float
        Estimated option price (discounted average payoff).
    bs_price : float, optional
        Black-Scholes price for comparison.
    option_type : str
        "call" or "put".
    title : str
        Plot title.
    figsize : tuple
        Figure size.
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Histogram of payoffs
    ax.hist(payoffs, bins=50, alpha=0.7, color="coral", edgecolor="black", density=False)
    
    # Mean payoff line
    mean_payoff = np.mean(payoffs)
    ax.axvline(mean_payoff, color="darkblue", linestyle="--", linewidth=2, 
               label=f"Mean Payoff: ${mean_payoff:.2f}")
    
    ax.set_xlabel("Option Payoff at Expiration", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add text box with pricing info
    info_text = f"Monte Carlo Price: ${option_price:.4f}"
    if bs_price is not None:
        info_text += f"\nBlack-Scholes Price: ${bs_price:.4f}"
        diff = abs(option_price - bs_price)
        pct_diff = (diff / bs_price) * 100 if bs_price != 0 else 0
        info_text += f"\nDifference: ${diff:.4f} ({pct_diff:.2f}%)"
    
    ax.text(0.98, 0.97, info_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    return fig


def plot_terminal_price_distribution(
    price_paths: np.ndarray,
    K: float,
    option_type: str = "call",
    title: str = "Terminal Stock Price Distribution",
    figsize: tuple[int, int] = (10, 6),
) -> plt.Figure:
    """
    Plot distribution of terminal stock prices with strike price.
    
    Parameters
    ----------
    price_paths : np.ndarray
        Simulated price paths.
    K : float
        Strike price.
    option_type : str
        "call" or "put".
    title : str
        Plot title.
    figsize : tuple
        Figure size.
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    terminal_prices = price_paths[:, -1]
    
    # Histogram
    ax.hist(terminal_prices, bins=50, alpha=0.7, color="steelblue", edgecolor="black", density=True)
    
    # KDE overlay
    sns.kdeplot(terminal_prices, ax=ax, color="darkblue", linewidth=2, label="KDE")
    
    # Strike price
    ax.axvline(K, color="red", linestyle="--", linewidth=2, label=f"Strike K={K}")
    
    # Mean terminal price
    mean_terminal = np.mean(terminal_prices)
    ax.axvline(mean_terminal, color="green", linestyle="--", linewidth=2, 
               label=f"Mean S_T={mean_terminal:.2f}")
    
    ax.set_xlabel("Terminal Stock Price", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig
