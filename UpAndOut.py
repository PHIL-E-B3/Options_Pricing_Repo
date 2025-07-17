from miscellaneous import simulate_gbm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from colorama import Fore, Style
 
# ----------------------------------- CODING AN UP AND OUT CALL (Or Put) ----------------------------------------------
 
S_0 = 55
r = 0.06
sigma = 0.2
T = 1
N = 252
 
BARRIER = 80
K = 60
n_sims = 10000
 
# Deciding if the observation will be european or daily -------------------------------------
 
dt = T / N
discount_factor = np.exp(-r * T)
 
# Let's simulate the GBM paths here --------------------------------------------------
 
def UpAndOut(gbm_sims, K, BARRIER, discount_factor, observation='european', option_type='call'):
    """
   
    Prices an up-and-out European call or put.
    observation = 'european' → barrier checked only at maturity
    observation = 'daily' → barrier checked every day
 
    """
 
    # European or Daily observation
 
    if observation.lower() == 'european':
        hit = gbm_sims[:, -1] >= BARRIER # final prices only
    else: # 'daily'
        hit = gbm_sims.max(axis=1) >= BARRIER # path-wise max
 
    # Option or call
    if option_type.lower() == 'call':
        payoff = np.where(hit, 0, np.maximum(0, gbm_sims[:, -1] - K))
    else:
        payoff = np.where(hit, 0, np.maximum(0, K - gbm_sims[:, -1]))
   
    premium = discount_factor * payoff.mean()
    print(f"{Fore.RED}Price of the up-and-in {option_type}: {premium:.4f}{Style.RESET_ALL}")
 
    hit_rate = hit.mean()
    print(f"{Fore.RED}Hit rate from MC simulation: {hit_rate * 100:.2f}%{Style.RESET_ALL}")
 
    return premium
 
# Plot 1) Sample of simulated paths + barrier / strike -------------------------------------------
def UpAndOut_MC_plot():
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
    plt.show()
 
# Plot 2) Histogram of Monte-Carlo pay-offs (discounted)
def UpAndOut_hist(option_type, discount_factor):
 
    if observation.lower() == 'european':
        hit = gbm_sims[:, -1] >= BARRIER # final prices only
    else: # 'daily'
        hit = gbm_sims.max(axis=1) >= BARRIER # path-wise max
 
    if option_type.lower() == 'call':
        payoff = np.where(hit, 0, np.maximum(0, gbm_sims[:, -1] - K))
    else:
        payoff = np.where(hit, 0, np.maximum(0, K - gbm_sims[:, -1]))
 
    disc_pay = discount_factor * payoff
 
    plt.figure(figsize=(6,4))
    plt.hist(disc_pay, bins=50, edgecolor='k')
    plt.title('Distribution of discounted pay-offs')
    plt.xlabel('Pay-off')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
 
# Plot 3) Static payoff profile (undiscounted) ---------------------------------
 
def UpAndOut_plot(option_type):
 
    x = np.linspace(0, BARRIER * 1.6, 600) # grid of S_T values (barrier x 1.6 ensures the whole price path is as least as big as 1.6 times the barrier)
 
    if option_type.lower() == 'call':
        payoff_profile = np.where(x >= BARRIER, 0, np.maximum(0, x - K))
    else: # 'put'
        payoff_profile = np.where(x <= BARRIER, 0, np.maximum(0, K - x))
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, payoff_profile, lw=2, label='Payoff')
    plt.axvline(BARRIER, color='red', ls='--', label=f'Barrier = {BARRIER}')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Up-and-Out {option_type} ({observation} observation): Payoff vs Final Price $S_T$")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Payoff at $T$ (undiscounted)')
    plt.legend()
    plt.grid(True, ls='--', lw=0.5)
    plt.tight_layout()
    plt.show()
 
#if you want to test out the file use: ---------------------------------------------------------------------
 
'''
gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt,n_sims=n_sims)
print(f"The shape of the GeomBM paths is: {gbm_sims.shape}")
 
observation = input("Please enter if you want 'european' or 'daily' observation: ").strip().lower()
option_type = input("Are you pricing a call or put? (enter 'call' or 'put'): ").strip().lower()
 
if observation not in ['european', 'daily']:
    raise ValueError("Invalid observation type. Please enter 'european' or 'daily'.")
if option_type not in ['call', 'put']:
    raise ValueError("Invalid option type. Please enter 'call' or 'put'.")
 
print("Generating plots and calculating the option price...")
 
UpAndOut_plot(option_type=option_type)
 
UpAndOut_hist(option_type=option_type, discount_factor=discount_factor)
 
premium = UpAndOut(
    gbm_sims=gbm_sims,
    K=K,
    BARRIER=BARRIER,
    discount_factor=discount_factor,
    observation=observation,
    option_type=option_type
)
 
UpAndOut_MC_plot()
print(f"All tasks completed. The calculated premium is: {premium:.4f}")
'''