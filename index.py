import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
from dash.exceptions import PreventUpdate

from bs4 import BeautifulSoup
import requests
import flask
from flask import Flask
import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import yfinance as yf
import numpy as np
import praw
import sqlite3

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash_utils import make_table, make_card, ticker_inputs, make_item
from reddit_data import get_reddit
from tweet_data import get_options_flow
# , get_financial_reportformatted
from fin_report_data import get_financial_report
from yf import get_screener
from yf1 import get_screener1
from yf2 import get_screener2
# from ratio import ratios

conn = sqlite3.connect('stocks.sqlite')
ticker = ''
server = Flask(__name__)
app = dash.Dash(__name__, server=server, meta_tags=[
                {"content": "width=device-width"}], external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True

get_options_flow()
flow = pd.read_sql(
    "select datetime, text from tweets order by datetime desc", conn)
global tables111, tables222, tables333
global dfr
dfr = get_reddit()
tables111 = get_screener('111')
tables222 = get_screener1('111')
tables333 = get_screener2('111')
layout1 = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Main', children=[
             # html.Div(id = 'cards')
             dbc.Row([dbc.Col(make_card("Enter Ticker", "success",
                                        ticker_inputs('ticker-input', 'date-picker', 36)))])  # row 1
             , dbc.Row([dbc.Col([make_card("Twitter Order Flow", 'primary', make_table('table-sorting-filtering2', flow, '17px', 10))]),
                        dbc.Col([make_card("Company Data ", "secondary", html.Div(id="fin-table"))])]),
             dbc.Row([make_card("select ticker", "warning", "select ticker")],
                     id='cards')  # row 2
             , dbc.Row([make_card("select ticker", "warning", "select ticker")],
                       id='cards1'),
             dbc.Row([
                # dbc.Col([
                #     dbc.Row([make_card("Wallstreet Bets New Posts", 'primary', [html.P(html.Button('Refresh', id='refresh')), make_table('table-sorting-filtering', dfr, '17px', 4)])
                #              ], justify='center')
                # ]),
                dbc.Col([dbc.Row([dbc.Alert("________________________Charts________________________", color="primary")], justify='center'),
                         dbc.Row(html.Div(id='x-vol-1'), justify='center'), dcc.Interval(
                    id='interval-component',
                    interval=1*150000,  # in milliseconds
                    n_intervals=0), dcc.Interval(
                    id='interval-component2',
                    interval=1*60000,  # in milliseconds
                    n_intervals=0),
                    #  dbc.Row([html.Div(id='tweets')])
                ]),
                ]),
             ]),
        dcc.Tab(label='Screener', children=[
            dbc.Row([dbc.Col([make_card("Quality Stocks", 'primary', [html.P(html.Button('Refresh', id='refresh1')), make_table('table-sorting-filtering3', tables111, '17px', 10)]),
                              ]),
                     ]),  # end row
            dbc.Row([dbc.Col([make_card("Recent Insider Buying", 'primary', make_table('table-sorting-filtering4', tables222, '17px', 10)),
                              ]),
                     ]),
            dbc.Row([dbc.Col([make_card("Major News", 'primary', make_table('table-sorting-filtering5', tables333, '17px', 10)),
                              ]),
                     ])
        ]),
        dcc.Tab(label='Help', children=[
            dbc.Row([html.Center(html.P('What is Eps?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('Earnings per share (EPS) is a companys net profit divided by the number of common shares it has outstanding. EPS indicates how much money a company makes for each share of its stock, and is a widely used metric to estimate corporate value.', style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'margin': '10px', 'width': '80em'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('What is LTD?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('Long Term Debt (LTD) is any amount of outstanding debt a company holds that has a maturity of 12 months or longer. It is classified as a non-current liability on the companys balance sheet. A debenture is a long-term debt instrument issued by corporations and governments to secure fresh funds or capital.', style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'font': 'Calibri', 'width': '80em'})), ], justify="around", align="center"),
            dbc.Row([html.Center(html.P('What is Shareholders Equity?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P("Shareholders equity is the amount that shows how the company has been financed with the help of common shares and preferred shares. Shareholder's equity is also called Share Capital, Stockholders Equity or Net worth. There are two important sources from which you can get shareholders equity.", style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'width': '80em'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('What is Net Income?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('Net income, also called net earnings, is sales minus cost of goods sold, general expenses, taxes, and interest.', style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'width': '80em'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('What is Interest Expense?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('Interest expense is a non-operating expense shown on the income statement. It represents interest payable on any borrowings ??? bonds, loans, convertible debt or lines of credit. It is essentially calculated as the interest rate times the outstanding principal amount of the debt.', style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'width': '80em'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('What is EBITDA?', style={
                     'color': 'blue', 'fontSize': 24, 'text-align': 'center'})), ], justify="center", align="center"),
            dbc.Row([html.Center(html.P('EBITDA, or earnings before interest, taxes, depreciation, and amortization, is a measure of a companys overall financial performance and is used as an alternative to net income in some circumstances', style={
                     'color': 'black', 'fontSize': 24, 'text-align': 'center', 'width': '80em'})), ], justify="center", align="center"),
        ]),

    ])
])


app.layout = layout1


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@ app.callback(Output('cards', 'children'),
               [Input('ticker-input', 'value')])
def refresh_cards(ticker):
    ticker = ticker.upper()
    if ticker is None:
        TICKER = 'MSFT'
    else:
        TICKER = yf.Ticker(ticker)
    cards = [dbc.Col(make_card("Previous Close ", "secondary", TICKER.info['previousClose'])), dbc.Col(make_card("Open", "secondary", TICKER.info['open'])),
             dbc.Col(make_card("Sector", 'secondary', TICKER.info['sector'])), dbc.Col(
        make_card("Beta", 'secondary', TICKER.info['beta'])),
        dbc.Col(make_card("50d Avg Price", 'secondary', TICKER.info['fiftyDayAverage'])), dbc.Col(make_card("Avg 10d Vol", 'secondary',
                                                                                                            TICKER.info['averageVolume10days']))
    ]  # end cards list
    return cards


@ app.callback(Output('cards1', 'children'),
               [Input('ticker-input', 'value')])
def ratios(ticker):
    ratios = 'https://www.marketwatch.com/investing/stock/' + \
        ticker+'/company-profile?mod=mw_quote_tab'
    ratio_financials = BeautifulSoup(
        requests.get(ratios).text, "lxml")
    titlesfinancials = ratio_financials.findAll(
        'td', attrs={'class': 'table__cell w75'})
    pe = ''
    pricetobook = ''
    equity = ''
    enterprise = ''
    currentratio = ''
    for title in titlesfinancials:
        if 'P/E Current' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'table__cell w25'}):
                pe = td.text
        if 'Price to Book Ratio' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'table__cell w25'}):
                pricetobook = td.text
        if 'Return on Equity' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'table__cell w25'}):
                equity = td.text
        if 'Total Debt to Enterprise Value' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'table__cell w25'}):
                enterprise = td.text
        if 'Current Ratio' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'table__cell w25'}):
                currentratio = td.text
    cards1 = [dbc.Col(make_card("P/E Current ", "secondary", pe)), dbc.Col(make_card("Price to Book Ratio", "secondary", pricetobook)),
              dbc.Col(make_card("Total Debt to Enterprise Value", 'secondary', enterprise)), dbc.Col(
        make_card("Current Ratio", 'secondary', currentratio)), dbc.Col(make_card("Return on Equity ", "secondary", equity)), dbc.Col(make_card("Company Filings ", "secondary", html.A(ticker, href='https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ticker+'&Find=Search&owner=exclude&action=getcompany')))]
    return cards1


@ app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 4)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 4)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 4)],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


@ app.callback(Output('x-vol-1', 'children'),
               [Input('ticker-input', 'value'), Input('date-picker', 'start_date'), Input('date-picker', 'end_date'), Input('interval-component', 'n_intervals')
                ])
def create_graph(ticker, startdate, enddate, n):
    ticker = ticker.upper()
    df1 = yf.download(ticker, startdate, enddate)
    df1.reset_index(inplace=True)

    fig1 = go.Figure(data=[go.Candlestick(x=df1['Date'],
                                          open=df1['Open'], high=df1['High'],
                                          low=df1['Low'], close=df1['Close'])
                           ])

    df2 = yf.download(ticker,  period="5d", interval="1m")
    df2.reset_index(inplace=True)

    fig2 = go.Figure(data=[go.Candlestick(x=df2['Datetime'],
                                          open=df2['Open'], high=df2['High'],
                                          low=df2['Low'], close=df2['Close'])
                           ])

    df3 = yf.download(ticker,  period="1d", interval="1m")
    df3.reset_index(inplace=True)

    fig3 = go.Figure(data=[go.Candlestick(x=df3['Datetime'],
                                          open=df3['Open'], high=df3['High'],
                                          low=df3['Low'], close=df3['Close'])
                           ])

    accordion = html.Div([make_item("Daily Chart", dcc.Graph(figure=fig1), 1), make_item("5d 5m Chart", dcc.Graph(figure=fig2), 2), make_item("1d 1m Chart", dcc.Graph(figure=fig3), 3)
                          ], className="accordion")
    return accordion


# @ app.callback(
#     Output('tweets', 'children'),
#     [Input('interval-component2', 'n_intervals'),
#      ])
# def new_tweets(n):
#     get_options_flow()
#     return html.P(f"Reloaded Tweets {n}")


@ app.callback(
    Output('table-sorting-filtering', 'data'),
    [Input('table-sorting-filtering', "page_current"),
     Input('table-sorting-filtering', "page_size"),
     Input('table-sorting-filtering', 'sort_by'),
     Input('table-sorting-filtering', 'filter_query'),
     Input('refresh', 'n_clicks')])
def update_table(page_current, page_size, sort_by, filter, n_clicks):
    filtering_expressions = filter.split(' && ')

    if n_clicks is None:
        raise PreventUpdate
    else:
        dff = get_reddit()
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False)

        page = page_current
        size = page_size
        return dff.iloc[page * size: (page + 1) * size].to_dict('records')


@ app.callback(
    Output('table-sorting-filtering2', 'data'),
    [Input('table-sorting-filtering2', "page_current"),
     Input('table-sorting-filtering2', "page_size"),
     Input('table-sorting-filtering2', 'sort_by'),
     Input('table-sorting-filtering2', 'filter_query'),
     Input('interval-component', 'n_intervals')
     ])
def update_table2(page_current, page_size, sort_by, filter, n):
    filtering_expressions = filter.split(' && ')
    conn = sqlite3.connect('stocks.sqlite')
    flow = pd.read_sql(
        "select datetime, text, source from tweets order by datetime desc", conn)
    dff = flow

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

    if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
        # these operators match pandas series operator method names
        dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
    elif operator == 'contains':
        dff = dff.loc[dff[col_name].str.contains(filter_value)]
    elif operator == 'datestartswith':
        # this is a simplification of the front-end filtering logic,
        # only works with complete fields in standard format
        dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')


@ app.callback(Output('fin-table', 'children'),
               [Input('ticker-input', 'value')])
def fin_report(ticker):
    # ticker = ticker.upper()
    df = get_financial_report(ticker)
    # table = make_table('table-sorting-filtering3', df, '20px',8)
    table = dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True)
    return table


@ app.callback(
    Output('table-sorting-filtering3', 'data'),
    [Input('table-sorting-filtering3', "page_current"),
     Input('table-sorting-filtering3', "page_size"),
     Input('table-sorting-filtering3', 'sort_by'),
     Input('table-sorting-filtering3', 'filter_query'),
     Input('refresh1', 'n_clicks')])
def updatetable3(page_current, page_size, sort_by, filter, n_clicks):
    filtering_expressions = filter.split(' && ')

    if n_clicks is None:
        raise PreventUpdate
    else:
        scrn = get_screener('111')

        page = page_current
        size = page_size
        return scrn.iloc[page * size: (page + 1) * size].to_dict('records')
    # return scrn


@ app.callback(
    Output('table-sorting-filtering4', 'data'),
    [Input('table-sorting-filtering4', "page_current"),
     Input('table-sorting-filtering4', "page_size"),
     Input('table-sorting-filtering4', 'sort_by'),
     Input('table-sorting-filtering4', 'filter_query'),
     Input('refresh1', 'n_clicks')])
def updatetable4(page_current, page_size, sort_by, filter, n_clicks):
    filtering_expressions = filter.split(' && ')

    if n_clicks is None:
        raise PreventUpdate
    else:
        scrn = get_screener1('111')

        page = page_current
        size = page_size
        return scrn.iloc[page * size: (page + 1) * size].to_dict('records')


@ app.callback(
    Output('table-sorting-filtering5', 'data'),
    [Input('table-sorting-filtering5', "page_current"),
     Input('table-sorting-filtering5', "page_size"),
     Input('table-sorting-filtering5', 'sort_by'),
     Input('table-sorting-filtering5', 'filter_query'),
     Input('refresh1', 'n_clicks')])
def updatetable4(page_current, page_size, sort_by, filter, n_clicks):
    filtering_expressions = filter.split(' && ')

    if n_clicks is None:
        raise PreventUpdate
    else:
        scrn = get_screener2('111')

        page = page_current
        size = page_size
        return scrn.iloc[page * size: (page + 1) * size].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
