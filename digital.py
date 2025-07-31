
# ================================================================
#  DIGITAL (CASH-OR-NOTHING) OPTION — PRICING & GREEKS TOOLKIT #  “Same format” as the previous Up-and-Out module # ================================================================
import numpy as np
import pandas as pd
from scipy.stats import norm
 
# ----------------------------------------------------------------
# 1.  Closed-form price for a European DIGITAL option # ----------------------------------------------------------------
def digital_price(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    """
    Closed-form Black-Scholes price of a cash-or-nothing digital option.
 
    * option_type = "call"  → pays `cash_payoff` if  S_T > K
    * option_type = "put"   → pays `cash_payoff` if  S_T < K
    """
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be strictly positive")
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
 
    if option_type.lower() == "call":
        return cash_payoff * disc * norm.cdf(d2)
    elif option_type.lower() == "put":
        return cash_payoff * disc * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")


# ----------------------------------------------------------------
# 4.  MARK-TO-MARKET MATRIX  (spot-factor × tenor → price) # ----------------------------------------------------------------
def digital_mtm_matrix(
        S_0,
        price_factors=(0.90, 1.00, 1.10),
        tenors=(0.5, 1.0, 2.5),
        r=0.06,
        sigma=0.2,
        K=60,
        option_type="call",
        cash_payoff=1.0,
        xlsx_file="digital_mtm_matrix.xlsx"
    ):
    """
    Returns a DataFrame and saves it to Excel.
    Rows = spot factors (90%,100%,110%); columns = tenors.
    """
    df = pd.DataFrame(
        index=[f"{int(pf*100)}%" for pf in price_factors],
        columns=tenors,
        dtype=float
    )
 
    for T in tenors:
        for pf in price_factors:
            S = S_0 * pf
            price = digital_price(S, K, r, sigma, T, option_type, cash_payoff)
            df.loc[f"{int(pf*100)}%", T] = price
 
    df.to_excel(xlsx_file, float_format="%.6f")
    print(f"Digital option price matrix written to '{xlsx_file}':\n")
    print(df)
    return df
 
# ----------------------------------------------------------------
# 5.  Quick demo when run standalone
# ----------------------------------------------------------------
if __name__ == "__main__":
    S0     = 55
    r      = 0.06
    sigma  = 0.20
    K      = 60
    tenors = (0.5, 1.0, 2.5)
 
    # show a Greek bundle
    g = digital_greeks(S0, K, r, sigma, T=1.0, option_type="call")
    for k, v in g.items():
        print(f"{k.capitalize():<6}: {v:,.6f}")
 
    # create and save an MTM matrix
    digital_mtm_matrix(
        S_0=S0,
        price_factors=(0.90, 1.00, 1.10),
        tenors=tenors,
        r=r,
        sigma=sigma,
        K=K,
        option_type="call"
    )