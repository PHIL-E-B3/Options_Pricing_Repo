from gbm import simulate_gbm
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

# Choose the barrier type

'''

Use when ready to have user input functions:

S_0 = int(input("What's your initial price? ")) hashtag#initial price --> this will be automated once on Blab 
r = float(input("What's your RFR? "))
sigma = float(input("What's your vol in decimals? ")) hashtag#vol
T = int(input("What's your Maturity? ")) # 1year
N = 252 hashtag#no of trad. days
n_sims = int(input("How many MC Simulations do you want? "))
BARRIER = int(input("What's your Barrier: "))
K = int(input("What's your Strike? ")) hashtag#strike

'''

S_0 = 55
r = 0.06
sigma = 0.2
T = 1
N = 252

BARRIER = 65
K = 60
n_sims = 1000

observation = input("Please enter if you want 'european' or 'daily' observation: ")


dt = T / N
discount_factor = np.exp(-r * T)

gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt,n_sims=n_sims)
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

 payoff = np.where(hit, np.maximum(0, gbm_sims[:, -1] - K), 0)
 premium = discount_factor * payoff.mean()
 print(f"Price of the up-and-in call: {premium:.4f}")
 return premium

premium = UpAndInCall(gbm_sims=gbm_sims, K=K, BARRIER=BARRIER, discount_factor=discount_factor, observation=observation)


# 1) Sample of simulated paths + barrier / strike
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



# 2) Histogram of Monte-Carlo pay-offs (discounted)
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


# Cumulative knock-in fraction (up-and-in) ----------------------------------
# 1) Running maximum of each simulated path
cum_max = np.maximum.accumulate(gbm_sims, axis=1)

# 2) Has each path ever crossed the barrier?
cum_hit = (cum_max >= BARRIER)

# 3) At each time-step, what fraction of paths have knocked in so far?
knockin_ratio = cum_hit.mean(axis=0)

# 4) Plot
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
plt.show()


# Hit rate from Monte-Carlo simulation ----------------------
hit = (gbm_sims.max(axis=1) >= BARRIER)
hit_rate = hit.mean()
print(f"Hit rate from MC simulation: {hit_rate * 100:.2f}%")