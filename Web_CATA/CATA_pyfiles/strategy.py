from data import DataAPI
import pandas as pd 
from backtesting import Backtesting
from ib_app import  IbApp
from email_notification import Notification


class Strategy:

    def __init__(self, email_add = None, email_pwd = None, brokerage_platform = None, user_id = None, password = None):
        # Initiate Broker Account and gmail account
        # Interactive Brokers TWS (Trader Workstation) software is needed to connect to Interactive Brokers' API. 
        # The webpage to download TWS: https://www.interactivebrokers.com/en/index.php?f=14099
        
        self.clent = IbApp()
        self.Email_client = Notification(email_add, email_pwd)
        self.brokerage_platform = brokerage_platform
        self.user_id = user_id
        self.password = password
        self.email_add = email_add

    def Implement_SMA(self, sec_id = 'AAPL', qty = 10, sma_short = 20, sma_long = 50, start_date = "2018-10-30"):
        
        # Get real time data from Interactive Broker
        user1 = DataAPI()
        df = user1.yahoo_pricing_data(sec_id, start_date = start_date)

        # Check the signal
        # -- sma --
        BT_user1 = Backtesting(df)
        df = BT_user1.SMA_single_stock(sma_short = sma_short , sma_long = sma_long)

        print('signal: {}'.format(df.loc[df.shape[0] - 1, 'signal']))
        # check the most recent signal 
        

        if df.loc[df.shape[0] - 1, 'signal'] == 'buy':

            self.submit_buy_order(sec_id, qty)
            self.Email_client.send_buy_notification(self.email_add, sec_id)

        elif df.loc[df.shape[0] - 1, 'signal'] == 'sell':

            self.submit_sell_order(sec_id, qty)
            self.Email_client.send_sell_notification(self.email_add, sec_id)


    def Implement_RSI(self, sec_id = 'AAPL', qty = 10, period= 14 , start_date = "2018-10-30"):
        
        # Get real time data from Interactive Broker
        user1 = DataAPI()
        df = user1.yahoo_pricing_data(sec_id, start_date = start_date)

        # Check the signal
        # -- sma --
        BT_user1 = Backtesting(df)
        df = BT_user1.RSI_single_stock(period= 14)

        print('signal: {}'.format(df.loc[df.shape[0] - 1, 'signal']))
        # check the most recent signal 
        

        if df.loc[df.shape[0] - 1, 'signal'] == 'buy':

            self.submit_buy_order(sec_id, qty)
            self.Email_client.send_buy_notification(self.email_add, sec_id)

        elif df.loc[df.shape[0] - 1, 'signal'] == 'sell':

            self.submit_sell_order(sec_id, qty)
            self.Email_client.send_sell_notification(self.email_add, sec_id)


    def submit_buy_order(self, sec_id, qty):

        self.clent.set_order_attributes(sec_id, 'BUY', qty)
        self.clent.main()


    def submit_sell_order(self, sec_id, qty):
 
        self.clent.set_order_attributes(sec_id, 'SELL', qty)
        self.clent.main()


