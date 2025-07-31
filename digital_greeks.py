
# ----------------------------------------------------------------
#  Analytic Greeks
# ----------------------------------------------------------------
def _phi(x):       # standard normal PDF
    return np.exp(-0.5 * x * x) / np.sqrt(2 * np.pi)
 
def digital_delta(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
    factor = cash_payoff * disc * _phi(d2) / (S * sigma * np.sqrt(T))
    return  factor if option_type.lower() == "call" else -factor
 
def digital_gamma(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
    term = (-d2 / (S * S * sigma * np.sqrt(T))) - 1/(S * S * sigma * np.sqrt(T))
    factor = cash_payoff * disc * _phi(d2) * term
    return factor if option_type.lower() == "call" else -factor
 
def digital_vega(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
    term = -d2 / sigma
    factor = cash_payoff * disc * _phi(d2) * term
    return factor if option_type.lower() == "call" else -factor
 
def digital_theta(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
    pdf   = _phi(d2)
    part1 = -cash_payoff * r * disc * (norm.cdf(d2) if option_type=="call" else norm.cdf(-d2))
    part2 = cash_payoff * disc * pdf * ( (r - 0.5*sigma**2)/(2*sigma*np.sqrt(T)) )
    if option_type.lower() == "call":
        return part1 + part2
    else:
        return -(part1 + part2)   # sign flips for put
 
def digital_rho(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    disc = np.exp(-r * T)
    payoff_prob = norm.cdf(d2) if option_type.lower()=="call" else norm.cdf(-d2)
    return -T * cash_payoff * disc * payoff_prob
 
# ----------------------------------------------------------------
# 3.  Convenience wrapper: everything in one dict # ----------------------------------------------------------------
def digital_greeks(S, K, r, sigma, T, option_type="call", cash_payoff=1.0):
    return {
        "price": digital_price(S, K, r, sigma, T, option_type, cash_payoff),
        "delta": digital_delta(S, K, r, sigma, T, option_type, cash_payoff),
        "gamma": digital_gamma(S, K, r, sigma, T, option_type, cash_payoff),
        "vega" : digital_vega (S, K, r, sigma, T, option_type, cash_payoff),
        "theta": digital_theta(S, K, r, sigma, T, option_type, cash_payoff),
        "rho"  : digital_rho  (S, K, r, sigma, T, option_type, cash_payoff)
    }