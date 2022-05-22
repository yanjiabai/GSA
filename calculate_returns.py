""" 
To calculate returns of financial instruments, defined in the same way as in 
the original data set.
One can check that this gives the same results as in the original data set by 
calculating the returns of Y and compare that to the 'returns' column in the
original data set.
"""
import pandas as pd
import warnings
from decimal import Decimal, getcontext

def get_dates(df, col_timestamp):
    """
    Input: dataframe, name of column containing timestamp data
    Output: None, but df has a new column containing dates
    """
    df['date'] = pd.to_datetime(df[col_timestamp], unit='ms').dt.date

def cal_returns(df, col_date, col_prices, precision=6, interval=60, trunc_high=0.875, trunc_low=-0.875):
    """
    To calculate returns given prices. The returns is defined to be the price ten
    minutes from now, minus the current price. It has been truncated to remove
    outliers. In the event that there is no price ten minutes from now (because 
    the market has closed, for example) then the latest price available is used.

    Input:
    df: dataframe
    col_date: name of column containing timestamps
    col_prices: name of column containing prices
    precision: precision of decimal representation, for floating point calculations
    interval: number of prices recorded in ten minutes, default=60
    trunc_high: upper bound for returns to truncate outliers, default=0.875
    trunc_low: lower bound for returns to truncate outliers, default=-0.875

    Output:
    returns: series containing returns data
    """
    # check the number of prices recorded per day
    if len(set(df.groupby([col_date]).size())) == 1:
        n_samples_per_day = df.groupby([col_date]).size()[0]
    else:
        raise ValueError('Different numbers of stock price samples per day!')
    
    getcontext().prec = precision # set floating point precision
    
    returns = [0.0]*df.shape[0]
    for i in range(df.shape[0]):
        day, loc = divmod(i, n_samples_per_day) 
        if loc < n_samples_per_day-interval-1: # not in last 10 minutes of a day
            # return = 10-minute-later price - current price
            returns[i] = Decimal(df[col_prices][i+interval]) - Decimal(df[col_prices][i]) 
        else: # in last 10 minutes of a day
            returns[i] = Decimal(df[col_prices][n_samples_per_day*(day+1)-1]) - Decimal(df[col_prices][i])
    returns = [float(i) for i in returns]
    # truncate outliers
    returns = [trunc_high if i > trunc_high else i for i in returns]
    returns = [trunc_low if i < trunc_low else i for i in returns]
    return returns

