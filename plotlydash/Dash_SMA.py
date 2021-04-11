#// Back-Testing Page


from dash import Dash
import dash_html_components as html 
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px 
import yfinance as yf
import datetime
import pandas as pd 
import flask
from flask import current_app as app
from plotlydash.plotly_SMA import sma_single


def create_dashboard_sma(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/backtest-sma/',
        external_stylesheets=[dbc.themes.FLATLY],
        meta_tags=[{'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'}]
    )

    # Create Dash Layout
    dash_app.layout = dbc.Container([

        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1("Back-Testing: SMA", className = "text-center bg-primary text-white mb-4", style={'marginBottom': 25, 'marginTop': 25}),
                    html.P("Simple Moving Average Strategy (Long only)", className = "font-weight-bolder", style={'fontSize': 24, 'marginBottom': 25})
                ]), width = 12)
        ]),
        
        dbc.Row([

            dbc.Col([
                html.Div([
                    html.H5("Ticker", className = "font-weight-bolder", style={'marginTop': 5})
                ])],  width={'size':1}),

            dbc.Col([
                dcc.Input(id="input_ticker", type = 'text', placeholder = "AAPL", value = "AAPL")], width={'size':2}
                ),

            dbc.Col([
                html.Div([
                    html.H5("Date", className = "font-weight-bolder", style={'marginTop': 5})
                ])],  width={'size':1, 'offset':1}),

            dbc.Col([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    start_date_placeholder_text="2020-01-01", start_date = "2020-01-01",
                    end_date_placeholder_text="2021-01-01", end_date = '2021-01-01',
                    calendar_orientation='vertical',)], width={'size':6, 'offset':0} )
        ], align="center"),

        dbc.Row([

            dbc.Col([
                html.Div([
                    html.H5("SMA_short", className = "font-weight-bolder", style={'marginTop': 5})
                ])],  width={'size':1}),

            dbc.Col([
                dcc.Input(id="sma_short", type = 'number', placeholder = 21, value = 21)], width={'size':2}
                ),

            dbc.Col([
                html.Div([
                    html.H5("SMA_long", className = "font-weight-bolder", style={'marginTop': 1})
                ])],  width={'size':1, 'offset':1}),

            dbc.Col([
                dcc.Input(id="sma_long", type = 'number', placeholder = 45, value = 45)], width={'size':2}
                )
        ], align="center", style={'marginTop': 20, 'marginBottom': 20}),

        dbc.Row([

            dbc.Col([
                dcc.Graph(id='line-fig', figure={})], width= {"size":12, 'offset': 0, 'order':0})
        ]),
    ])

    init_callbacks(dash_app)

    return dash_app.server

def init_callbacks(dash_app):
    # Line chart - Single
    @dash_app.callback(
        Output('line-fig', 'figure'),
        [Input('input_ticker', 'value'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')],
        Input('sma_short', 'value'),
        Input('sma_long', 'value')
    )
    def update_graph(stock_slctd, start_date, end_date, sma_short, sma_long):
        fig = sma_single(stock_slctd, start_date, end_date, sma_short, sma_long)

        return fig

