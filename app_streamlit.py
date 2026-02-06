"""
Streamlit UI for Monte Carlo Options Pricing.

Run with:
    streamlit run app_streamlit.py
"""

from __future__ import annotations

import streamlit as st

from src.pipeline import price_option_monte_carlo
from src.visualizations import (
    plot_payoff_distribution,
    plot_price_paths,
    plot_terminal_price_distribution,
)


def main() -> None:
    st.title("Monte Carlo Options Pricing Simulator")
    
    st.markdown(
        """
This tool prices **European options** using **Monte Carlo simulation** with **Geometric Brownian Motion (GBM)**.

### How It Works
1. **Simulate** thousands of stock price paths using GBM: `dS = μS dt + σS dW`
2. **Calculate** option payoff for each terminal price
3. **Average** all payoffs and discount to present value
4. **Compare** with analytical Black-Scholes price

Monte Carlo is particularly useful for complex derivatives where closed-form solutions don't exist.
        """
    )
    
    with st.sidebar:
        st.header("Option Parameters")
        
        spot_price = st.number_input(
            "Spot Price (S₀)",
            min_value=1.0,
            max_value=1000.0,
            value=100.0,
            step=1.0,
            help="Current stock price",
        )
        
        strike_price = st.number_input(
            "Strike Price (K)",
            min_value=1.0,
            max_value=1000.0,
            value=100.0,
            step=1.0,
            help="Option strike price",
        )
        
        time_to_expiration = st.number_input(
            "Time to Expiration (years)",
            min_value=0.01,
            max_value=5.0,
            value=1.0,
            step=0.1,
            help="Time until option expires",
        )
        
        risk_free_rate = st.number_input(
            "Risk-Free Rate (%)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.5,
            help="Annualized risk-free interest rate",
        ) / 100
        
        volatility = st.number_input(
            "Volatility - σ (%)",
            min_value=1.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
            help="Annualized volatility (standard deviation)",
        ) / 100
        
        option_type = st.selectbox(
            "Option Type",
            options=["call", "put"],
            index=0,
        )
        
        st.header("Simulation Parameters")
        
        num_simulations = st.number_input(
            "Number of Simulations",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000,
            help="More simulations = more accurate but slower",
        )
        
        num_steps = st.number_input(
            "Time Steps per Path",
            min_value=10,
            max_value=1000,
            value=252,
            step=10,
            help="Number of steps to discretize each price path",
        )
        
        calculate_button = st.button("Calculate Option Price", type="primary")
    
    if not calculate_button:
        st.info("Configure parameters in the sidebar and click **Calculate Option Price**.")
        return
    
    # Run simulation
    with st.spinner("Running Monte Carlo simulation..."):
        try:
            results = price_option_monte_carlo(
                spot_price=spot_price,
                strike_price=strike_price,
                time_to_expiration=time_to_expiration,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                option_type=option_type,
                num_simulations=int(num_simulations),
                num_steps=int(num_steps),
            )
        except Exception as exc:
            st.error(f"Error during simulation: {exc}")
            return
    
    # Display results
    st.success(f"✅ Simulation complete with {int(num_simulations):,} paths!")
    
    # Price comparison
    st.subheader("Option Pricing Results")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Monte Carlo Price",
        f"${results.mc_price:.4f}",
        help="Estimated price from Monte Carlo simulation",
    )
    col2.metric(
        "Black-Scholes Price",
        f"${results.bs_price:.4f}",
        help="Theoretical price from Black-Scholes formula",
    )
    col3.metric(
        "Difference",
        f"{results.percentage_difference:.2f}%",
        help="Percentage difference between methods",
    )
    
    # Confidence interval
    st.write(f"**95% Confidence Interval:** [${results.mc_ci_lower:.4f}, ${results.mc_ci_upper:.4f}]")
    st.write(f"**Standard Error:** ${results.mc_std_error:.4f}")
    
    # Interpretation
    st.subheader("Interpretation")
    st.write(
        f"The Monte Carlo simulation estimates this **{option_type.upper()}** option is worth "
        f"**${results.mc_price:.4f}**, which is within **{results.percentage_difference:.2f}%** of the "
        f"Black-Scholes theoretical price of **${results.bs_price:.4f}**."
    )
    
    if results.percentage_difference < 1.0:
        st.success("✅ Excellent agreement! The Monte Carlo estimate closely matches Black-Scholes.")
    elif results.percentage_difference < 3.0:
        st.info("ℹ️ Good agreement. Small differences are expected due to Monte Carlo sampling.")
    else:
        st.warning("⚠️ Consider increasing the number of simulations for better accuracy.")
    
    # Visualizations
    st.subheader("Simulated Stock Price Paths")
    fig1 = plot_price_paths(
        results.mc_price_paths,
        results.spot_price,
        results.strike_price,
        results.time_to_expiration,
        num_paths_to_plot=min(100, int(num_simulations)),
    )
    st.pyplot(fig1)
    st.caption("Sample of simulated price paths showing possible stock price evolution over time.")
    
    st.subheader("Terminal Stock Price Distribution")
    fig2 = plot_terminal_price_distribution(
        results.mc_price_paths,
        results.strike_price,
        option_type,
    )
    st.pyplot(fig2)
    st.caption("Distribution of stock prices at expiration (S_T).")
    
    st.subheader("Option Payoff Distribution")
    fig3 = plot_payoff_distribution(
        results.mc_payoffs,
        results.mc_price,
        results.bs_price,
        option_type,
    )
    st.pyplot(fig3)
    st.caption("Distribution of option payoffs at expiration, before discounting.")
    
    # Summary statistics
    st.subheader("Simulation Statistics")
    col1, col2 = st.columns(2)
    
    terminal_prices = results.mc_price_paths[:, -1]
    col1.metric("Mean Terminal Price", f"${terminal_prices.mean():.2f}")
    col1.metric("Std Dev (Terminal)", f"${terminal_prices.std():.2f}")
    
    col2.metric("Mean Payoff", f"${results.mc_payoffs.mean():.2f}")
    col2.metric("Max Payoff", f"${results.mc_payoffs.max():.2f}")
    
    # Option Greeks info
    with st.expander("ℹ️ About Monte Carlo vs Black-Scholes"):
        st.markdown(
            """
**Monte Carlo Simulation:**
- Numerically estimates option prices by simulating many possible future price paths
- Flexible and can handle complex payoffs and path-dependent options
- Convergence rate: Error decreases as 1/√N (N = number of simulations)
- Useful when no closed-form solution exists

**Black-Scholes Formula:**
- Provides exact analytical solution for European options
- Assumes log-normal distribution of stock prices
- Instant calculation, no simulation needed
- Serves as a benchmark to validate Monte Carlo accuracy

**Why the small difference?**
Monte Carlo is a statistical method with inherent sampling error. More simulations reduce this error.
For European options on non-dividend-paying stocks, both methods should converge to the same price.
            """
        )


if __name__ == "__main__":
    main()
