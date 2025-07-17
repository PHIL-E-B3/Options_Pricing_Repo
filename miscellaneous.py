import pandas as pd
import numpy as np
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
 
T = 1 # 1year
N = 252 #no of trad. days
dt = T / N
 
def simulate_gbm(s_0, mu, sigma, dt, n_sims, random_seed=102):
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
 
if __name__ == "__main__":
    simulate_gbm(s_0, mu, sigma, dt, n_sims, random_seed=102)