import numpy as np
import matplotlib.pyplot as plt
import seaborn

##----------------------------------##
# PAYOFF AT EXPIRATION #
##----------------------------------##

count = 0
while True:
    corr_string_1 = 'short'
    corr_string_2 = 'long'
    try:
        short_OR_long = input("short or long: ")
        if short_OR_long != corr_string_1 and short_OR_long != corr_string_2:
            raise ValueError("Error: Incorrect String entered. Please enter 'short' or 'long'.")
        else:
            print("Correct!")
            break
    except ValueError as e:
        print(e)
    
    count += 1
    if count == 3:
        print("Too many attempts.")
        break

# Fortis stock price 
spot_price = 138.90

# Long call
K = 145 
premium_call = 3.50

# Stock price range at expiration of the put
sT = np.arange(0.7*spot_price, 1.3*spot_price, 1)

# LONG CALL PAYOFF
def call_payoff(sT, K, premium, short_OR_long):
    if short_OR_long == 'short':
        return np.where(sT > K, -(sT - K), 0) - premium
    else: 
        return np.where(sT > K, sT - K, 0) - premium

payoff_long_call = call_payoff(sT, K, premium_call, short_OR_long=short_OR_long)

# Plot
fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT, payoff_long_call, label=f'{short_OR_long.capitalize()} Call', color='r')

# --------- New bits ↓ ---------
y_min, y_max = payoff_long_call.min(), payoff_long_call.max()
pad = 0.1 * (y_max - y_min) or 1      # fallback so pad ≠ 0 when flat
ax.set_ylim(y_min - pad, y_max + pad) # long y-axis
ax.axhline(0, ls='--', lw=0.8, color='grey', alpha=0.6)  # zero-P&L line
# --------- New bits ↑ ---------

plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.title(f'{short_OR_long.capitalize()} Call Payoff')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.5)
plt.show()
