import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
 
# now imports from our files
from miscellaneous import simulate_gbm
from DownAndInPut import DownAndInPut, plot_hist_DownAndInPut, plot_DownAndInPut
from UpAndIn import UpAndInCall, plot_UpAndInCall
from UpAndOut import UpAndOut, UpAndOut_hist, UpAndOut_plot, UpAndOut_MC_plot
from Vanilla.blackscholesvanilla import black_scholes_call_value, black_scholes_put_value
from Vanilla.VanillaCall_Plotting import plot_call_payoff
from exotic_greeks import (call_vomma,put_vomma,call_vanna,put_vanna,call_charm,put_charm,call_zomma,put_zomma,call_color,put_color,call_speed,put_speed,call_ultima,put_ultima,plot_vomma_,plot_vanna_,plot_charm_,plot_zomma_,plot_color_,plot_speed_,plot_ultima_)
 
from Vanilla.vanilla_greeks import (phi, gamma, vega, call_delta, call_theta, call_rho, put_delta, put_theta, put_rho, plot_call_theta_, plot_gamma_, plot_call_rho_, plot_vega_, plot_call_delta_, plot_call_greeks_, plot_multiple_deltas, plot_all_greeks)



# Here we define our initial parameters ------------------------------------------------------------- init parameters
 
n_sims = 100_000
N = 252
S = 32.21
K = 32.21
r = 3.97
T = 1
div_yield =
 
maturities = [2,1,0.5]
 
# strikes
long_call_strike = 1.00  # ATM
short_call_strike = 1.20  # 20 % OTM
short_put_strike = 1.00  # ATM
long_put_strike = 0.98  # 2 % OTM
 
# vol
ATM_vol = 0.295
short_call_vol = 0.33
long_put_vol = 0.292
 
vol = 0.33
 
greek_you_want = 'delta'


# the demo-parameters you will build
u
 
# N.B. Here, you choose the underlying price scenario yourself - this can be done with a Monte-carlo simulation if wanted, and you could extract 3 random prices if you wanted to, for example.  
 
demo_params = {
    "K": 100.0,
    "scenarios": [
        {"S": 120, "sigma": 0.33, "r": 0.04, "T": 2.0},
        {"S": 150, "sigma": 0.45, "r": 0.04, "T": 1.0},
        {"S": 130, "sigma": 0.40, "r": 0.04, "T": 0.5},
    ],
}


# BullSpread ----------------------------------------------------------------------------------- Bullspread price + plot
 
def BullSpread_Price(
                    S, #initial price
                    K,  #strike will always equal spot price * a parameter  
                    r,
                    T,
                    show=True):
 
    '''
    Parameters:
    long_call_strike = if atm, then input = 1
    short_call_strike = if otm (e.g. 120%) input 1.2
    short_put_strike = if atm then input = 1
    long_put_strike = if otm then (e.g. 80%), then input = 0.8
    '''
 
    # calculate option values
    long_call = black_scholes_call_value(S, K * long_call_strike, r, T, ATM_vol)
    short_call = black_scholes_call_value(S, K * short_call_strike, r, T, short_call_vol)
    short_put = black_scholes_put_value(S, K * short_put_strike, r, T, ATM_vol)
    long_put = black_scholes_put_value(S, K * long_put_strike, r, T, long_put_vol)
 
    BullSpread_Price = long_call - short_call - short_put + long_put # total value of the BullSpread Price
   
    return BullSpread_Price


def plot_BullSpread(
                    S, #initial price
                    K,  #strike will always equal spot price * a parameter  
                    r,
                    T,
                    show=True
                    ):
 
                                                                           
                                                                                                           
        # Plotting:
 
        # Define payoff functions
        call_payoff = lambda S, K: np.maximum(S - K, 0.0)
        put_payoff = lambda S, K: np.maximum(K - S, 0.0)
 
        # Generate a range of stock prices at expiration
        S_range = np.linspace(S * 0.5, S * 1.5, 100)
 
        # Calculate final day payoffs for each leg of the strategy
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
       
 
        # REMOVE IF YOU DON'T WANT TO SEE THE PREMIUM ON THE GRAPH:
 
        plt.text(S * 1.3, 4, f'Premium: {BullSpread_Price:.2f}', fontsize=12, color='red',
                bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'))
 
        plt.title('Bull Spread Payoff Diagram')
        plt.xlabel('Stock Price at Expiration')
        plt.ylabel('Payoff')
        plt.legend()
 
        if show:
            plt.show()





function_dictionary = {
    "delta": {"call": "call_delta", "put": "put_delta"},
    "gamma": {"call": "gamma", "put": "gamma"},             # Gamma is the same for both calls and puts
    "vega": {"call": "vega", "put": "vega"},                # Vega is the same for both calls and puts
    "theta": {"call": "call_theta", "put": "put_theta"},
    "rho": {"call": "call_rho", "put": "put_rho"},
    "vomma": {"call": "call_vomma", "put": "put_vomma"},   # Vomma (volga) measures sensitivity to volatility
    "vanna": {"call": "call_vanna", "put": "put_vanna"},   # Vanna measures sensitivity to changes in volatility and spot price
    "charm": {"call": "call_charm", "put": "put_charm"},   # Charm measures the rate of change of delta over time
    "zomma": {"call": "call_zomma", "put": "put_zomma"},   # Zomma measures the rate of change of gamma with respect to spot price
    "color": {"call": "call_color", "put": "put_color"},   # Color measures the rate of change of gamma over time
    "speed": {"call": "call_speed", "put": "put_speed"},   # Speed measures the rate of change of gamma with respect to spot price
    "ultima": {"call": "call_ultima", "put": "put_ultima"} # Ultima measures the sensitivity of vomma to changes in volatility
}
 
# here the user will be able to dynamically change the greek depending on what he wants. the greek will be then dynamically searched in a dictionary and spit out the corresponding bull spread greek
def bull_spread_greek(S, K, r, T, greek_you_want):
    """
    Vectorised—S can be scalar or array.
    The function dynamically selects the appropriate Greek calculation based on user input.
    """
    # Get the function references for the specified Greek
    call_function = globals()[function_dictionary[greek_you_want]["call"]] # globals will dynamically rerieve actual function objects (if not you return a string)
    put_function = globals()[function_dictionary[greek_you_want]["put"]]
   
    # Call the functions directly
    long_call = call_function(S, K * long_call_strike, r, T, ATM_vol)
    short_call = -call_function(S, K * short_call_strike, r, T, short_call_vol)
    short_put = -put_function(S, K * short_put_strike, r, T, ATM_vol)
    long_put = put_function(S, K * long_put_strike, r, T, long_put_vol)
   
    return long_call + short_call + short_put + long_put
 
# --- Driver --------------------------------------------------------------------------------------------
 
def bull_greek_scenarios(params, greek_you_want, show=True):
    """
    params = {
        "K": 100.0,
        "scenarios": [
            {"S": 120, "sigma": 0.33, "r": 0.04, "T": 1.5},
            {"S": 150, "sigma": 0.45, "r": 0.04, "T": 1.0},
            {"S": 130, "sigma": 0.40, "r": 0.04, "T": 0.5},
        ],
    }
    Only K and the three scenarios matter; vol inside scenarios is ignored
    because the strategy already has its own leg-specific vols.
    """
   
    K = params["K"]
    scenarios = params["scenarios"]
    if len(scenarios) != 3:
        raise ValueError("Need exactly three maturity scenarios")
 
    print("\n=== Bull-Spread Prices ===")
    for i, sc in enumerate(scenarios, 1):
        price = BullSpread_Price(sc["S"], K, sc["r"], sc["T"])
        print(f"Scenario {i}: T={sc['T']:.2f}y Price = {price:,.4f}")
 
    S_grid = np.linspace(0.5 * min(sc["S"] for sc in scenarios),
                         1.5 * max(sc["S"] for sc in scenarios), 250)
 
    plt.figure(figsize=(8, 5))
    for sc in scenarios:
        greeks_ = bull_spread_greek(S_grid, K, sc["r"], sc["T"], greek_you_want)
        plt.plot(S_grid, greeks_, label=f"T = {sc['T']:.2f} yr")
 
    plt.title(f"Bull-Spread {greek_you_want} vs Underlying Price")
    plt.xlabel("Underlying price S")
    plt.ylabel(f"{greek_you_want}")
    plt.axhline(0, lw=0.8, ls="--", alpha=0.6)
    plt.legend()
    plt.grid(True, ls=":", alpha=0.5)
    plt.tight_layout()
    if show:
        plt.show()


# ---------------------------------------------------------------------------
# Demo usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
 
    # problem to solve: it'll print first the graph, and then the price
 
    BullSpreadPrice = BullSpread_Price(
                    S=S,
                    K=K,  
                    r=r,
                    T=T,
                    show=False
                    )
   
    # printing it noicely:
    text = f"BullSpread Premium: {BullSpreadPrice:.2f}"
    box_width = len(text) + 2
    print(
        f"╔{'═' * box_width}╗\n"
        f"║ {text.center(box_width - 2)} ║\n"
        f"╚{'═' * box_width}╝"
    )
 
    #second step: plotting the deltas
 
    bull_greek_scenarios(demo_params, greek_you_want=greek_you_want, show=False)
 
    # the greek
 
    bull_spread_greek = bull_spread_greek(
                                        S=S,
                                        K=K,
                                        r=r,
                                        T=T,
                                        greek_you_want=greek_you_want
                                        )
                     
    text_2 = f"BullSpread Delta: {bull_spread_greek:.2f}"
    box_width = len(text_2) + 2
    print(
        f"╔{'═' * box_width}╗\n"
        f"║ {text_2.center(box_width - 2)} ║\n"
        f"╚{'═' * box_width}╝"
 
       
    )
 
    plot_BullSpread(
                    S=S, #initial price
                    K=K,  #strike will always equal spot price * a parameter  
                    r=r,
                    T=T,
                    show=True
                    )
 
   
    plt.show()
 