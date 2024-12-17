import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import copy
from scipy.optimize import minimize
np.random.seed(16021997)
import yfinance as yf
import random
import operator
from deap import base, creator, tools, gp

plt.rcParams['font.family'] = 'Monospace'
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['grid.color'] = 'gray'  # Grid color
plt.rcParams['grid.linestyle'] = '--'  # Dashed lines
plt.rcParams['grid.linewidth'] = 0.3   # Line width

tickers = [
    "ENI.MI",   # Eni S.p.A.
    "ENEL.MI",  # Enel S.p.A.
    "ISP.MI",   # Intesa Sanpaolo S.p.A.
    "UCG.MI",   # UniCredit S.p.A.
    "PIRC.MI",  # Pirelli & C. S.p.A.
    "TIT.MI",   # Telecom Italia S.p.A.
    "LDO.MI",   # Leonardo S.p.A.
    "MB.MI",    # Mediobanca S.p.A.
    "G.MI",     # Assicurazioni Generali S.p.A.
    "SPM.MI",   # Saipem S.p.A.
    "MONC.MI",  # Moncler S.p.A.
    "CPR.MI",   # Campari Group
    "PRY.MI",   # Prysmian
    "TEN.MI",   # Tenaris
    "PST.MI",   # Poste Italiane
    "A2A.MI",   # A2A
    "TRN.MI"    # Terna
]

companies_colors = {
    'A2A':'#3396ff', 
    'CPR':'#d60b0b', 
    'ENEL':'#5bc47b', 
    'ENI':'#fae457', 
    'G':'#e13e0a', 
    'ISP':'#0f640e', 
    'LDO':'#031103', 
    'MB':'#2d3f7a', 
    'MONC':'#dfe2ea', 
    'PIRC':'#e9f70d',
    'PRY':'#2ec38d', 
    'PST':'#1d39c5', 
    'SPM':'#244c5b', 
    'TEN':'#6c6c6c', 
    'TIT':'#00378a', 
    'TRN':'#285cbc', 
    'UCG':'#e41b23'
}

def fitness_function(weights,
                     avg_returns,
                     cov_matrix,
                     risk_aversion):
    weights = np.asarray(weights).reshape((-1, 1)) # to ensure matrix multiplications work
    portfolio_return = np.dot(weights.T, avg_returns)
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    fitness = portfolio_return - (risk_aversion/2) * portfolio_variance
    return -fitness.item() # minimization for scipy

def markowitz_solution(num_stocks,
                        avg_returns,
                        cov_matrix,
                        risk_aversion,
                        short_selling=False):
    
    if not short_selling:
        constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

        # Bounds: each weight should be between 0 and 1 (no short-selling)
        bounds = [(0, 1) for _ in range(num_stocks)]

        # Initial guess (equal distribution)
        initial_weights = np.ones(num_stocks) / num_stocks

        # Optimization
        result = minimize(fitness_function, 
                        initial_weights, 
                        method='SLSQP', 
                        bounds=bounds, 
                        constraints=constraints,
                        args=(avg_returns, cov_matrix, risk_aversion),
                        options={'maxiter':100000000,'ftol': 1e-8})

        # Optimal weights and fitness value
        optimal_weights_markowitz = result.x
        optimal_fitness_markowitz = -result.fun  # Flip the sign back

    else:
        ones_vector = np.ones((num_stocks,1))
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        R = inv_cov_matrix - np.dot(inv_cov_matrix,np.dot(ones_vector,np.dot(ones_vector.T,inv_cov_matrix))) / np.dot(ones_vector.T,np.dot(inv_cov_matrix,ones_vector))
        optimal_weights_markowitz = np.array(np.dot(inv_cov_matrix,ones_vector) / np.dot(ones_vector.T,np.dot(inv_cov_matrix,ones_vector)) + np.dot(R,avg_returns)/risk_aversion)
        optimal_fitness_markowitz = fitness_function(optimal_weights_markowitz,
                                                     avg_returns,
                                                    cov_matrix,
                                                    risk_aversion)*-1

    return optimal_weights_markowitz, optimal_fitness_markowitz