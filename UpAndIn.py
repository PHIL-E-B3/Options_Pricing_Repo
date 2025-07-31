from miscellaneous import simulate_gbm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from colorama import Fore, Style
# Choose the barrier type
 
S_0 = 330.15 # NVDA current price
r = 0.03974
sigma = 0.5
T = 1
N = 252 * T
 
BARRIER = 200
K = S_0 * 1.0 # change according to
n_sims = 10000
div_yield = 0.03833
 
observation = 'european' #change to daily if daily
 
dt = T / N
discount_factor = np.exp(-r * T)
 
gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt,n_sims=n_sims,N=N,div_yield=div_yield)
print(gbm_sims.shape)
 
def UpAndInCall(gbm_sims, K, BARRIER, discount_factor, observation='european'):
    """
   
    Prices an up-and-in European call.
    observation = 'european' → barrier checked only at maturity
    observation = 'daily' → barrier checked every day
 
    """
    if observation.lower() == 'european':
        hit = gbm_sims[:, -1] >= BARRIER # final prices only
    else: # 'daily'
        hit = gbm_sims.max(axis=1) >= BARRIER # path-wise max
 
    # Payoff: (payoff function explained: if the hit condition is met, i.e. that the last MC path is >= to the BARRIER,
    # the payoff is the max between the last price - K or 0. In addition, if the condition is not met, then the output is also 0)
 
    payoff = np.where(
        hit, # final price of the MC paths that are subject to a >= barrier logic
        np.maximum(0, gbm_sims[:, -1] - K), # array will be created based
        0
    )
 
    premium = discount_factor * payoff.mean()
    print(f"{Fore.RED}Price of the up-and-in Call: {premium:.4f}{Style.RESET_ALL}")
 
    hit = (gbm_sims.max(axis=1) >= BARRIER)
    hit_rate = hit.mean()
    print(f"{Fore.RED}Hit rate from MC simulation: {hit_rate * 100:.2f}%{Style.RESET_ALL}")
 
    return premium


# 1) Sample of simulated paths + barrier / strike ---------------------------------------------------
 
def plot_MC_UpAndInCall(show=True):
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


# 2) Histogram of Monte-Carlo pay-offs (discounted) -----------------------------------------
def plot_hist_UpAndInCall(show=True):
    hit = gbm_sims.max(axis=1) > BARRIER
    payoffs = np.where(
        hit,
        np.maximum(0, gbm_sims[:,-1] - K),
        0)
 
    disc_pay = discount_factor * payoffs
 
    plt.figure(figsize=(6,4))
    plt.hist(disc_pay, bins=50, edgecolor='k')
    plt.title('Distribution of discounted pay-offs')
    plt.xlabel('Pay-off')
    plt.ylabel('Frequency')
    plt.grid(True)
    if show:
        plt.show()
 
# Cumulative knock-in fraction (up-and-in) ------------------------------------------------------
 
def plot_cum_KI(show=True):
    cum_max = np.maximum.accumulate(gbm_sims, axis=1)
 
    cum_hit = (cum_max >= BARRIER)
 
    knockin_ratio = cum_hit.mean(axis=0)
 
    plt.figure(figsize=(6, 4))
    plt.plot(knockin_ratio, lw=2)
    plt.title('Cumulative fraction of paths that have knocked in')
    plt.xlabel('Time step')
    plt.ylabel('Knock-in probability so far')
    plt.ylim(0, 1) # keeps the line inside the frame
    plt.grid(True, ls='--', lw=0.5)
    plt.tight_layout()
    if show:
        plt.show()
 
# Static payoff profile (undiscounted) ------------------------------------------------------
 
def plot_UpAndInCall(show=True):
    x = np.linspace(0, BARRIER * 1.6, 600) # grid of S_T values (barrier x 1.6 ensures the whole price path is as least as big as 1.6 times the barrier)
 
    payoff_profile = np.where(x >= BARRIER,
    np.maximum(0, x - K),
    0)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, payoff_profile, lw=2, label='Payoff')
    plt.axvline(BARRIER, color='red', ls='--', label=f'Barrier = {BARRIER}')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Up-and-in Call ({observation} observation): Payoff vs Final Price $S_T$")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Payoff at $T$ (undiscounted)')
    plt.legend()
    plt.grid(True, ls='--', lw=0.5)
    plt.tight_layout()
    if show:
        plt.show()




def plot_all_UpAndIn():
    UpAndInCall(gbm_sims=gbm_sims, K=K, BARRIER=BARRIER, discount_factor=discount_factor, observation=observation)
    plot_UpAndInCall(show=False)
    plot_cum_KI(show=False)
    plot_hist_UpAndInCall(show=False)
    plot_MC_UpAndInCall(show=False)
    plt.show()
 
if __name__ == "__main__":
    plot_all_UpAndIn()