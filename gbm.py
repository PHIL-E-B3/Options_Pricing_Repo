import numpy as np
 
T = 1 # 1year
N = 252 #no of trad. days
dt = T / N
 
def simulate_gbm(s_0, mu, sigma, dt, n_sims, random_seed=1):
    """Simulate stock returns using Geometric Brownian Motion."""
   
    np.random.seed(random_seed)
 
    # scale is the standard deviation of the distribution (from which you take the draws)
    # size is the output shape: n_sim rows and N columns
        # n_sim rows (1000) by N columns (252)
    # in discrete time, increments dt are scaled by the square root of time step to maintain the properties of the continuous process
    dW = np.random.normal(scale=np.sqrt(dt), size=(n_sims, N + 1))
 
    # simulate the evolution of the process
    S_t = s_0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * dW, axis=1))
    S_t[:, 0] = s_0 #corrects the first column value and places the first price inside of it
 
    return S_t