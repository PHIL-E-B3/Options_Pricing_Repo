from miscellaneous import simulate_gbm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from colorama import Fore, Style
 
# ----------------------------------- CODING DOWN AND IN CALL (or PUT) ----------------------------------------------
 
# Here we define our initial parameters --------------------------------------------------
 
S_0 = 100
r = 0.04
sigma = 0.5
K = 100  # Strike price
BARRIER = 80  # Barrier level
n_sims = 100_000
T = 1
N = 252
dt = T / N
discount_factor = np.exp(-r * T)
observation = 'daily' #european if you want european
div_yield = 0.003


# Let's simulate the GBM paths here --------------------------------------------------
gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt, n_sims=n_sims, N=N, div_yield=div_yield)
 
def DownAndInPut(gbm_sims, K, BARRIER, discount_factor, observation='european'):
    """
    Prices an Down-And-In European Put with Monte-Carlo.
    observation = 'european' → barrier checked only at maturity
    observation = 'daily' → barrier checked every day
    """
 
    if observation.lower() == 'european':
        hit = gbm_sims[:, -1] < BARRIER # final prices min
    else: # 'daily'
        hit = gbm_sims.min(axis=1) < BARRIER # path-wise min
 
    payoff = np.where(
        hit, #value if true (checks each row to calculate the payoff with the last value(price) )
                                            # takes all rows (every simulated path) and -1 takes the last column (i.e. the value at the final time-step T)
        np.maximum(0, K - gbm_sims[:, -1]),
        0)
 
    if BARRIER > K:
        print("You should input a Barrier < K")
 
    premium = discount_factor * payoff.mean()
    print(f"Price of the Down and In Put: {premium:.4f}")
 
    hit = (gbm_sims.max(axis=1) >= BARRIER)
    hit_rate = hit.mean()
    print(f"{Fore.RED}Hit rate from MC simulation: {hit_rate * 100:.2f}%{Style.RESET_ALL}")
 
    return premium
 
# Sample of simulated paths + barrier / strike ----------------------------------------------
def plot_MC_DownAndInPut(n_sims, gbm_sims, BARRIER, K, show=True):
    plt.figure(figsize=(9,4))
    sample = np.random.choice(n_sims, size=min(30, n_sims), replace=False)
 
    for idx in sample:
        plt.plot(gbm_sims[idx], alpha=0.4)
    plt.axhline(BARRIER, color='red', ls='--', label=f'Barrier = {BARRIER}')
    plt.axhline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title('Subset of GBM paths')
    plt.xlabel('Time step')
    plt.ylabel('Underlying price')
    plt.legend()
    if show: 
        plt.show()
    
 
# Histogram of Monte-Carlo pay-offs (discounted) -----------------------------------------------
def plot_hist_DownAndInPut(show=True):        
    hit = gbm_sims.max(axis=1) > BARRIER
    payoffs = np.where(
        hit,
        np.maximum(0, K- gbm_sims[:,-1]),
        0)
 
    disc_pay = discount_factor * payoffs
 
    plt.figure(figsize=(6,4))
    plt.hist(disc_pay, bins=50, edgecolor='k', color='skyblue', alpha=0.7)
    plt.title('Distribution of discounted pay-offs')
    plt.xlabel('Pay-off')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.grid(True)
    if show: 
        plt.show()    


# Static payoff profile (undiscounted)----------------------------------------------------------------
def plot_DownAndInPut(show=True):
    x = np.linspace(0, BARRIER * 1.6, 600)  # Grid of S_T values
 
    # Short put payoff graph is min(S_t - X, 0)
    # Payoff logic for a down-and-in put
    payoff_profile = np.where(x <= BARRIER,  # If the barrier is breached
                            np.minimum(x - K, 0),  # Payoff is max(K - S_T, 0)
                            0)  # Otherwise, payoff is 0
 
    # Plotting the payoff profile
    plt.figure(figsize=(7, 4))
    plt.plot(x, payoff_profile, lw=2, label='Payoff')
    plt.axvline(BARRIER, color='red', ls='--', label=f'Barrier = {BARRIER}')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title('Down-and-In Put: Payoff vs Final Price $S_T$')
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Payoff at $T$ (undiscounted)')
    plt.legend()
    plt.grid(True, ls='--', lw=0.5)
    plt.tight_layout()
    if show: 
        plt.show()
 
   
if __name__ == "__main__":

    plot_DownAndInPut(show=False)
    DownAndInPut(gbm_sims=gbm_sims, K=K, BARRIER=BARRIER, discount_factor=discount_factor)
    plot_hist_DownAndInPut(show=False)
    plot_MC_DownAndInPut(n_sims=n_sims, gbm_sims=gbm_sims, BARRIER=BARRIER, K=K,show=False)
 
    plt.show()