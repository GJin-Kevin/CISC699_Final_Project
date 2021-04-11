from data import DataAPI
from backtesting import Backtesting
from Visualization import Visualize
import pandas as pd 
import matplotlib.pyplot as plt


user1 = DataAPI("IEX", IEX_token)

# path_aapl2y = r'D:\K\HU\HU - Courses\CISC 695 Research Methodology and Writing\Assignments\sample_data\aapl2y.csv'

# df = pd.read_csv(path_aapl2y)
# df = pd.read_csv(path_aapl2y)

df = user1.IEX_daily_pricing_data('AAPL', '2y')

bt1 = Backtesting(df)

df1 = bt1.RSI_single_stock(notification=False)

v1 = Visualize(df1)
v1.sma_plot_result()

# df2 = bt1.sma_backteting_bulk()
# print(df2)