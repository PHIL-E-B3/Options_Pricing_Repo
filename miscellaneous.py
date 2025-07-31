import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# import bql # to import only when using this file within bloomberg. 0
'''bq = bql.Service()
 
##---------------------------------------------##
# Function for bloomie ticker price retrieval    ------------------------------------------------------------      
##---------------------------------------------##
 
def get_bloomieticker_price():
    '''''' Simple function that retrieves the desired ticker''''''
 
    ticker = input("What Bloomberg ticker do you want to retrieve: ")
 
    # Define the target universe of your BQL query: one or more entities
    universe = ticker
   
    # Define the target data (e.g., last price) you want for the universe
    data_item = bq.data.px_last()
 
    # Pass the two parts of your query as arguments for a Request object
    # And execute the request
    request = bql.Request(universe, data_item)
    response = bq.execute(request)
 
    # Parse the response as a DataFrame and print the output
 
    data = response[0].df()
    data_interest = data.iloc[0,2]
 
    return data_interest
 
'''
##---------------------------------------------##
# Function for Simulating gbm paths              ------------------------------------------------------------
##---------------------------------------------##



# Parameters
s_0 = 176.675          # Initial stock price
mu = 0.05      # Risk-free rate
sigma = 0.5        # Volatility
T = 1              # Time to maturity (1 year)
N = 252            # Number of trading days
dt = T / N         # Time step
n_sims = 10000     # Number of simulations
div_yield = 0.02   # Dividend yield
 
def simulate_gbm(s_0, mu, sigma, dt, n_sims, N, div_yield=0.0, random_seed=102):
    """
    Simulate stock returns using Geometric Brownian Motion with dividend yield.
 
    Parameters:
    - s_0: Initial stock price
    - mu: Risk-free rate
    - sigma: Volatility
    - dt: Time step
    - n_sims: Number of simulations
    - N: Number of time steps
    - div_yield: Dividend yield (default is 0.0)
    - random_seed: Seed for reproducibility (default is 102)
 
    Returns:
    - S_t: Simulated stock price paths (n_sims x (N + 1))
    """
    np.random.seed(random_seed)
 
    # Initialize the stock price array
    S_t = np.zeros((n_sims, N + 1))
    S_t[:, 0] = s_0  # Set the initial stock price
 
    # Generate random normal increments
    dW = np.random.normal(scale=np.sqrt(dt), size=(n_sims, N))
 
    # Adjust the drift term to account for the dividend yield
    drift = (mu - div_yield - 0.5 * sigma**2) * dt
 
    # Simulate the evolution of the process
    for t in range(1, N + 1):
        S_t[:, t] = S_t[:, t - 1] * np.exp(drift + sigma * dW[:, t - 1])
 
    return S_t


# Simulate GBM paths
 
# Plot a subset of paths
def plot_GBM(show=True):
    plt.figure(figsize=(10, 6))
    for i in range(30):  # Plot 30 random paths
        plt.plot(gbm_paths[i], alpha=0.5)
    plt.title('Simulated GBM Paths')
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    if show:
        plt.show()
 
if __name__ == "__main__":
    gbm_paths = simulate_gbm(s_0=s_0, mu=mu, sigma=sigma, dt=dt, n_sims=n_sims, N=N, div_yield=div_yield)
    plot_GBM(show=False)
    plt.show()