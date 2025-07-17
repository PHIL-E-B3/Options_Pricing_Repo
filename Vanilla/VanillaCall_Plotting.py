import numpy as np
import matplotlib.pyplot as plt
import seaborn
 
##----------------------------------##
#   CALL PAYOFF AT EXPIRATION       # ------------------------------------------------------------
##----------------------------------##
 
# NB: the current price of the underlying security can be retrieved with bloomberg with:
# import get_bloomieticker_price from miscellaneous
 
# Also, if you want MC simulations instead of the np.linspace, you can:
# import simulate_gbm from gbm
 
import numpy as np
import matplotlib.pyplot as plt
 
def plot_call_payoff(spot_price, strike_price, premium, position_type=None):
    """
    Plots the payoff for a short or long call option.
 
    Parameters:
    - spot_price: Current price of the underlying asset.
    - strike_price: Strike price of the call option.
    - premium: Premium paid/received for the call option.
    - position_type: 'short' or 'long' to specify the position type. If None, prompts the user.
    """
 
    # Validate or prompt for position type
    if position_type not in ['short', 'long']:
        count = 0
        while True:
            try:
                position_type = input("Enter position type ('short' or 'long'): ").strip().lower()
                if position_type not in ['short', 'long']:
                    raise ValueError("Error: Incorrect input. Please enter 'short' or 'long'.")
                break
            except ValueError as e:
                print(e)
                count += 1
                if count == 3:
                    print("Too many invalid attempts. Exiting.")
                    return
 
    # Stock price range at expiration
    sT = np.arange(0, 1.6 * spot_price, 1)
 
    # Calculate payoff
    def call_payoff(sT, K, premium, position_type):
        if position_type == 'short':
            return np.where(sT > K, -(sT - K), 0) - premium
        else:
            return np.where(sT > K, sT - K, 0) - premium
 
    payoff = call_payoff(sT, strike_price, premium, position_type)
 
 
    fig, ax = plt.subplots()
    ax.spines['bottom'].set_position('zero')
    ax.plot(sT, payoff, label=f'{position_type.capitalize()} Call', color='r')
 
    # Adjust y-axis limits
    y_min, y_max = payoff.min(), payoff.max()
    pad = 0.1 * (y_max - y_min) or 1  # fallback so pad ≠ 0 when flat
    ax.set_ylim(y_min - pad, y_max + pad)  # long y-axis
    ax.axhline(0, ls='--', lw=0.8, color='grey', alpha=0.6)  # zero-P&L line
 
    # Labels and title
    plt.xlabel('Stock Price')
    ax.xaxis.set_label_coords(1.02, -0.04)
    plt.ylabel('Profit and Loss')
    plt.title(f'{position_type.capitalize()} Call Payoff')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.4)
    plt.show()
 
# Example usage
# plot_call_payoff(spot_price=138.90, strike_price=100, premium=10)