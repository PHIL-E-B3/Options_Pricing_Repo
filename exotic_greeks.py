import numpy as np
from scipy.stats import norm
 
# Cumulative normal distribution function
N = norm.cdf
# Probability density function
n = norm.pdf
 
################################################################################
#                                VOMMA (VOLGA)                                 #
#   Vomma measures the sensitivity of Vega to changes in volatility.           #
################################################################################
 
def call_vomma(S, K, r, T, vol):
    """ Call Vomma (Volga) measures sensitivity to volatility """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return S * n(d1) * np.sqrt(T) * d1 * d2 / vol
 
def put_vomma(S, K, r, T, vol):
    """ Put Vomma (Volga) measures sensitivity to volatility """
    return call_vomma(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   VANNA                                      #
#   Vanna measures the sensitivity of Delta to changes in volatility.          #
################################################################################
 
def call_vanna(S, K, r, T, vol):
    """ Call Vanna measures sensitivity to changes in volatility and spot price """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return -n(d1) * d1 * T / vol
 
def put_vanna(S, K, r, T, vol):
    """ Put Vanna measures sensitivity to changes in volatility and spot price """
    return call_vanna(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   CHARM                                      #
#   Charm measures the rate of change of Delta with respect to time.           #
################################################################################
 
def call_charm(S, K, r, T, vol):
    """ Call Charm measures the rate of change of delta over time """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return -n(d1) * (2 * (r - d2 * vol * np.sqrt(T)) / (2 * T * vol * np.sqrt(T)))
 
def put_charm(S, K, r, T, vol):
    """ Put Charm measures the rate of change of delta over time """
    return call_charm(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   ZOMMA                                      #
#   Zomma measures the rate of change of Gamma with respect to spot price.     #
################################################################################
 
def call_zomma(S, K, r, T, vol):
    """ Call Zomma measures the rate of change of gamma with respect to spot price """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return n(d1) * (d1 * (d1 - vol * np.sqrt(T)) - 1) / (S * vol * np.sqrt(T))
 
def put_zomma(S, K, r, T, vol):
    """ Put Zomma measures the rate of change of gamma with respect to spot price """
    return call_zomma(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   COLOR                                      #
#   Color measures the rate of change of Gamma with respect to time.           #
################################################################################
 
def call_color(S, K, r, T, vol):
    """ Call Color measures the rate of change of gamma over time """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return -n(d1) * (d1 / (2 * T) + (r - d1 * vol * np.sqrt(T)) / (vol * T * np.sqrt(T)))
 
def put_color(S, K, r, T, vol):
    """ Put Color measures the rate of change of gamma over time """
    return call_color(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   SPEED                                      #
#   Speed measures the rate of change of Gamma with respect to spot price.     #
################################################################################
 
def call_speed(S, K, r, T, vol):
    """ Call Speed measures the rate of change of gamma with respect to spot price """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    return -n(d1) * (d1 / (S ** 2 * vol * np.sqrt(T)))
 
def put_speed(S, K, r, T, vol):
    """ Put Speed measures the rate of change of gamma with respect to spot price """
    return call_speed(S, K, r, T, vol)  # Same formula for calls and puts
 
################################################################################
#                                   ULTIMA                                     #
#   Ultima measures the sensitivity of Vomma to changes in volatility.         #
################################################################################


def call_ultima(S, K, r, T, vol):
    """ Call Ultima measures the sensitivity of Vomma to changes in volatility """
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return -S * n(d1) * np.sqrt(T) * (d1 * d2 * (1 - d1 * d2) - d1 ** 2 - d2 ** 2) / (vol ** 2)
 
def put_ultima(S, K, r, T, vol):
    """ Put Ultima measures the sensitivity of Vomma to changes in volatility """
    return call_ultima(S, K, r, T, vol)  # Same formula for calls and puts




### Now for plotting ---------------------------------------------------------------------------------------------------------------
 
# Plotting Vomma -------------------------------------------------------------------------------------------- plot vomma
 
def plot_vomma_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    vomma_values = []
    for number in x:
        vomma_val = vomma(number, K, r, T, vol)
        vomma_values.append(vomma_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, vomma_values, lw=2, label='Vomma')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Vomma")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Vomma')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Vanna -------------------------------------------------------------------------------------------- plot vanna
 
def plot_vanna_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    vanna_values = []
    for number in x:
        vanna_val = vanna(number, K, r, T, vol)
        vanna_values.append(vanna_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, vanna_values, lw=2, label='Vanna')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Vanna")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Vanna')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Charm -------------------------------------------------------------------------------------------- plot charm
 
def plot_charm_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    charm_values = []
    for number in x:
        charm_val = charm(number, K, r, T, vol)
        charm_values.append(charm_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, charm_values, lw=2, label='Charm')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Charm")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Charm')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Zomma -------------------------------------------------------------------------------------------- plot zomma
 
def plot_zomma_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    zomma_values = []
    for number in x:
        zomma_val = zomma(number, K, r, T, vol)
        zomma_values.append(zomma_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, zomma_values, lw=2, label='Zomma')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Zomma")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Zomma')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Color -------------------------------------------------------------------------------------------- plot color
 
def plot_color_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    color_values = []
    for number in x:
        color_val = color(number, K, r, T, vol)
        color_values.append(color_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, color_values, lw=2, label='Color')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Color")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Color')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Speed -------------------------------------------------------------------------------------------- plot speed
 
def plot_speed_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    speed_values = []
    for number in x:
        speed_val = speed(number, K, r, T, vol)
        speed_values.append(speed_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, speed_values, lw=2, label='Speed')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Speed")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Speed')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()
 
# Plotting Ultima ------------------------------------------------------------------------------------------- plot ultima
 
def plot_ultima_(show=True):
    x = np.linspace(0.01, K * 1.6, 600)
   
    ultima_values = []
    for number in x:
        ultima_val = ultima(number, K, r, T, vol)
        ultima_values.append(ultima_val)
 
    plt.figure(figsize=(7, 4))
    plt.plot(x, ultima_values, lw=2, label='Ultima')
    plt.axvline(K, color='green', ls=':', label=f'Strike = {K}')
    plt.title(f"Vanilla Call Ultima")
    plt.xlabel(r'Final underlying price $S_T$')
    plt.ylabel('Ultima')
    plt.legend()
    plt.tight_layout()
    if show:
        plt.show()