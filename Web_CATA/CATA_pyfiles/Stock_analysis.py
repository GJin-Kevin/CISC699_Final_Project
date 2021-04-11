from data import DataAPI
from email_notification import Notification
from backtesting import Backtesting
from Visualization import Visualization
from strategy import Strategy

import pandas as pd
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Analysis_report:

    def __init__(self, sec_id: str = 'AAPL'):
        
        self.sec_id = sec_id
        self.sf_data_client = DataAPI(which_API = 'SimFin')
        self.yh_data_client = DataAPI(which_API = 'yahoo')
        self.period = 'annual'
        self.market = 'us'
        self.IS_revenue = None

    def stock_report(self, File_path):
        
        #// Retrive pricing data from yahoo finance
        df_pricing = self.yh_data_client.yahoo_pricing_data(sec_id = self.sec_id)
        
        #// Retrieve Income Statement
        df_income = self.sf_data_client.SF_income_statement(sec_id = self.sec_id, period = self.period, market = self.market )
        #// Retrieve Balance Sheet Data
        df_bs = self.sf_data_client.SF_balance_sheet(sec_id = self.sec_id, period = self.period, market = self.market )
        #// Retrieve Cash Flow Statement
        df_cf = self.sf_data_client.SF_cashflow_statment(sec_id = self.sec_id, period = self.period, market = self.market )
        #// Retrieve Ratios
        df_ratios = self.sf_data_client.SF_Derived_Ratios(sec_id = self.sec_id, period = self.period, market= self.market )
        
        #// Plot pricing chart
        self.plotly_stock_price(df_pricing)
        
        
        #// Balance Sheet

        df_bs = df_bs.T
        #// Balance Sheet commonsize
        df_BS_common_size = self.balance_sheet_commonsize(df_bs.T)
    
        #// Income Statement Common Size
        df_IS_common_size = self.income_statment_common_size(df_income)
        
        #// Cash flow statement 
        df_cf = df_cf.T
        
        #// Ratio
        df_ratios = self.ratios_yoy(df_ratios)

        #// write data to an excel file
        with pd.ExcelWriter(File_path) as writer:  
            df_bs.to_excel(writer, sheet_name = "Balance Sheet")
            df_BS_common_size.to_excel(writer, sheet_name = "Balance Sheet Commonsize")
            df_IS_common_size.to_excel(writer, sheet_name='Income Statement')
            df_cf.to_excel(writer, sheet_name = "Cash Flow Statement")
            df_ratios.to_excel(writer, sheet_name = "Ratios")
            df_pricing.to_excel(writer, sheet_name = "Historical_price")
            
    def plotly_stock_price(self, df):
        fig = go.Figure(data=[go.Candlestick(x=df['date'],
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])])
        fig.layout.xaxis.type = 'category'
        fig.show()
        
    def income_statment_common_size(self, df):
        
        dfT = df.T
        
        Row_Revenue = dfT.index.get_loc('Revenue') + 1

        Row_lis = dfT.index[Row_Revenue:]
        
        self.IS_revenue = dfT.loc['Revenue']
        df_temp = dfT.iloc[:Row_Revenue, :]
        
        for i in Row_lis:
            
            S_lis = self.IS_add_yoy_rows(dfT.loc[i])
            df_temp = df_temp.append(dfT.loc[i].map(lambda x:  '{:,} M'.format(x/1000000)), ignore_index = False)
            df_temp = df_temp.append(S_lis, ignore_index = False)
        
        return df_temp

    def IS_add_yoy_rows(self, row_series):
        
        #// Add yoy pct change, commonsize, yoy_commonsize rows into Income Stetement
        row_index_name = row_series.name
        YOY_name = "YOY_" + row_index_name
        S_YOY_name = pd.Series(self.yoy_pct_change(row_series), name = YOY_name)
        
        CommonSize_Name= "CommonSize_" + row_index_name
        S_CommonSize_Name = pd.Series(row_series/self.IS_revenue, name = CommonSize_Name)
        
        YOY_CommonSize_Name = "YOY_CommonSize_" + row_index_name
        S_YOY_CommonSize_Name = pd.Series(self.yoy_pct_change(S_CommonSize_Name), name = YOY_CommonSize_Name)
        
        S_lis = [S_YOY_name, S_CommonSize_Name, S_YOY_CommonSize_Name]
        
        return S_lis
        
    def yoy_pct_change(self, col_series):
        
        #// replace pct_change function as it is not accurate when numbers are negative
        S_pct_change = (col_series - col_series.shift(1))/col_series.shift(1).map(lambda x: x if x >= 0 else -x)
        S_pct_change = S_pct_change.map(lambda x: '{:.2%}'.format(x))

        return S_pct_change


    def balance_sheet_yoy(self, df):
        
        dfT = df.T
        
        Ros_shares = dfT.index.get_loc('Shares (Diluted)') + 1
        Row_lis = dfT.index[Ros_shares:]
        
        df_temp = dfT.iloc[:Ros_shares, :]
        
        for i in Row_lis:
            
            S_yoy_col = self.BS_add_yoy_rows(dfT.loc[i])
            df_temp = df_temp.append(dfT.loc[i].map(lambda x:  '{:,} M'.format(x/1000000)), ignore_index = False)
            df_temp = df_temp.append(S_yoy_col, ignore_index = False)
        
        return df_temp

    def BS_add_yoy_rows(self, row_series):
        
        #// Add yoy pct change, commonsize, yoy_commonsize rows into Income Stetement
        row_index_name = row_series.name
        YOY_name = "YOY_" + row_index_name
        S_YOY_name = pd.Series(self.yoy_pct_change(row_series), name = YOY_name)

        return S_YOY_name
        
    def yoy_pct_change(self, col_series):
        
        #// replace pct_change function as it is not accurate when numbers are negative
        col_shift_1 = col_series.shift(1).map(lambda x: x + 0.0001 if x >= 0 else -x)
        S_pct_change = (col_series - col_series.shift(1))/col_shift_1
        S_pct_change = S_pct_change.map(lambda x: '{:.2%}'.format(x))

        return S_pct_change



    def balance_sheet_commonsize(self, df):
        
        #// transpose to date as columns
        df = df.T
        
        #// categorize index names into asset and liabilities
        lis_asset = ['Cash, Cash Equivalents & Short Term Investments', 'Accounts & Notes Receivable', 'Inventories',
                'Property, Plant & Equipment, Net', 'Long Term Investments & Receivables', 'Other Long Term Assets',
                'Total Noncurrent Assets']
        total_asset = 'Total Assets'
        lis_liability = ['Payables & Accruals','Short Term Debt', 'Total Current Liabilities', 
                        'Long Term Debt','Total Noncurrent Liabilities']
        total_liability = 'Total Liabilities'
        lis_equity = ['Share Capital & Additional Paid-In Capital', 'Treasury Stock','Retained Earnings']
        total_equity = 'Total Equity'
        total_liabilityNequity = 'Total Liabilities & Equity'

        df.loc[lis_asset] = df.loc[lis_asset]/df.loc[total_asset]
        df.loc[lis_liability] = df.loc[lis_liability]/df.loc[total_liabilityNequity]
        df.loc[lis_equity] = df.loc[lis_equity]/df.loc[total_liabilityNequity]
        
        lis_a = lis_asset + lis_liability + lis_equity
        lis_b = [total_asset, total_liability, total_equity, total_liabilityNequity, 'Total Current Assets']
        
        df.loc[lis_a] = df.loc[lis_a].applymap(lambda x: '{:.2%}'.format(x))
        df.loc[lis_b] = df.loc[lis_b].applymap(lambda x: '{:,} M'.format(x/1000000))

        return df

    def ratios_yoy(self, df):
        
        df = df.T
        
        lis = ['EBITDA', 'Total Debt', 'Free Cash Flow',
        'Gross Profit Margin', 'Operating Margin', 'Net Profit Margin',
        'Return on Equity', 'Return on Assets', 'Free Cash Flow to Net Income',
        'Current Ratio', 'Liabilities to Equity Ratio', 'Debt Ratio',
        'Earnings Per Share, Basic', 'Earnings Per Share, Diluted',
        'Sales Per Share', 'Equity Per Share', 'Free Cash Flow Per Share',
        'Dividends Per Share']
        
        Row_Ebida = df.index.get_loc('EBITDA')
        df_temp = df.iloc[:Row_Ebida, :]

        for i in lis:
            
            row_index_name = df.loc[i].name
            YOY_name = "YOY_" + row_index_name
            S_YOY_name = pd.Series(self.yoy_pct_change(df.loc[i]), name = YOY_name)
            
            df_temp = df_temp.append(df.loc[i])
            df_temp = df_temp.append(S_YOY_name, ignore_index = False)
            
        
        lis_dollar_Form = ['EBITDA', 'Total Debt', 'Free Cash Flow']
        lis_pct_form = ['Gross Profit Margin', 'Operating Margin', 'Net Profit Margin',
        'Return on Equity', 'Return on Assets', 'Free Cash Flow to Net Income',
        'Current Ratio', 'Liabilities to Equity Ratio', 'Debt Ratio']
        
        
        df_temp.loc[lis_pct_form] = df_temp.loc[lis_pct_form].applymap(lambda x: '{:.2%}'.format(x))
        df_temp.loc[lis_dollar_Form] = df_temp.loc[lis_dollar_Form].applymap(lambda x: '{:,} M'.format(x/1000000))

        
        return df_temp
