import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

import sys
sys.path.append('./')

from CATA_pyfiles.data import DataAPI
from CATA_pyfiles.backtesting import Backtesting



def vwap_single(sec_id, start_date, end_date, sma_short, sma_long):

    yahooapi = DataAPI(which_API="yahoo")
    df = yahooapi.yahoo_pricing_data(sec_id=sec_id, start_date = start_date, end_date = end_date)

    bt = Backtesting(df)
    df = bt.VWAP_single_parameter(sma_short = sma_short, sma_long = sma_long)

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
        # title = 'Back-testing SMA Strategy',
        yaxis_title = 'Stock Price',
        xaxis_title = "Date",
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


    fig.add_trace(
        go.Scatter(
            x=df['date'], y=df['vwap_short'], mode = 'lines', name="SMA_Short", marker_color='rgba(45, 51, 235, 1)'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['date'], y=df['vwap_long'], mode = 'lines', name="SMA_Long", marker_color='rgba(199, 44, 219, 1)'
        )
    )

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
        xaxis_rangeslider_visible=False,
    )

    return fig