import sys
sys.path.append('./')
import numpy as np
from CATA_pyfiles.data import DataAPI
from CATA_pyfiles.backtesting import Backtesting
import pandas as pd 

from ta.volume import VolumeWeightedAveragePrice

def vwap(dataframe, label='vwap', window=7, fillna=True):
        dataframe[label] = VolumeWeightedAveragePrice(high=dataframe['high'], low=dataframe['low'], close=dataframe["close"], volume=dataframe['volume'], window=window, fillna=fillna).volume_weighted_average_price()
        return dataframe

def _vwap_add_signal(df):

    '''
    
    stretegy:
        - if sma_10 trends up and cross sma_30 then buy
        - if sma_10 trends lower and cross sma_30 then sell if we have positions
        - no short sales
    '''
    df.loc[0, 'signal'] = ""
    
    for i in range(1, df.shape[0]-1):
        
        #// if indicator is Nan, no signal
        if pd.isnull(df.loc[i,'trend_indicator']) is True:
            df.loc[i, 'signal'] = 'none'
            
        #// if indicator turns from null to low, then none
        elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'Low':
            df.loc[i, 'signal'] = 'none'
            
        #// if indicator turns from null to high, then none
        elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'High':
            df.loc[i, 'signal'] = 'none'
            
        #// if indicator turns to high from low, means it's trending higher.
        elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'High':
            df.loc[i, 'signal'] = 'buy'
        
        #// if indicator keeps High, and we have positions then hold.
        elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'High' and (df.loc[i-1, 'signal'] == 'buy' or df.loc[i-1, 'signal'] == 'hold'):
            df.loc[i, 'signal'] = 'hold'
            
        #// if indicator keeps low, then none.
        elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'Low':
            df.loc[i, 'signal'] = 'none'
            
        #// if indicator turns to high from low, means it's trending higher.
        elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'Low' and df.loc[i - 1, 'signal'] == 'none':
            df.loc[i, 'signal'] = 'none'
            
        #// if indicator turns to low from high, means it's trending lower.
        elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'Low' and (df.loc[i - 1, 'signal'] == 'hold' or df.loc[i - 1, 'signal'] == 'buy') :
            df.loc[i,'signal'] = 'sell'                             
        
    return df


yahooapi = DataAPI(which_API="yahoo")
df = yahooapi.yahoo_pricing_data(sec_id="AAPL", start_date = "2019-01-01", end_date = "2021-01-01")

df = vwap(df, label='vwap_short', window = 7)
df = vwap(df, label='vwap_long', window = 30)

# Add colume trend_indicator, which will be used to populate buy_or_sell signal later
df.loc[df['vwap_short'] >= df['vwap_long'], 'trend_indicator'] = 'High'
df.loc[df['vwap_short'] < df['vwap_long'], 'trend_indicator'] = 'Low'

df = _vwap_add_signal(df)


print(df.head(100))