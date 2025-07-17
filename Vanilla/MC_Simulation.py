# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 16:05:01 2025
 
@author: PhilipBunford
"""
import random
import numpy as np
import pandas as pd
 
seed_value = 1234
 
random.seed(seed_value)
np.random.seed(seed_value)
 
# Let's create a MC simulation funct that we can re-use easily
# We want to simulate over time steps t_j = j * Delta * r for j=0,1,....,N
# we store these arrays in a shape (N_train, N + 1)
 
T = 1



def simulate_one_asset_path(N_train,
                            N,
                            dt,
                            sigma,
                            S_0):
   
    '''
    Simulate N_train trajectories for the asset over N time steps,
    given lognormal dynamics
   
    Params:
        N_train: no. of simulated trajectories
        N: no. of time steps
        dt =
   
   
    Returns:
        Numpy array 'paths' of shape (N_train, N+1)
    '''
   
    increments 4
 