from CATA_pyfiles.data import DataAPI
import pandas as pd 
import numpy as np
from ta.volume import VolumeWeightedAveragePrice

class Backtesting:

    def __init__(self, df: pd.DataFrame = None) -> None:
        self.df = df

    def SMA_single_parameter(self, sma_short = 7, sma_long = 30, notification = True) -> pd.DataFrame:

        """[summary] Back Testing simple moving average strategy.

        Args:
            sma_short (int, optional): sma short duration. Defaults to 10.
            sma_long (int, optional): sma long duration. Defaults to 30.

        Returns:
            [type]: [description]
        """ 

        # Create a copy of original data        
        df = self.df.copy()

        # Add sma_short and sma_long columns
        df['sma_short'] = df.loc[:,'close'].rolling(window=sma_short).mean()
        df['sma_long'] = df.loc[:,'close'].rolling(window=sma_long).mean()

        # Add colume trend_indicator, which will be used to populate buy_or_sell signal later
        df.loc[df['sma_short'] >= df['sma_long'], 'trend_indicator'] = 'High'
        df.loc[df['sma_short'] < df['sma_long'], 'trend_indicator'] = 'Low'
        
        # add signal column to dataset
        df = self._sma_add_signal(df)

        # add investment to dataset. value fluctuate based on signal and daily price changes
        df = self.backtesting(df, initial_investment = 1000000)

        if notification:
            print("Back-testing result:\n\tsma_short:{}, sma_long:{}".format(sma_short, sma_long))
            print("Strategy gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Profit']))
            print("Stock gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Pct_change']))

        return df


    def SMA_bulk_parameters(self, sma_short = [5, 10, 15], sma_long = [30, 50, 100]):
        
        pd_result = pd.DataFrame(columns = ['Back-testing Index', 'sma_short', 'sma_long', 'stock_gain', 'strategy_gain', 'diff'])
        count = 1
        for i in sma_short:
            for j in sma_long:
                df = self.SMA_single_parameter(i, j)
                pd_result = pd_result.append({
                    'Back-testing Index': count, 
                    'sma_short': i, 
                    'sma_long': j, 
                    'stock_gain':df.loc[df.shape[0]-1, 'Pct_change'], 
                    'strategy_gain': df.loc[df.shape[0]-1, 'Profit'], 
                    'diff': df.loc[df.shape[0]-1, 'Profit'] - df.loc[df.shape[0]-1, 'Pct_change']
                }
                , ignore_index = True
                )
                count += 1
        
        return pd_result
    



    def _sma_add_signal(self, df):

        '''
        
        stretegy:
            - if sma_10 trends up and cross sma_30 then buy
            - if sma_10 trends lower and cross sma_30 then sell if we have positions
            - no short sales
        '''
        
        for i in range(1, df.shape[0]):
            
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



    def RSI_single_parameter(self, period: int = 14, notification = True) -> pd.DataFrame:
        """[summary] RSI Strategy BackTesting

        Args:
            period (int, optional): [description]. Defaults to 20.

        Returns:
            pd.DataFrame: [description]
        """        

        df = self.df.copy()

        # add a column to calculate price change from previous day
        df['change_in_price'] = df['close'].transform(
            lambda x: x.diff()
        )

        # Define the up days.
        df['up_day'] = df['change_in_price'].apply(
            lambda x : np.where(x >= 0, x, 0)
        )

        # Define the down days.
        df['down_day'] = df['change_in_price'].apply(
            lambda x : np.where(x < 0, abs(x), 0)
        )

        # Calculate the EWMA for the Up days.
        df['ewma_up'] = df.loc[:,'up_day'].rolling(window=period).mean()

        # Calculate the EWMA for the Down days.
        df['ewma_down'] = df.loc[:,'down_day'].rolling(window=period).mean()


        # Calculate the Relative Strength
        df['relative_strength']= df['ewma_up'] / df['ewma_down']

        # Calculate the Relative Strength Index
        df['RSI'] = 100.0 - (100.0 / (1.0 + df['relative_strength']))

        # Clean up before sending back.
        df.drop(
            labels=['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_price'],
            axis=1,
            inplace=True
        )

        # Add colume trend_indicator
        #           if RSI > 70, then trend_indicator = sell
        #           if RSI < 30, then trend_indicator = buy

        conditions = [
            (df['RSI'] >= 70),
            (df['RSI'] <70) & (df['RSI'] >=30),
            (df['RSI'] < 30)
        ]

        values = ['sell', 'none', 'buy']

        df['trend_indicator'] = np.select(conditions, values)

        df = self._rsi_add_signal(df)
        df = self.backtesting(df)
        if notification:
            print("Back-testing result:\nperiod:{}".format(period))
            print("Strategy gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Profit']))
            print("Stock gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Pct_change']))
        
        return df



    def _rsi_add_signal(self, df):

        '''
        
        stretegy:
            - if sma_10 trends up and cross sma_30 then buy
            - if sma_10 trends lower and cross sma_30 then sell if we have positions
            - no short sales
        '''
        
        for i in range(1, df.shape[0]):
            
            #// if indicator is Nan, no signal
            if pd.isnull(df.loc[i,'trend_indicator']) is True:
                df.loc[i, 'signal'] = 'none'
                
            #// if indicator turns from null to buy, then buy
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'buy':
                df.loc[i, 'signal'] = 'none'
                
            #// if indicator turns from null to sell, then none
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'sell':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from null to none, then none
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from buy to buy, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'buy' and df.loc[i, 'trend_indicator'] == 'buy'and df.loc[i - 1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from buy to buy, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'buy' and df.loc[i, 'trend_indicator'] == 'buy'and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from buy to none, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'buy' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'buy'
            
            #// if indicator turns from buy to none, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'buy' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from sell to none, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'sell' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'
            #// if indicator turns from none to buy and previous signal is hold, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'sell' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'sell'

            #// if indicator turns from sell to sell, then see=ll.
            elif df.loc[i-1, 'trend_indicator'] == 'sell' and df.loc[i, 'trend_indicator'] == 'sell' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from sell to sell, then see=ll.
            elif df.loc[i-1, 'trend_indicator'] == 'sell' and df.loc[i, 'trend_indicator'] == 'sell' and df.loc[i - 1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'


            #// if indicator turns from none to buy and previous signal is hold, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'sell' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from none to buy and previous signal is none, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'buy' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'
            #// if indicator turns from none to buy and previous signal is none, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'buy' and df.loc[i - 1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'buy' and df.loc[i - 1, 'signal'] == 'buy':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from none to hold, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'buy':
                df.loc[i, 'signal'] = 'hold'
            
            #// if indicator turns from none to hold, then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'none' and df.loc[i, 'trend_indicator'] == 'none' and df.loc[i - 1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'


            else:
                df.loc[i, 'signal'] = 'none'
        return df





    def backtesting(self, df, initial_investment = 1000000):
        
            df.loc[0, 'Total_Value'] = initial_investment
            df.loc[0, 'Share_Value'] = 0
            df.loc[0, 'Cash_Value'] = initial_investment
            df.loc[0, 'Shares'] = 0
            
            for i in range(1, df.shape[0]):
            
                #// if indicator is Nan, no signal
                if pd.isnull(df.loc[i,'signal']):
                    
                    df.loc[i, 'Total_Value'] = initial_investment
                    df.loc[i, 'Share_Value'] = 0
                    df.loc[i, 'Cash_Value'] = initial_investment
                    df.loc[i, 'Shares'] = 0

                elif df.loc[i,'signal'] == 'none':
                    
                    df.loc[i, 'Shares'] = 0
                    df.loc[i, 'Share_Value'] = 0
                    df.loc[i, 'Cash_Value'] = df.loc[i - 1, 'Cash_Value'] 
                    df.loc[i, 'Total_Value'] = df.loc[i, 'Share_Value'] + df.loc[i, 'Cash_Value'] 
                    
                elif df.loc[i,'signal'] == 'buy':
                    
                    df.loc[i, 'Shares'] = df.loc[i - 1, 'Total_Value']//df.loc[i, 'close'] 
                    df.loc[i, 'Share_Value'] = df.loc[i, 'Shares'] * df.loc[i, 'close']
                    df.loc[i, 'Cash_Value'] = df.loc[i-1, 'Total_Value']% df.loc[i, 'close']
                    df.loc[i, 'Total_Value'] = df.loc[i, 'Share_Value'] + df.loc[i, 'Cash_Value']   

                elif df.loc[i,'signal'] == 'hold':
                    
                    df.loc[i, 'Shares'] = df.loc[i-1, 'Shares']
                    df.loc[i, 'Share_Value'] = df.loc[i, 'Shares'] * df.loc[i, 'close']
                    df.loc[i, 'Cash_Value'] = df.loc[i-1, 'Cash_Value']
                    df.loc[i, 'Total_Value'] = df.loc[i, 'Share_Value'] + df.loc[i, 'Cash_Value'] 
                    
                elif df.loc[i,'signal'] == 'sell':
                    
                    df.loc[i, 'Shares'] = 0
                    df.loc[i, 'Share_Value'] = 0
                    df.loc[i, 'Cash_Value'] = df.loc[i-1, 'Cash_Value'] + df.loc[i-1, 'Shares'] * df.loc[i, 'close']
                    df.loc[i, 'Total_Value'] = df.loc[i, 'Share_Value'] + df.loc[i, 'Cash_Value'] 
                    
            df['Profit'] = df['Total_Value'].apply(lambda x: x / initial_investment)
            df['Pct_change'] = df['close'].apply(lambda x: x / df.loc[0, 'close'])

            return df


    def Bollinger_single_parameter(self, sma_period = 30, std_period = 20, notification = True) -> pd.DataFrame:

        """[summary] Back Testing Bollinger Bands strategy. 

        Args:
            sma_period (int, optional): sma duration. Defaults to 30.
            std_period (int, optional): duration to calculate standard deviation. Defaults to 20.

        Returns:
            [type]: [description]
        """ 

        # Create a copy of original data        
        df = self.df.copy()

        # Add sma_short and sma_long columns
        df['sma'] = df.loc[:,'close'].rolling(window=sma_period).mean()
        df['std'] = df.loc[:,'close'].rolling(window=std_period).std()

        # Upper Bollinger Bands = Mean+2*SD
        # Lower Bollinger Bands = Mean-2*SD
        df['Upper'] = df['sma'] + 2*df['std']
        df['Lower'] = df['sma'] - 2*df['std']

        # Add colume trend_indicator, which will be used to populate buy_or_sell signal later
        df.loc[df['close'] >= df['Upper'], 'trend_indicator'] = 'High'
        df.loc[df['close'] < df['Lower'], 'trend_indicator'] = 'Low'
        df.loc[(df['close'] < df['Upper']) & (df['close'] >= df['Lower']), 'trend_indicator'] = 'Middle'

        # add signal column to dataset
        df = self._bollinger_add_signal(df)

        # add investment to dataset. value fluctuate based on signal and daily price changes
        df = self.backtesting(df)

        if notification:
            print("Back-testing result:\n\tsma_period:{}, std_period:{}".format(sma_period, std_period))
            print("Strategy gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Profit']))
            print("Stock gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Pct_change']))

        return df


    def _bollinger_add_signal(self, df):

        ''' 
        stretegy:
            - if price trends up and cross Bollinger lower band, then buy
            - if price trends down and cross Bollinger uper band, then sell
            - no short sales
        '''
        
        for i in range(1, df.shape[0]):
            
            #// if indicator is Nan, no signal
            if pd.isnull(df.loc[i,'trend_indicator']) is True:
                df.loc[i, 'signal'] = 'none'
                
            #// if indicator turns from null to High, then none
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'High':
                df.loc[i, 'signal'] = 'buy'
                
            #// if indicator turns from null to Low, then none
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'Low':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from null to Middle, then none
            elif pd.isnull(df.loc[i-1, 'trend_indicator']) and df.loc[i, 'trend_indicator'] == 'Middle':
                df.loc[i, 'signal'] = 'none'


            #// if indicator turns from Low to Low, then none signal.
            elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'Low' and df.loc[i-1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from Low to Low, then none signal.
            elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'Low' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from Low to Middle and no holdings, then buy.
            elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'Middle' and df.loc[i-1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'buy'

            #// if indicator turns from Low to Middle and no holdings, then buy.
            elif df.loc[i-1, 'trend_indicator'] == 'Low' and df.loc[i, 'trend_indicator'] == 'Middle' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'


            #// if indicator turns from Middle to Middle, and no holdings, then none signal.
            elif df.loc[i-1, 'trend_indicator'] == 'Middle' and df.loc[i, 'trend_indicator'] == 'Middle' and df.loc[i-1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from Middle to Middle, and with holdings then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'Middle' and df.loc[i, 'trend_indicator'] == 'Middle' and (df.loc[i-1, 'signal'] == 'buy' or df.loc[i-1, 'signal'] == 'hold'):
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from Middle to Low, and with holdings then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'Middle' and df.loc[i, 'trend_indicator'] == 'Low' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            #// if indicator turns from Middle to High, and no holdings, then none signal.
            elif df.loc[i-1, 'trend_indicator'] == 'Middle' and df.loc[i, 'trend_indicator'] == 'High' and df.loc[i-1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from Middle to High, and with holdings then hold.
            elif df.loc[i-1, 'trend_indicator'] == 'Middle' and df.loc[i, 'trend_indicator'] == 'High' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'


            #// if indicator turns from High to Middle, and no holdings, then none signal.
            elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'Middle' and df.loc[i-1, 'signal'] == 'none':
                df.loc[i, 'signal'] = 'none'

            #// if indicator turns from High to Middle, and with holdings then sell.
            elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'Middle' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'sell'

            #// if indicator turns from High to Middle, and with holdings then sell.
            elif df.loc[i-1, 'trend_indicator'] == 'High' and df.loc[i, 'trend_indicator'] == 'High' and df.loc[i-1, 'signal'] == 'hold':
                df.loc[i, 'signal'] = 'hold'

            else:
                df.loc[i, 'signal'] = 'none'
        return df

    def VWAP_single_parameter(self, sma_short = 7, sma_long = 30, notification = True) -> pd.DataFrame:

        """[summary] Back Testing Volume weighted moving average strategy.

        Args:
            sma_short (int, optional): sma short duration. Defaults to 10.
            sma_long (int, optional): sma long duration. Defaults to 30.

        Returns:
            [type]: DataFrame
        """ 
        

        # Create a copy of original data        
        df = self.df.copy()

        # Add vwap_short and vwap_long columns
        df = vwap(df, label='vwap_short', window = sma_short)
        df = vwap(df, label='vwap_long', window = sma_long)

        # Add colume trend_indicator, which will be used to populate buy_or_sell signal later
        df.loc[df['vwap_short'] >= df['vwap_long'], 'trend_indicator'] = 'High'
        df.loc[df['vwap_short'] < df['vwap_long'], 'trend_indicator'] = 'Low'
        
        # add signal column to dataset
        df = self._vwap_add_signal(df)

        # add investment to dataset. value fluctuate based on signal and daily price changes
        df = self.backtesting(df, initial_investment = 1000000)

        if notification:
            print("Back-testing result:\n\tvwap_short:{}, vwap_long:{}".format(sma_short, sma_long))
            print("Strategy gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Profit']))
            print("Stock gain in this back-test is {:.2f}".format(df.loc[df.shape[0]-1, 'Pct_change']))

        print(df.tail(5))
        return df


    def _vwap_add_signal(self, df):

        '''
        
        stretegy:
            - if sma_10 trends up and cross sma_30 then buy
            - if sma_10 trends lower and cross sma_30 then sell if we have positions
            - no short sales
        '''
        df.loc[0, 'signal'] = ""

        for i in range(1, df.shape[0]):
            
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



def vwap(dataframe, label='vwap', window=7, fillna=True):
        dataframe[label] = VolumeWeightedAveragePrice(high=dataframe['high'], low=dataframe['low'], close=dataframe["close"], volume=dataframe['volume'], window=window, fillna=fillna).volume_weighted_average_price()
        return dataframe


