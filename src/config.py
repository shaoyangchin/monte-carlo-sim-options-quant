from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class DefaultConfig:
    """
    Default configuration for Monte Carlo options pricing.
    """

    # Option parameters
    spot_price: float = 100.0  # Current stock price (S0)
    strike_price: float = 100.0  # Strike price (K)
    time_to_expiration: float = 1.0  # Time to expiration in years (T)
    risk_free_rate: float = 0.05  # Risk-free interest rate (r)
    volatility: float = 0.20  # Annualized volatility (sigma)
    
    # Option type
    option_type: str = "call"  # "call" or "put"
    
    # Monte Carlo parameters
    num_simulations: int = 10000  # Number of price paths to simulate
    num_steps: int = 252  # Number of time steps (trading days in a year)
    
    # Market data for volatility estimation
    ticker: str = "AAPL"
    lookback_days: int = 252  # Use 1 year of data for volatility estimation
    
    @property
    def start_date(self) -> date:
        return date.today() - timedelta(days=self.lookback_days + 30)
    
    @property
    def end_date(self) -> date:
        return date.today() - timedelta(days=1)
