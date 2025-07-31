# helper function phi
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
 


# Init parameters  -------------------------------------------------------------------------------------------------- init params
 
K = 100       # Strike price
r = 0.05      # Risk-free rate
T = 1         # Time to expiration (in years)
vol = 0.2     # Volatility
 
# phi -------------------------------------------------------------------------------------------------- phi
 
def phi(x):
    """ Phi helper function
    """
    return np.exp(-0.5 * x * x) / (np.sqrt(2.0 * np.pi))
 
# gamma --------------------------------------------------------------------------------------------------gamma
 
# +------------------------------------------------------+
# |                                                      |
# | SHARED GREEKS (Vega and Gamma same for calls + Puts)                    
# |                                                      |
# +------------------------------------------------------+
 
# shared gamma
 
def gamma(S, K, r, T, vol):
    """ Black-Scholes gamma
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: gamma
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    return phi(d1) / (S * vol * np.sqrt(T))
 
# vega ----------------------------------------------------------------------------------------------------vega
 
def vega(S, K, r, T, vol):
    """ Black-Scholes vega
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: vega
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    return (S * phi(d1) * np.sqrt(T)) / 100.0
 
# +--------------------------------------------------+
# |                                                  |
# |                  CALL GREEKS                    
# |                                                  |
# +--------------------------------------------------+


# call greeks ----------------------------------------------------------------------------------------call greeks
 
def call_delta(S, K, r, T, vol):
    """ Black-Scholes call delta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call delta
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    return N(d1)
 
# call theta -------------------------------------------------------------------------------------------call theta
 
def call_theta(S, K, r, Theta, vol):
    """ Black-Scholes call theta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call theta
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
 
    d2 = d1 - (vol * np.sqrt(T))
    theta = -((S * phi(d1) * vol) / (2.0 * np.sqrt(T))) - (r * K * np.exp(-r * T) * N(d2))
    return theta / 365.0
 
# call rho ------------------------------------------------------------------------------------------call rho
 
def call_rho(S, K, r, T, vol):
    """ Black-Scholes call rho
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: call rho
    """
    N = norm.cdf
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    d2 = d1 - (vol * np.sqrt(T))
    rho = K * T * np.exp(-r * T) * N(d2)
    return rho / 100.0
 
# +--------------------------------------------------+
# |                                                  |
# |                  PUT GREEKS                    
# |                                                  |
# +--------------------------------------------------+


# put greeks  -------------------------------------------------------------------------------------- PUT greeks
 
def put_delta(S, K, r, T, vol):
    """ Black-Scholes put delta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put delta
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    return norm.cdf(d1) - 1.0
 
# put theta -------------------------------------------------------------------------------------------  put theta
 
def put_theta(S, K, r, t, vol):
    """ Black-Scholes put theta
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put theta
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    d2 = d1 - (vol * np.sqrt(T))
    theta = -((S * phi(d1) * vol) / (2.0 * np.sqrt(T))) + (r * K * np.exp(-r * T) * N(-d2))
    return theta / 365.0
 
# Put rho ----------------------------------------------------------------------------------------------   PUT rho
 
def put_rho(S, K, r, T, vol):
    """ Black-Scholes put rho
    :param S: underlying
    :param K: strike price
    :param r: rate
    :param t: time to expiration
    :param vol: volatility
    :return: put rho
    """
    d1 = (1.0 / (vol * np.sqrt(T))) * (np.log(S / K) + (r + 0.5 * vol ** 2.0) * T)
    d2 = d1 - (vol * np.sqrt(T))
    rho = -K * T * np.exp(-r * T) * N(-d2)
    return rho / 100.0
 
# +--------------------------------------------------+
# |                                                  |
# |                PLOTTING GREEKS                    
# |                                                  |
# +--------------------------------------------------+



# Plotting theta -------------------------------------------------------------------------------------------plot theta
 
def plot_call_theta_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    theta_values = []
    for number in x:
        thetas = call_theta(number, K, r, T, vol)
        theta_values.append(thetas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, theta_values, lw=2, label='Theta')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Theta")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Theta ')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting gamma ------------------------------------------------------------------------------------------- plot gamma
 
def plot_gamma_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    gamma_values = []
    for number in x:
        gammas = gamma(number, K, r, T, vol)
        gamma_values.append(gammas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, gamma_values, lw=2, label='Gamma')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Gamma")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Gamma ')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
 
# Plotting rho ----------------------------------------------------------------------------------------------- plot rho
 
def plot_call_rho_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    rho_values = []
    for number in x:
        rhos = call_rho(number, K, r, T, vol)
        rho_values.append(rhos)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, rho_values, lw=2, label='Rho')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call Rho")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Rho ')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting vega ------------------------------------------------------------------------------------------------- plot vega
 
def plot_vega_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    vega_values = []
    for number in x:
        vegas = vega(number, K, r, T, vol)
        vega_values.append(vegas)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, vega_values, lw=2, label='vega')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call vega")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('vega ')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting delta ------------------------------------------------------------------------------------------------- plot delta
 
def plot_call_delta_(show=True):
 
    x = np.linspace(0.01, K * 1.6, 600)
   
    delta_values = [call_delta(number, K, r, T, vol) for number in x]
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, delta_values, lw=2, label='delta')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f" Vanilla Call delta")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('delta ')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()


# Plotting All Greeks -------------------------------------------------------------------------------------------- plot all greeks
 
def plot_call_greeks_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    delta_values = [call_delta(number, K, r, T, vol) for number in x]
    theta_values = [call_theta(number, K, r, T, vol) for number in x]
    vega_values = [vega(number, K, r, T, vol) for number in x]
    rho_values = [call_rho(number, K, r, T, vol) for number in x]
    gamma_values = [gamma(number, K, r, T, vol) for number in x]
 
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
 
    if show:
        plt.show()
 
# plot multiple delta values for different mat. ---------------------------------------------------------
def plot_multiple_deltas(K, r, vol, *maturities, show=True):
    """
    Plots delta for different maturities on the same graph.
 
    Parameters:
    - K: Strike price
    - r: Risk-free rate
    - vol: Volatility
    - *maturities: Any number of maturities (T)
    """
    x = np.linspace(0.01, K * 1.6, 600)
   
    plt.figure(figsize=(7, 4))
   
    for T in maturities:
        delta_values = [call_delta(number, K, r, T, vol) for number in x]
        plt.plot(x, delta_values, lw=2, label=f'Delta (T={T})')
   
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title("Vanilla Call Delta for Different Maturities")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Delta')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Correct function call
# plot_multiple_deltas(100, 0.05, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 2)



def plot_all_greeks():
    """Plots all Greeks on separate figures and displays them together."""
    plot_call_theta_(show=False)
    plot_gamma_(show=False)
    plot_call_rho_(show=False)
    plot_vega_(show=False)
    plot_call_delta_(show=False)
    plot_call_greeks_(show=False)
    plt.show()  # Display all plots together
   
if __name__ == "__main__":
    plot_all_greeks()