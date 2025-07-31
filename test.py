import numpy as np
import matplotlib.pyplot as plt

# ------------------------- #
#  USER INPUT (robust)      #
# ------------------------- #
def ask(prompt, valid):
    """Simple validated input helper."""
    tries = 0
    while True:
        ans = input(prompt).strip().lower()
        if ans in valid:
            return ans
        print(f"❌  Please enter one of {valid}.")
        tries += 1
        if tries == 3:
            raise SystemExit("Too many invalid attempts.")

position   = ask("long or short?  → ", {"long", "short"})
opt_type   = ask("call or put?    → ", {"call", "put"})

# ------------------------- #
#  PARAMETERS               #
# ------------------------- #
spot   = 138.90           # underlying spot price
K      = 145              # strike
prem   = 3.50             # option premium (paid/received)
sT     = np.arange(0.7*spot, 1.3*spot + 1, 1)   # price grid at expiry

# ------------------------- #
#  PAYOFF FUNCTION          #
# ------------------------- #
def option_payoff(s, strike, premium, otype="call", pos="long"):
    """Generic European option payoff."""
    if otype == "call":
        intrinsic = np.maximum(s - strike, 0)
    else:                      # put
        intrinsic = np.maximum(strike - s, 0)
        
    pnl = intrinsic - premium          # long payoff
    if pos == "short":
        pnl = -pnl                     # flip sign for short
    
    return pnl

payoff = option_payoff(sT, K, prem, otype=opt_type, pos=position)

# ------------------------- #
#  PLOT                     #
# ------------------------- #
fig, ax = plt.subplots()

