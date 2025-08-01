# ----------------- A General file to test out all functions ------------------------------------------------
 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
 
#now imports from our files
from miscellaneous import simulate_gbm
from DownAndInPut import DownAndInPut, plot_hist_DownAndInPut, plot_DownAndInPut
from UpAndIn import UpAndInCall, plot_UpAndInCall
from UpAndOut import UpAndOut, UpAndOut_hist, UpAndOut_plot, UpAndOut_MC_plot
from Vanilla.vanilla_greeks import phi, gamma, vega, call_delta, call_rho, call_theta, put_delta, put_rho, put_theta, plot_all_greeks, plot_delta_, plot_gamma_, plot_greeks_, plot_rho_, plot_theta_, plot_vega_, plot_multiple_deltas
from Vanilla.blackscholesvanilla import black_scholes_call_value, black_scholes_put_value
from Vanilla.VanillaCall_Plotting import plot_call_payoff
from StrucProd import BullSpread_Price
 
# Parameters to be changed -------------------------------------------------------------------
 
S_0 = 32.21 #initial price S0
r = 3.97 # risk free rate
sigma = 0.5 # volatility
n_sims = 100_000 # no of simulations
BARRIER = 80  # Barrier level
 
T = 1 # time to maturity
N = 252 # no. of trading days
dt = T / N #dt (time steps so 1/252 time grid discrepancy)
discount_factor = np.exp(-r * T) # the discount factor used
 
S = 32.21
K = 32.21
r = 3.97
T = 1
 
maturities = [0.5,1,2]
 
# strikes
long_call_strike = 1.00  # ATM
short_call_strike = 1.20  # 20 % OTM
short_put_strike = 1.00  # ATM
long_put_strike = 0.98  # 2 % OTM
 
# vol
ATM_vol = 0.295
short_call_vol = 0.33
long_put_vol = 0.292
 
vol = 0.33
 
#  
 
# Helper functions - miscellaneous -------------------------------------------------------------------
 
gbm_sims = simulate_gbm(s_0=S_0, mu=r, sigma=sigma, dt=dt,n_sims=n_sims)
print(gbm_sims.shape)






# Vanilla --------------------------------------------------------------------------------------------
 
# Example parameters:
# S  = 32.21
# St = 38.143
# r = 3.97


# plotting vanilla greeks:
# plot_all_greeks()
 
# Other ------------------------------------------------------------------------------------------







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










# Exotic ---------------------------------------------------------------------------------------------
 
# Up and in Call
'''
UpAndInCall(gbm_sims=gbm_sims, K=K, BARRIER=BARRIER, discount_factor=discount_factor, observation=observation)
plot_UpAndInCall()
plot_hist_UpAndInCall()
plot_cum_KI()
'''
 
# Down and in Put
'''
# WORKS
DownAndInPut()
plot_MC_DownAndInPut(n_sims=n_sims, gbm_sims=gbm_sims, BARRIER=BARRIER, K=K)
plot_hist_DownAndInPut
plot_DownAndInPut()
'''