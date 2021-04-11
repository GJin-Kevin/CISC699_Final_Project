import unittest
import pandas as pd

import sys
sys.path.append('./')

from CATA_pyfiles.data import DataAPI
from CATA_pyfiles.backtesting import Backtesting
from CATA_pyfiles.Visualization import Visualization

class Test_DataAPI(unittest.TestCase):


    def test_SF_daily_pricing_data(self):

        usr = DataAPI(which_API='SimFin', token ='free')
        result = usr.SF_pricing_data('AAPL', period='Daily', market = 'us', 
                            start_date='2018-01-01', end_date= '2020-10-30')
        self.assertIsInstance(result, pd.DataFrame)

    def test_SF_income_statement(self):

        usr = DataAPI(which_API='SimFin', token ='free')
        result = usr.SF_income_statement('AAPL', period='quarterly', market = 'us')
        self.assertIsInstance(result, pd.DataFrame)

    def test_SF_balance_sheet(self):

        usr = DataAPI(which_API='SimFin', token ='free')
        result = usr.SF_balance_sheet('AAPL', period='quarterly', market = 'us')
        self.assertIsInstance(result, pd.DataFrame)

    def test_SF_cashflow_statment(self):

        usr = DataAPI(which_API='SimFin', token ='free')
        result = usr.SF_cashflow_statment('AAPL', period='quarterly', market = 'us')
        self.assertIsInstance(result, pd.DataFrame)


    def test_yahoo_pricing_data(self):

        usr = DataAPI(which_API='yahoo')
        result = usr.yahoo_pricing_data('AAPL', start_date='2018-01-01', end_date= '2020-10-30')
        self.assertIsInstance(result, pd.DataFrame)


class Test_Backtesting(unittest.TestCase):

    def get_data(self):
        
        df = DataAPI.yahoo_pricing_data('AAPL', start_date='2019-01-01', end_date= '2020-10-30')
        return df

    def test_SMA_bulk_parameters(self):
        
        df = self.get_data()
        Bt = Backtesting(df)
        
        result = Bt.SMA_bulk_parameters()
        self.assertIsInstance(result, pd.DataFrame)

    def test_SMA_single_parameter(self):
        
        df = self.get_data()
        Bt = Backtesting(df)
        
        result = Bt.SMA_single_parameter()
        self.assertIsInstance(result, pd.DataFrame)

    def test_RSI_single_parameter(self):
        
        df = self.get_data()
        Bt = Backtesting(df)
        
        result = Bt.RSI_single_parameter()
        self.assertIsInstance(result, pd.DataFrame)

    def test_Bollinger_single_parameter(self):
        
        df = self.get_data()
        Bt = Backtesting(df)
        
        result = Bt.Bollinger_single_parameter()
        self.assertIsInstance(result, pd.DataFrame)


    def test_backtesting(self):
        
        df = self.get_data()
        Bt = Backtesting(df)
        df = Bt.SMA_single_parameter()

        result = Bt.backtesting(df)
        self.assertIsInstance(result, pd.DataFrame)    

class Test_Visualization(unittest.TestCase):

    def get_data(self):
        
        df = DataAPI.yahoo_pricing_data('AAPL', start_date='2019-01-01', end_date= '2020-10-30')
        return df

    def test_sma_plot_result(self):
        
        df = self.get_data()

        Bt = Backtesting(df)
        df = Bt.SMA_single_parameter()

        vi = Visualization(df)
        result = vi.sma_plot_result()

        self.assertIsNone(result)


    def test_rsi_plot_result(self):
        
        df = self.get_data()

        Bt = Backtesting(df)
        df = Bt.RSI_single_parameter()

        vi = Visualization(df)
        result = vi.rsi_plot_result()

        self.assertIsNone(result)




if __name__ == '__main__':
    unittest.main()