import argparse

from src.pipeline import price_option_monte_carlo, summarize_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monte Carlo Options Pricing using Geometric Brownian Motion"
    )
    
    # Option parameters
    parser.add_argument(
        "--spot-price",
        type=float,
        default=100.0,
        help="Current stock price (default: 100.0)",
    )
    parser.add_argument(
        "--strike-price",
        type=float,
        default=100.0,
        help="Strike price (default: 100.0)",
    )
    parser.add_argument(
        "--time-to-expiration",
        type=float,
        default=1.0,
        help="Time to expiration in years (default: 1.0)",
    )
    parser.add_argument(
        "--risk-free-rate",
        type=float,
        default=0.05,
        help="Risk-free interest rate as decimal (default: 0.05)",
    )
    parser.add_argument(
        "--volatility",
        type=float,
        default=0.20,
        help="Annualized volatility as decimal (default: 0.20)",
    )
    parser.add_argument(
        "--option-type",
        type=str,
        choices=["call", "put"],
        default="call",
        help="Option type: call or put (default: call)",
    )
    
    # Simulation parameters
    parser.add_argument(
        "--num-simulations",
        type=int,
        default=10000,
        help="Number of Monte Carlo simulations (default: 10000)",
    )
    parser.add_argument(
        "--num-steps",
        type=int,
        default=252,
        help="Number of time steps per simulation (default: 252)",
    )
    
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    print("\nPricing option using Monte Carlo simulation...")
    print("This may take a moment...\n")
    
    results = price_option_monte_carlo(
        spot_price=args.spot_price,
        strike_price=args.strike_price,
        time_to_expiration=args.time_to_expiration,
        risk_free_rate=args.risk_free_rate,
        volatility=args.volatility,
        option_type=args.option_type,
        num_simulations=args.num_simulations,
        num_steps=args.num_steps,
    )
    
    summary = summarize_results(results)
    print(summary)


if __name__ == "__main__":
    main()
