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
import copy

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