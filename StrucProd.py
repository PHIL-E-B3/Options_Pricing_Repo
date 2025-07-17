import numpy as np
from scipy.stats import norm
from Vanilla.blackscholesvanilla import black_scholes_call_value, black_scholes_put_value, N, BullSpread_Price
from Vanilla.vanilla_greeks import call_delta, put_delta
import numpy as np
 
# BullSpread ----------------------------------------------------------------------------------- Bullspread price + plot
 
def BullSpread_Price(
                    S, #initial price
                    K,  #strike will always equal spot price * a parameter  
                    r,
                    T,
                    long_call_strike,
                    short_call_strike,
                    short_put_strike,
                    long_put_strike,
                    ATM_vol,
                    short_call_vol,
                    long_put_vol
                    ):
    '''
    Parameters:
    long_call_strike = if atm, then input = 1
    short_call_strike = if otm (e.g. 120%) input 1.2
    short_put_strike = if atm then input = 1
    long_put_strike = if otm then (e.g. 80%), then input = 0.8
    '''
 
    long_call = black_scholes_call_value(S, K * long_call_strike, r, T, ATM_vol)
    short_call = black_scholes_call_value(S, K * short_call_strike, r, T, short_call_vol)
    short_put = black_scholes_put_value(S, K * short_put_strike, r, T, ATM_vol)
    long_put = black_scholes_put_value(S, K * long_put_strike, r, T, long_put_vol)
 
    BullSpread_Price = long_call - short_call - short_put + long_put
   
    print(f"BullSpread Premium: {BullSpread_Price:.2f}")
 
    # Plotting:
 
    # Define payoff functions
    call_payoff = lambda S, K: np.maximum(S - K, 0.0)
    put_payoff = lambda S, K: np.maximum(K - S, 0.0)
 
    # Generate a range of stock prices at expiration
    S_range = np.linspace(S * 0.5, S * 1.5, 100)
 
    # Calculate payoffs for each leg of the strategy
    long_call_payoff = call_payoff(S_range, K * long_call_strike)
    short_call_payoff = -call_payoff(S_range, K * short_call_strike)
    short_put_payoff = -put_payoff(S_range, K * short_put_strike)
    long_put_payoff = put_payoff(S_range, K * long_put_strike)
 
    # Total payoff of the bull spread
    total_payoff = long_call_payoff + short_call_payoff + short_put_payoff + long_put_payoff
 
    # Plot the payoff diagram
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, total_payoff, label='Bull Spread Payoff', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
 
    # Add strike levels to the legend
    plt.plot([], [], ' ', label=f'Long Call Strike: {K * long_call_strike:.2f}')
    plt.plot([], [], ' ', label=f'Short Call Strike: {K * short_call_strike:.2f}')
    plt.plot([], [], ' ', label=f'Short Put Strike: {K * short_put_strike:.2f}')
    plt.plot([], [], ' ', label=f'Long Put Strike: {K * long_put_strike:.2f}')
   
 
    # Annotate the premium on the graph
    plt.text(S * 1.3, 4, f'Premium: {BullSpread_Price:.2f}', fontsize=12, color='red',
             bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'))
 
    plt.title('Bull Spread Payoff Diagram')
    plt.xlabel('Stock Price at Expiration')
    plt.ylabel('Payoff')
    plt.legend()
    plt.show()
 
    return BullSpread_Price
 
# BullSpreadDelta ------------------------------------------------------------------------------------------------------BullSpreadDelta
 
def BullSpread_delta(K,
                     r,
                     vol,
                     long_call_strike,
                     short_call_strike,
                     short_put_strike,
                     long_put_strike,
                     *maturities):
   
    x = np.linspace(0.01, K * 1.6, 600)
   
    plt.figure(figsize=(7, 4))
   
    for T in maturities:
        delta_values_long_call = [call_delta(number, K * long_call_strike, r, T, vol) for number in x]
        delta_values_short_call = [call_delta(number, K * short_call_strike, r, T, vol) for number in x]
        delta_values_short_put = [put_delta(number, K * short_put_strike, r, T, vol) for number in x]
        delta_values_long_put = [put_delta(number, K * long_put_strike, r, T, vol) for number in x]
        bull_spread_delta = delta_values_long_call + delta_values_short_call + delta_values_short_put + delta_values_long_put
        plt.plot(x, bull_spread_delta, lw=2, label=f'Delta (T={T})')
 
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title("Vanilla Call Delta for Different Maturities")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Delta')
    plt.legend()
    plt.tight_layout()
    plt.show()





## General Struc Prod ----------------------------------------------------------------------------------------- General Struc prod
 
import numpy as np
import matplotlib.pyplot as plt
 
# Assuming call_delta and put_delta functions are already defined
def call_delta(S, K, r, T, vol):
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)
 
def put_delta(S, K, r, T, vol):
    from scipy.stats import norm
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1) - 1
 
def structured_product_delta(S, r, vol, time_points, components, plot=False):
    deltas = {}
    for T in time_points:
        total_delta = 0
        for component in components:
            if component['type'] == 'call':
                delta = call_delta(S, component['strike'], r, T, vol)
            elif component['type'] == 'put':
                delta = put_delta(S, component['strike'], r, T, vol)
            else:
                delta = 0  # For non-option components like bonds
            total_delta += component['position'] * delta
        deltas[T] = total_delta
 
    # Print deltas
    for T, delta in deltas.items():
        print(f"Delta at T={T} years: {delta:.4f}")
 
    # Plot deltas if requested
    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, list(deltas.values()), marker='o', label=f"Delta for S={S}, vol={vol}")
        plt.xlabel("Time to Maturity (Years)")
        plt.ylabel("Delta")
        plt.title("Delta vs Time to Maturity")
        plt.legend()
        plt.grid()
        plt.show()
 
    return deltas
 
# Example usage
if __name__ == "__main__":
    # Define parameters
    S_values = [90, 100, 110]  # Different stock prices
    r = 0.05  # Risk-free rate
    vol_values = [0.2, 0.3]  # Different volatilities
    time_points = [0.5, 1, 2]  # Time to maturities
    components = [
        {'type': 'call', 'strike': 100, 'position': 1},
        {'type': 'put', 'strike': 90, 'position': -1}
    ]
 
    # Loop through different prices and volatilities
    for S in S_values:
        for vol in vol_values:
            print(f"\nCalculating deltas for S={S}, vol={vol}")
            structured_product_delta(S, r, vol, time_points, components, plot=True)


# Bull spread call deltas ------------------------------------------------------------------------------- bull spread call delta
 
# Here we define our initial parameters --------------------------------------------------
 
#!/usr/bin/env python3
"""
Bull-Spread Pricing & Delta Plot
--------------------------------
• Accepts a *single* params dictionary:
params = {
"K1": 95.0, # lower strike
"K2": 105.0, # upper strike
"scenarios": [ # exactly three maturities
{"S": 100, "sigma": 0.25, "r": 0.03, "T": 1.0 },
{"S": 100, "sigma": 0.24, "r": 0.028, "T": 0.5 },
{"S": 100, "sigma": 0.22, "r": 0.025, "T": 0.25},
]
}
 
• Prints each maturity’s price.
• Plots the bull-spread Δ vs underlying for all three maturities.
------------------------------------------------------------------
"""
 
from typing import Dict, List
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
 
# ---------------------------------------------------------------------------
# Fallback Black-Scholes building blocks (replace if you already have these)
# ---------------------------------------------------------------------------
def bs_call_price(S: float, K: float, r: float, T: float, sigma: float) -> float:
    """European call price (Black-Scholes, continuous compounding)."""
    if T <= 0 or sigma <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
 
def default_call_delta(S: float, K: float, r: float, T: float, sigma: float) -> float:
    """European call delta (Black-Scholes)."""
    if T <= 0 or sigma <= 0:
        return 1.0 if S > K else 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)
 
# If the user already defined call_delta/put_delta, import them;
# otherwise fall back to the implementation above.
try:
    from __main__ import call_delta as user_call_delta # noqa: F401
    call_delta = user_call_delta # type: ignore
except ImportError:
    call_delta = default_call_delta # type: ignore
 
# ---------------------------------------------------------------------------
# Bull-spread helpers
# ---------------------------------------------------------------------------
def bull_spread_price(S: float, K1: float, K2: float,
                    r: float, T: float, sigma: float) -> float:
    """Price of a long call bull-spread = long call(K1) − short call(K2)."""
    return bs_call_price(S, K1, r, T, sigma) - bs_call_price(S, K2, r, T, sigma)
 
def bull_spread_delta(S: np.ndarray, K1: float, K2: float,
    r: float, T: float, sigma: float) -> np.ndarray:
    """Delta of a long call bull-spread."""
    return call_delta(S, K1, r, T, sigma) - call_delta(S, K2, r, T, sigma)
 
# ---------------------------------------------------------------------------
# Core routine
# ---------------------------------------------------------------------------
def run_pricing(params: Dict) -> None:
    """
    Parameters
    ----------
    params : dict
    Must contain:
    • "K1", "K2" (floats)
    • "scenarios": list of exactly three dicts, each with keys
    "S", "sigma", "r", "T"
    """
    K1: float = params["K1"]
    K2: float = params["K2"]
    scenarios: List[Dict] = params["scenarios"]
 
    if len(scenarios) != 3:
        raise ValueError("Provide *exactly* three maturity scenarios")
 
    # ---- Pricing ----
    print("\n=== Bull-Spread Prices ===")
    for idx, sc in enumerate(scenarios, 1):
        price = bull_spread_price(sc["S"], K1, K2, sc["r"], sc["T"], sc["sigma"])
        print(f"Scenario {idx}: T={sc['T']:.3f}y Price = {price:,.4f}")
 
    # ---- Delta plot ----
    S_grid = np.linspace(
        0.5 * min(sc["S"] for sc in scenarios),
        1.5 * max(sc["S"] for sc in scenarios),
        250,
    )
 
    plt.figure(figsize=(8, 5))
    for sc in scenarios:
        deltas = bull_spread_delta(S_grid, K1, K2, sc["r"], sc["T"], sc["sigma"])
        plt.plot(S_grid, deltas, label=f"T = {sc['T']:.2f} yr")
 
    plt.title("Bull-Spread Δ vs Underlying Price")
    plt.xlabel("Underlying price S")
    plt.ylabel("Delta of bull-spread")
    plt.axhline(0, lw=0.8, ls="--", alpha=0.6)
    plt.legend()
    plt.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    plt.show()
 
# ---------------------------------------------------------------------------
# Demo usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_params = {
        "K1": 95.0,
        "K2": 105.0,
        "scenarios": [
        {"S": 100, "sigma": 0.25, "r": 0.03, "T": 1.0},
        {"S": 100, "sigma": 0.24, "r": 0.028, "T": 0.5},
        {"S": 100, "sigma": 0.22, "r": 0.025, "T": 0.25},
        ],
    }
    run_pricing(demo_params)