import pandas as pd
import numpy as np
import requests

import simfin
from simfin.names import *
import yfinance as yf

class DataAPI:

    def __init__(self, which_API: str = 'yahoo', token: str = None) -> None:
        """Initalizes a new instance of the DataAPI and connects to the API platform specified

        Args:
            which_API (str, optional): currently three options
                                        - 'IEX': https://iexcloud.io/
                                        - 'SimFin': https://simfin.com/
                                        - 'yahoo finance'
            token (str, optional): [token for API]. Defaults to None.
        """        
        
        # Set the attributes depending on different API platform
        if which_API == "IEX":
            self.API = which_API
            self.token = token

        elif which_API == "SimFin":
            self.API = which_API

            if token is None:
                #// If you are a SimFin+ user, then save your key into the simfin_api_key file. If not, API key will be set to free.
                self.token = simfin.load_api_key(path='~/simfin_api_key.txt', default_key='free')
            else:
                self.token = token
                simfin.set_api_key(api_key=self.token)

            simfin.set_data_dir('~/simfin_data/')

        elif which_API == "yahoo":
            self.API = which_API

        self.base_url = self._base_url()
        

    def _base_url(self):
        """Change base URL to conenct to API

        Returns:
            [type]: None
        """        

        if self.API == "IEX":
            self.base_url = "https://cloud.iexapis.com"
        elif self.API == "SimFin":
            self.base_url = ""
        else:
            self.base_url = ""
        
        return self.base_url

    def IEX_daily_pricing_data(self, sec_id: str = 'AAPL', duration: str = '1y') -> pd.DataFrame:
        """[summary] Send API request to IEX Cloud to retrieve daily pricing data. In order to use IEX API, a token is needed when initializing
                        an instance of DataAPI.

        Args:
            sec_id (str, optional): [ticker]. Defaults to None.
            duration (str, optional): [see below parameters can be used]. Defaults to 1 year.
                max	All available data up to 15 years	Historically adjusted market-wide data
                5y	Five years	Historically adjusted market-wide data
                2y	Two years	Historically adjusted market-wide data
                1y	One year	Historically adjusted market-wide data
                ytd	Year-to-date	Historically adjusted market-wide data
                6m	Six months	Historically adjusted market-wide data
                3m	Three months	Historically adjusted market-wide data
                1m	One month (default)	Historically adjusted market-wide data
                1mm	One month	Historically adjusted market-wide data in 30 minute intervals
                5d	Five Days	Historically adjusted market-wide data by day.
                5dm	Five Days	Historically adjusted market-wide data in 10 minute intervals

        Returns:
            pd.DataFrame: [pricing dataframe]
        """        

        # convert to api format
        token_new = "?token=" + self.token
        
        if duration is None:
            available_methods = '/stable/stock/{symbol}/chart'.format(symbol = sec_id)
            complete_url = self.base_url + available_methods + token_new
        else:
            available_methods = '/stable/stock/{symbol}/chart/{range}'.format(symbol = sec_id, range = duration)
            complete_url = self.base_url + available_methods + token_new
        
        # request api
        response = requests.get(complete_url)
        # check status code
        if response.status_code == 200:
            df = pd.DataFrame.from_dict(response.json())
            # standard format
            df = df[['date', 'open', 'close', 'high', 'low', 'volume']]
            df['date'] = pd.to_datetime(df['date'])

        else:
            print("Error: {status_code}".format(status_code = response.status_code))
            return None
        
        return df
        
    def yahoo_pricing_data(self, sec_id = 'AAPL', start_date = None, end_date = None) -> pd.DataFrame:
        """[summary] Retrieve pricing data from yahoo finance. No token is needed for recent data.

        Args:
            sec_id (str, optional): [description]. Defaults to 'AAPL'.
            start_date ([type], optional): [description]. Defaults to None.
            end_date ([type], optional): [description]. Defaults to None.

        Returns:
            pd.DataFrame: [description]
        """        

        df = yf.download(tickers = sec_id, start = start_date, end = end_date)
        df = df.reset_index()
        df = df.rename(columns={"Date": "date", 'Open':'open', 'Close':'close', 'High':'high', 'Low':'low', 'Volume':'volume'})
        df = df[['date', 'open', 'close', 'high', 'low', 'volume']]
        df['date'] = pd.to_datetime(df['date'])

        return df

    def SF_pricing_data(self, sec_id = 'AAPL', period: str = 'Daily', market: str = 'us', start_date = None, end_date = None) -> pd.DataFrame:
        """[summary] Get dailiy pricing data from simfin. Token is needed for the most recent data.
                    This function will download a csv file with pricing data for US stocks.

        Args:
            sec_id (str, optional): [stock ticker]. Defaults to 'AAPL'.
            period (str, optional): [the period of stock price]. Defaults to 'Daily'.
            market (str, optional): [stock market, us, de, etc]. Defaults to 'us'.
            start_date ([type], optional): ['xxxx-xx-xx' start date of pricing data]. Defaults to None.
            end_date ([type], optional): ['xxxx-xx-xx' end date of pricing data]. Defaults to None.

        Returns:
            pd.DataFrame: 
        """        

        df = simfin.load_shareprices(variant= period, market=market)
       
        df = df.loc[sec_id]
        df = df.reset_index()
        df = df.rename(columns={"Date": "date", 'Open':'open', 'Close':'close', 'High':'high', 'Low':'low', 'Volume':'volume'})
        
        df = df[['date', 'open', 'close', 'high', 'low', 'volume']]
        df['date'] = pd.to_datetime(df['date'])


        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        if start_date is None and end_date is None:
            return df
        elif start_date is not None and end_date is None:
            df = df[(df['date'] >= start_date)]
        elif start_date is None and end_date is not None:
            df = df[(df['date'] <= end_date)]
        else:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date )]

        df = df.reset_index()
        return df

    def SF_income_statement(self, sec_id: str = 'AAPL', period : str = 'quarterly', market :str = 'us') -> pd.DataFrame:
        """[summary] Load income statement data.

        Args:
            sec_id (str, optional): [stock tiker]. Defaults to 'AAPL'.
            period (str, optional): [annual, quarterly]. Defaults to 'annual'.
            market (str, optional): [us, de, etc]. Defaults to 'us'.

        Returns:
            pd.DataFrame: 
        """        

        df_income = simfin.load_income(variant=period, market=market,
              index=[TICKER, REPORT_DATE, FISCAL_PERIOD],
              parse_dates=[REPORT_DATE, PUBLISH_DATE, RESTATED_DATE])
        df_income = df_income.loc[sec_id]

        return df_income


    def SF_balance_sheet(self, sec_id: str = 'AAPL', period : str = 'quarterly', market :str = 'us') -> pd.DataFrame:
        """[summary] Load balance sheet data.

        Args:
            sec_id (str, optional): [stock ticker]. Defaults to 'AAPL'.
            period (str, optional): [annual, quarterly]. Defaults to 'quarterly'.
            market (str, optional): [us, de, etc]. Defaults to 'us'.

        Returns:
            pd.DataFrame: 
        """        

        df_balance = simfin.load_balance(variant = period, market = market)

        df_balance = df_balance.loc[sec_id]

        return df_balance

    def SF_cashflow_statment(self, sec_id: str = 'AAPL', period : str = 'quarterly', market :str = 'us') -> pd.DataFrame:
        """[summary] Load cash flow statement.

        Args:
            sec_id (str, optional): [stock ticker]. Defaults to 'AAPL'.
            period (str, optional): [annual, quarterly]. Defaults to 'quarterly'.
            market (str, optional): [us, de, etc]. Defaults to 'us'.

        Returns:
            pd.DataFrame: 
        """        

        df_cashflow = simfin.load_cashflow(variant = period, market = market)

        df_cashflow = df_cashflow.loc[sec_id]

        return df_cashflow

    def SF_ratios(self, sec_id: str = 'AAPL', period : str = 'annual', market :str = 'us') -> pd.DataFrame:
        """[summary] Load cash flow statement.

        Args:
            sec_id (str, optional): [stock ticker]. Defaults to 'AAPL'.
            period (str, optional): [annual, quarterly]. Defaults to 'quarterly'.
            market (str, optional): [us, de, etc]. Defaults to 'us'.

        Returns:
            pd.DataFrame: 
        """        

        df_ra = simfin.load_derived(variant = period, market = market)

        df_ra = df_ra.loc[sec_id]

        return df_ra


    def SF_Derived_Ratios(self, sec_id: str = 'AAPL', period : str = 'quarterly', market :str = 'us') -> pd.DataFrame:
        """[summary] Load ratios data.

        Args:
            sec_id (str, optional): [stock ticker]. Defaults to 'AAPL'.
            period (str, optional): [annual, quarterly]. Defaults to 'quarterly'.
            market (str, optional): [us, de, etc]. Defaults to 'us'.

        Returns:
            pd.DataFrame: 
        """        

        df_ratios = simfin.load_derived(variant=period, market=market)

        df_ratios = df_ratios.loc[sec_id]

        return df_ratios
       

    
    def IB_pricing_date(self):
        pass