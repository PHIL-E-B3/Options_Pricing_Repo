import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
 
#coding simple black scholes vanilla pricing
 
# underlying stock price
S = 45.0
 
# again this can be replaced by our MC sims if we want.
 
K = 45.0
T = 164.0 / 365.0
r = 0.02
vol = 0.25
 
S_ = np.arange(35.0, K * 1.6, 0.01)
 
def N(z):
    """ Normal cumulative density function
    :param z: point at which cumulative density is calculated
    :return: cumulative density under normal curve
    """
    return norm.cdf(z)
 
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
    call_value = N(d1) * S - N(d2) * K * np.exp(-r * T)
 
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
    put_value = N(-d2) * K * np.exp(-r * T) - N(-d1) * S
 
    return put_value
 
'''
 
'''


if __name__ == "__main__":
    BullSpread_Price(
                S = 32.21,
                K = 32.21,  # you'll always input strike equal to 100% of spot price
                r = 3.97,
                T = 1,
                long_call_strike = 1,
                short_call_strike = 1.2,
                short_put_strike = 1 ,
                long_put_strike = 0.98,
                ATM_vol = 29.5,
                short_call_vol = 33,
                long_put_vol = 29.2
                )
 
    call_value = black_scholes_call_value(S=32.21, K=32.21, r=3.97, T=1, vol=29.5)
    put_value = black_scholes_put_value(S=32.21, K=32.21, r=3.97, T=1, vol=29.5)
 
    print(f"Call value is: {call_value:.2f}")
    print(f"Put valus is: {put_value:.2f}")
    plt.show()
 
