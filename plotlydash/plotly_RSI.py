import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import sys
sys.path.append('./')

from CATA_pyfiles.data import DataAPI
from CATA_pyfiles.backtesting import Backtesting



def rsi_single(sec_id, start_date, end_date, period = 14):

    yahooapi = DataAPI(which_API="yahoo")
    df = yahooapi.yahoo_pricing_data(sec_id=sec_id, start_date = start_date, end_date = end_date)

    bt = Backtesting(df)
    df = bt.RSI_single_parameter(period = period)
    df['low_threshold'] = 30
    df['high_threshold'] = 70

    df_buy = df[df['signal'] == 'buy']
    df_sell = df[df['signal'] == 'sell']
    
    x1 = df_buy['date']
    y1 = df_buy['low']

    x2 = df_sell['date']
    y2 = df_sell['high']


    annotationsList_buy = [dict(
                    x=xi,
                    y=yi,
                    text="Buy",
                    showarrow=True,
                            font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                    align="center",
                    arrowhead=1,
                    arrowsize=1,
                    arrowwidth=1,
                    arrowcolor="#636363",
                    ax=0,
                    ay=30,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#55e06c",
                    opacity=0.8
                ) for xi, yi in zip(x1, y1)]

    annotationsList_sell = [dict(
                    x=xi,
                    y=yi,
                    text="Sell",
                    showarrow=True,
                    font=dict(
                    family="Courier New, monospace",
                    size=16,
                    color="#ffffff"
                    ),
                    align="center",
                    arrowhead=1,
                    arrowsize=1,
                    arrowwidth=1,
                    arrowcolor="#636363",
                    ax=0,
                    ay=-30,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="#de5b5b",
                    opacity=0.8
                ) for xi, yi in zip(x2, y2)]

    annotationsList = annotationsList_buy + annotationsList_sell

    layout = go.Layout(
        title = 'Back-testing RSI Strategy',
        yaxis_title = 'Stock Price',
        # xaxis_title = "Date",
        width = 1000,
        height = 600,
        plot_bgcolor="#FFFFFF",
        annotations = annotationsList
    )

    fig = go.Figure(go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'], name="Stock Price"
        ), layout=layout)



    text_stock_performance = "Stock performance:{:.2f}".format(df.loc[df.shape[0]-1, 'Pct_change'])

    fig.add_annotation(text=text_stock_performance,
                  xref="paper", yref="paper",
                  x=0.05, y=0.95, showarrow=False,
                  font=dict(
                    family="Courier New, monospace",
                    size=20,
                    color="#121111"
                    ))

    text_strategy_performance = "Strategy performance:{:.2f}".format(df.loc[df.shape[0]-1, 'Profit'])

    fig.add_annotation(text= text_strategy_performance,
                xref="paper", yref="paper",
                x=0.05, y=0.85, showarrow=False,
                font=dict(
                family="Courier New",
                size=20,
                color="#0f0f0f"
                ))

    fig.update_layout(
        xaxis_rangeslider_visible=False, width = 1200
    )


    return fig


def rsi_chart(sec_id, start_date, end_date, period = 14):

    yahooapi = DataAPI(which_API="yahoo")
    df = yahooapi.yahoo_pricing_data(sec_id=sec_id, start_date = start_date, end_date = end_date)

    bt = Backtesting(df)
    df = bt.RSI_single_parameter(period = period)
    df['low_threshold'] = 30
    df['high_threshold'] = 70

    layout = go.Layout(
        # title = 'Back-testing SMA Strategy',
        yaxis_title = 'RSI',
        # xaxis_title = "Date",
        width = 1000,
        height = 600,
        plot_bgcolor="#FFFFFF",
    )

    fig = go.Figure(go.Scatter(
        x=df['date'], y = df['RSI'], name="RSI", y0 = 0, dy = 10, mode= "lines"
        ), layout=layout)


    fig.add_trace(
        go.Scatter(
        x=df['date'], y = df['low_threshold'], name = "Low Threshold", mode= "lines"))

    fig.add_trace(
        go.Scatter(
        x=df['date'], y = df['high_threshold'], name = "High Threshold", mode= "lines"))

    fig.update_layout(
        xaxis_rangeslider_visible=False, width = 1200, height= 400, showlegend=False
    )

    return fig