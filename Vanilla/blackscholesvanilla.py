import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
 
#coding simple black scholes vanilla pricing
 
S = 45.0
K = 45.0
T = 164.0 / 365.0
r = 0.02
vol = 0.25
S_ = np.arange(35.0, K * 1.6, 0.01)
 
def black_scholes_call_value(S, K, r, T, vol):
    """ Black-Scholes call option
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param T: time to expiration
    :param vol: volatility
    :return: BS call option value
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    d2 = d1 - (vol * np.sqrt(T))
    call_value = norm.cdf(d1) * S - norm.cdf(d2) * K * np.exp(-r * T)
 
    return call_value
 
def black_scholes_put_value(S, K, r, T, vol):
    """ Black-Scholes put option
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: BS put option value
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    d2 = d1 - (vol * np.sqrt(T))
    put_value = norm.cdf(-d2) * K * np.exp(-r * T) - norm.cdf(-d1) * S
 
    return put_value



if __name__ == "__main__":
    call_value = black_scholes_call_value(S=S,
                             K=K,
                             r=r,
                             T=T,
                             vol=vol)
    print(f"Black Scholes call value: {call_value}")
 
    put_value = black_scholes_put_value(S=S,
                             K=K,
                             r=r,
                             T=T,
                             vol=vol)
    print(f"Black Scholes put value: {put_value}")
 