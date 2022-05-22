"""
Tests for stationarity
"""
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen

def test_adf(timeseries):
    """
    To do the Augmented Dickey Fuller Test (ADF Test) and output p-value
    Input: timeseries data
    Output: p-value (float)
    """
    adft = adfuller(timeseries,autolag='AIC')
    # output for dft will give us without defining what the values are.
    #hence we manually write what values does it explains using a for loop
    output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','Number of observations used'])
    return output['p-value']

def cointegration_test(df): 
    """
    To do the Johansen cointegration test of the cointegration rank
    Input: dataframe
    Output: Boolean, True if significant results in all columns
    """
    res = coint_johansen(df,-1,5)
    d = {'0.90':0, '0.95':1, '0.99':2}
    traces = res.lr1
    cvts = res.cvt[:, d[str(1-0.05)]]
    def adjust(val, length= 6): 
        return str(val).ljust(length)
    result = True
    for trace, cvt in zip(traces, cvts):
        result = result and (trace > cvt)
    return result