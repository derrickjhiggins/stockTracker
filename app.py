import requests, os
from bs4 import BeautifulSoup
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import yfinance as yf
from model import create_prediction_model


app = Dash(__name__)
app.server.static_folder = os.path.join(os.getcwd(), 'images')

# fig = px.bar(df, x="Ticker", y="Price", color="City", barmode="group")
nav = html.Div([html.H1('Stock Tracker'),

    html.H2("Welcome to my stocks Dash App!", className="start"), 
    html.Div([
        dcc.Input(id='ticker-input', type='text', placeholder='Ticker (e.g. AAPL)'),
        html.Button('Submit', id='ticker-submit', n_clicks=0, className='right-align-button'),
    ]),
    html.Div([
        dcc.DatePickerRange(
            id='stockDates',
            min_date_allowed=date(2010,1,1),
            max_date_allowed=date.today(),
            initial_visible_month=date(2015,1,1),
            end_date=date.today(),
            display_format='MMM D, YYYY'
        )
    ]),
    html.Div([
        dcc.Input(id='quantity-input', type='number', value=0, min=0),
        html.Button('Forecast', id='forecast-button', n_clicks=0)
    ])
], className='input')

content = html.Div(id='company-info')
app.layout = html.Div([nav, content, ], className="container")

# callback functions
@app.callback(
    Output(component_id="company-info", component_property='children'),
    # Output(component_id="forecast-button", component_property='children'),
    Input(component_id="ticker-input", component_property='value'),
    Input(component_id='ticker-submit', component_property='n_clicks'),
    Input(component_id='forecast-button', component_property='n_clicks'),
    Input(component_id='quantity-input', component_property='value'),
    [Input('stockDates', 'start_date'),
    Input('stockDates', 'end_date')]
)
# [State(component_id="ticker-submit-button", component_property='children')])
def update_data(stockSymbol, n_clicks, forecast_n_clicks, forecast_value, start_date, end_date):
    if not n_clicks:
        return

    # generate historical stock prices graph
    ticker = yf.Ticker(stockSymbol)
    inf = ticker.info
    company_data = yf.download(inf['symbol'], start_date, end_date)
    company_data.reset_index(inplace=True)
    print(company_data)
    df = pd.DataFrame().from_dict(inf, orient='index')
    logo_url = get_logo(df[0]['website'])
    graph_fig = get_chart(company_data, start_date, end_date)
    content = html.Div([
        html.P(f"Symbol: {df[0]['symbol']}"),
        html.P(f"Industry: {df[0]['industry']}"),
        html.P(f"Description: {df[0]['longBusinessSummary']}"),
        html.Img(src=logo_url, alt='Company Logo'),
        dcc.Graph(figure=graph_fig),
    ])

    # check if forecast_graph to be added
    if forecast_n_clicks:
        days = forecast_value
        print(days)
        forecast_data = create_prediction_model(stockSymbol, days)
        print(forecast_data)
        forecast_fig = px.line(forecast_data, x='Date', y='Forecast')
        forecast_graph = dcc.Graph(figure=forecast_fig)
        content.children.append(forecast_graph)

    return [content]

def get_logo(company_domain):
    response = requests.get(f'https://logo.clearbit.com/{company_domain}')
    if response.status_code == 200:
        logo_url = response.url
    else:
        logo_url = 'https://previews.123rf.com/images/urfandadashov/urfandadashov1806/urfandadashov180601827/150417827-photo-not-available-vector-icon-isolated-on-transparent-background-photo-not-available-logo-concept.jpg'
    return logo_url

def get_chart(data, start_date, stop_date):
    data.reset_index(inplace=True)
    fig = px.line(data, x='Date', y='Adj Close')
    return fig

# update n-clicks callback
# @app.callback(
#     Output(component_id='ticker-submit', component_property='n_clicks'),
#     [Input(component_id='ticker-submit', component_property='n_clicks')]
#     # [State(component_id='graph-content', component_property='children')]
# )
# def reset_n_clicks(n_clicks):
#     if n_clicks:
#         return None

if __name__ == '__main__':
    # Set the static folder to serve images
    static_folder = os.path.join(os.getcwd(), 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Add the static route
    app.server.static_folder = static_folder
    app.server.static_route = '/static/'

    app.run_server(debug=True)