# Coding the final payoff, graph etc. of a Down and In Put Option

from gbm import simulate_gbm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
# Here we define our initial parameters --------------------------------------------------
 
S_0 = 100
r = 0.06
sigma = 0.5
 
BARRIER = 45
K = 60
n_sims = 100_000
 
T = 1
N = 252
dt = T / N
discount_factor = np.exp(-r * T)
 
observation = input("Please enter if you want 'european' or 'daily' observation: ")
 
# Let's simulate the GBM paths here --------------------------------------------------
gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt,n_sims=n_sims)
 
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
 
    premium = discount_factor * payoff.mean()
    print(f"Price of the Down and In put: {premium:.4f}")
    return premium
 
premium = DownAndInPut(gbm_sims=gbm_sims, K=K, BARRIER=BARRIER, discount_factor=discount_factor)


# Sample of simulated paths + barrier / strike ----------------------------------------------
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
 
# Histogram of Monte-Carlo pay-offs (discounted) -----------------------------------------------
hit = gbm_sims.max(axis=1) > BARRIER
payoffs = np.where(
    hit,
    np.maximum(0, K- gbm_sims[:,-1]),
    0)
 
disc_pay = discount_factor * payoffs
 
plt.figure(figsize=(6,4))
plt.hist(disc_pay, bins=50, edgecolor='k')
plt.title('Distribution of discounted pay-offs')
plt.xlabel('Pay-off')
plt.ylabel('Frequency')
plt.grid(True)
 
# Cumulative knock-in fraction (up-and-in) ----------------------------------
 
cum_max = np.maximum.accumulate(gbm_sims, axis=1) # Running maximum of each simulated path
cum_hit = (cum_max <= BARRIER) # Has each path ever crossed the barrier?
knockin_ratio = cum_hit.mean(axis=0) # At each time-step, what fraction of paths have knocked in so far?
 
plt.figure(figsize=(6, 4))
plt.plot(knockin_ratio, lw=2)
plt.title('Cumulative fraction of paths that have knocked in')
plt.xlabel('Time step')
plt.ylabel('Knock-in probability so far')
plt.ylim(0, 1) # keeps the line inside the frame
plt.grid(True, ls='--', lw=0.5)
plt.tight_layout()



# Static payoff profile (undiscounted) ---------------------------
x = np.linspace(0, BARRIER * 1.6, 600) # grid of S_T values (barrier x 1.6 ensures the whole price path is as least as big as 1.6 times the barrier)
 
payoff_profile = np.where(x <= BARRIER,
 np.maximum(0, K - x),
 0)
 
plt.figure(figsize=(7, 4))
plt.plot(x, payoff_profile, lw=2, label='Payoff')
plt.axvline(BARRIER, color='red', ls='--', label=f'Barrier = {BARRIER}')
plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
plt.title('Down-and-In Put : Payoff vs Final Price $S_T$')
plt.xlabel(r'Final underlying price $S_T$')
plt.ylabel('Payoff at $T$ (undiscounted)')
plt.legend()
plt.grid(True, ls='--', lw=0.5)
plt.tight_layout()
plt.show()
 
# Hit rate from Monte-Carlo simulation ----------------------
hit = (gbm_sims.max(axis=1) <= BARRIER)
hit_rate = hit.mean()
print(f"Hit rate from MC simulation: {hit_rate * 100:.2f}%")