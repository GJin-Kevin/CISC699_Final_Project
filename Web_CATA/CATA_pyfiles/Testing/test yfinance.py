from data import DataAPI
from backtesting import Backtesting
from Visualization import Visualization
import pandas as pd 
import matplotlib.pyplot as plt



user1 = DataAPI("yahoo")


df = user1.yahoo_pricing_data('AAPL', start_date= "2015-10-30")

# -- sma --
# bt1 = Backtesting(df)
# df1 = bt1.backtesting_sma_single_stock(sma_short=5, sma_long=30)
# v1 = Visualize(df1)
# v1.sma_plot_result()

# -- rsi --

# bt1 = Backtesting(df)
# df1 = bt1.RSI_single_stock(period= 28)
# v1 = Visualize(df1)
# v1.sma_plot_result()

# path = r'D:\K\HU\HU - Courses\CISC 695 Research Methodology and Writing\Assignments\sample_data\rsi_aapl_data.csv'
# df1.to_csv(path)


#// test sma_backtesting bulk 

# bt1 = Backtesting(df)
# sma_s = [7, 12]
# sma_l = [35, 50]
# df2 = bt1.backtesting_sma_bulk_stocks(sma_s, sma_l)
# print(df2)


#// test bollonger band single

path = r"D:\K\HU\HU - Courses\CISC 695 Research Methodology and Writing\Assignments\sample_data\boll.csv"
df = user1.yahoo_pricing_data(start_date='2015-01-01')
# df = user1.SF_daily_pricing_data_from_local()
bt1 = Backtesting(df)
df1 = bt1.Bollinger_single_stock(sma_period = 25, std_period = 30)
df1.to_csv(path)
v1 = Visualization(df1)
v1.boll_plot_result()