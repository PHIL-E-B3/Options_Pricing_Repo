# helper function phi
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
 
K = 100       # Strike price
r = 0.05      # Risk-free rate
t = 1         # Time to expiration (in years)
vol = 0.2     # Volatility


def phi(x):
    """ Phi helper function
    """
    return np.exp(-0.5 * x * x) / (np.sqrt(2.0 * np.pi))
 
# shared
def gamma(S, K, r, t, vol):
    """ Black-Scholes gamma
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: gamma
    """
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    return phi(d1) / (S * vol * np.sqrt(t))
 
def vega(S, K, r, t, vol):
    """ Black-Scholes vega
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: vega
    """
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    return (S * phi(d1) * np.sqrt(t)) / 100.0
 
# call options
def call_delta(S, K, r, t, vol):
    """ Black-Scholes call delta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call delta
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    return N(d1)
 
def call_theta(S, K, r, t, vol):
    """ Black-Scholes call theta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call theta
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
 
    d2 = d1 - (vol * np.sqrt(t))
    theta = -((S * phi(d1) * vol) / (2.0 * np.sqrt(t))) - (r * K * np.exp(-r * t) * N(d2))
    return theta / 365.0
 
def call_rho(S, K, r, t, vol):
    """ Black-Scholes call rho
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call rho
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    d2 = d1 - (vol * np.sqrt(t))
    rho = K * t * np.exp(-r * t) * N(d2)
    return rho / 100.0


# put options
def put_delta(S, K, r, t, vol):
    """ Black-Scholes put delta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put delta
    """
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    return N(d1) - 1.0
 
def put_theta(S, K, r, t, vol):
    """ Black-Scholes put theta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put theta
    """
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    d2 = d1 - (vol * np.sqrt(t))
    theta = -((S * phi(d1) * vol) / (2.0 * np.sqrt(t))) + (
    r * K * np.exp(-r * t) * N(-d2)
    )
    return theta / 365.0
 
# Put rho -----------------------------------------
 
def put_rho(S, K, r, t, vol):
    """ Black-Scholes put rho
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put rho
    """
    d1 = (1.0 / (vol * np.sqrt(t))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * t)
    d2 = d1 - (vol * np.sqrt(t))
    rho = -K * t * np.exp(-r * t) * N(-d2)
    return rho / 100.0
 
# Plotting theta -----------------------------------
 
def plot_theta_():
    x = np.linspace(0.01, K * 1.6, 600)
   
    theta_values = []
    for number in x:
        thetas = call_theta(number, K, r, t, vol)
        theta_values.append(thetas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, theta_values, lw=2, label='Theta')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Theta")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Theta ')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
 
# Plotting gamma -----------------------------------
 
def plot_gamma_():
    x = np.linspace(0.01, K * 1.6, 600)
   
    gamma_values = []
    for number in x:
        gammas = gamma(number, K, r, t, vol)
        gamma_values.append(gammas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, gamma_values, lw=2, label='Gamma')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Gamma")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Gamma ')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
 
# Plotting rho -----------------------------------
 
def plot_rho_():
    x = np.linspace(0.01, K * 1.6, 600)
   
    rho_values = []
    for number in x:
        rhos = call_rho(number, K, r, t, vol)
        rho_values.append(rhos)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, rho_values, lw=2, label='Rho')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Rho")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Rho ')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
 
# Plotting vega -----------------------------------
 
def plot_vega_():
    x = np.linspace(0.01, K * 1.6, 600)
   
    vega_values = []
    for number in x:
        vegas = vega(number, K, r, t, vol)
        vega_values.append(vegas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, vega_values, lw=2, label='vega')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call vega")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('vega ')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
 
# Plotting delta -----------------------------------
 
def plot_delta_():
 
    x = np.linspace(0.01, K * 1.6, 600)
   
    delta_values = [call_delta(number, K, r, t, vol) for number in x]
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, delta_values, lw=2, label='delta')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call delta")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('delta ')
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(1)
 
# Plotting All Greeks -----------------------------------
 
def plot_greeks_():
    x = np.linspace(0.01, K * 1.6, 600)
   
    delta_values = [call_delta(number, K, r, t, vol) for number in x]
    theta_values = [call_theta(number, K, r, t, vol) for number in x]
    vega_values = [vega(number, K, r, t, vol) for number in x]
    rho_values = [call_rho(number, K, r, t, vol) for number in x]
    gamma_values = [gamma(number, K, r, t, vol) for number in x]
 
    fig, axs = plt.subplots(5, figsize=(10, 15))
    fig.suptitle('Greeks', fontsize=20)
    plt.suptitle('Greeks')
 
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9,
                        top=0.9, wspace=0.4, hspace=0.6)
   
    axs[0].plot(x, delta_values)
    axs[0].axvline(K, color='green', ls=':', label=f'Strike = {K}')
    axs[0].title.set_text('Delta')
 
    axs[1].plot(x, theta_values)
    axs[1].axvline(K, color='green', ls=':', label=f'Strike = {K}')
    axs[1].title.set_text('Theta')
 
    axs[2].plot(x, vega_values)
    axs[2].axvline(K, color='green', ls=':', label=f'Strike = {K}')
    axs[2].title.set_text('Vega')
 
    axs[3].plot(x, rho_values)
    axs[3].axvline(K, color='green', ls=':', label=f'Strike = {K}')
    axs[3].title.set_text('Rho')
 
    axs[4].plot(x, gamma_values)
    axs[4].axvline(K, color='green', ls=':', label=f'Strike = {K}')
    axs[4].title.set_text('Gamma')
   
    plt.show(block=False)
    plt.pause(1)



'''
gamma_yn = input('Do you want to plot gamma? (y/n)')
theta_yn = input('Do you want to plot theta? (y/n)')
rho_yn = input('Do you want to plot rho? (y/n)')
delta_yn = input('Do you want to plot delta? (y/n)')
vega_yn = input('Do you want to plot vega? (y/n)')
 
'''


count = 0
while True:
    corr_string_1 = 'y'
    corr_string_2 = 'n'
 
    try:
        gamma_yn = input('Do you want to plot greeks? (y/n)')
        if gamma_yn != corr_string_1 and gamma_yn != corr_string_2:
            raise ValueError("Error: Incorrect String entered. Please enter 'y' or 'n'.")
        else:
            plot_gamma_()
            plot_delta_()
            plot_vega_()
            plot_rho_()
            plot_theta_()
            plot_greeks_()
            break
    except ValueError as e:
        print(e)
 
 