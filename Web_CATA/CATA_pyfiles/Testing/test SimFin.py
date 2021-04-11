from data import DataAPI
from backtesting import Backtesting
from Visualization import Visualization
import pandas as pd 
import matplotlib.pyplot as plt

# user_yf = DataAPI('yahoo')
# df = user_yf.yahoo_pricing_data()

# print(df)

user1 = DataAPI("SimFin")

# df_income = user1.SF_income_statement()
# print('Income statement')
# print(df_income)

# df_bs = user1.SF_balance_sheet()
# print('balancesheet statement')
# print(df_bs)

# df_cf = user1.SF_cashflow_statment()
# print('cashflow statement')
# print(df_cf)



#// test sma_backtesting single

# df = user1.SF_pricing_data(start_date='2016-01-01')
# # df = user1.SF_daily_pricing_data_from_local()
# bt1 = Backtesting(df)
# df1 = bt1.SMA_single_stock(sma_short=5, sma_long=30)
# v1 = Visualize(df1)
# v1.sma_plot_result()

#// test sma_backtesting bulk 
# df = user1.SF_pricing_data(start_date='2016-01-01')
#df = user1.SF_daily_pricing_data_from_local()
# bt1 = Backtesting(df)
# sma_s = [7, 12, 20, 27]
# sma_l = [35, 50, 90, 120]
# df2 = bt1.sma_backteting_bulk(sma_s, sma_l)
# print(df2)

#// test bollonger band single
path = r"D:\K\HU\HU - Courses\CISC 695 Research Methodology and Writing\Assignments\sample_data\boll.csv"
df = user1.SF_pricing_data(start_date='2016-01-01')
# df = user1.SF_daily_pricing_data_from_local()
bt1 = Backtesting(df)
df1 = bt1.Bollinger_single_stock(sma_period = 30, std_period = 20)
df1.to_csv(path)
v1 = Visualization(df1)
v1.sma_plot_result()