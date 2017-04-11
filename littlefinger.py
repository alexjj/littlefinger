# -*- coding: utf-8 -*-
"""
Littlefinger

Performing calculations on personal financial transactions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.parser import parse
import seaborn as sns
import matplotlib.pyplot as plt


# Useful timeranges
now = datetime.now()
weekago = now - timedelta(7)

def tidyxacts(df):
    """
    Fix formats of columns for transactions in dataframe df

    Parameters
    ----------
    df : Dataframe

    Returns
    -------

      Date formatted as Date
      Amounts as numeric
      Top and sub level categories as category
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df['Inflow'] = pd.to_numeric(df['Inflow'])
    df['Outflow'] = pd.to_numeric(df['Outflow'])
    df['Net'] = pd.to_numeric(df['Net'])
    df['Master Category'] = df['Master Category'].astype("category")
    df['Sub Category'] = df['Sub Category'].astype("category")


def add_date_info(df):
    """
    Adds columns for year, month, quarter, week number
    """
    df['Year'], df['Month'] = df['Date'].dt.year, df['Date'].dt.month
    df['Quarter'], df['Week'] = df['Date'].dt.quarter, df['Date'].dt.week


def top10expenses(df, starttime, endtime):
    """
    Returns top 10 expenses between dates. 
    
    Makes a smaller list of relevant columns and filters df.
    
    TODO
    ----
    
      Add categorical listing to expense/income to avoid showing income
    
    """
    cols = ['Account', 'Date', 'Payee', 'Master Category', 'Sub Category',
            'Outflow']
    df2 = df[cols]
    filtered = df2[(df2['Date'] >= starttime) & (df2['Date'] <= endtime)]
    return filtered.sort_values(by='Outflow', ascending=False).head(10)


def dateindex(df):
    """
    Returns df with index as date column
    """
    return df.set_index(['Date'])


def account_balances(df):
    """
    Returns current account balances
    """

    return pd.pivot_table(df, index=["Account"], values=["Net"],
                          aggfunc=np.sum).sort_values(by='Net')


def annualspends(df):
    """
    Returns pivot table by year and master category.
    """
    return pd.pivot_table(uk, index=['Year', 'Master Category'],
                          values=["Net"], aggfunc=np.sum)


"""
def money(x):
    return "${:,.0f}".format(x)

formatted_df = df_sub.applymap(money)
formatted_df
"""


# Each account's balance
def accounttrend(df):
    """
    Plot running total of each account over all time
    """
    grouped = df['Net'].groupby(df['Account'])
    for account, net in grouped:
        print(account)
        net.cumsum().plot()

def funds_net_worth():
    """
    This function calculates the net worth of each fund over time, plots it
    and calculates the total
    """
    funds = excel.parse('Investments')
    prices = excel.parse('Funds')
    dateindex(prices)
    dateindex(funds)
    
    # Prices at point of purchase
    purchase_prices = funds.pivot(index='Date', columns='Company Code', 
                                  values='Price (GBP)')
    # Price Table
    # TODO - import from somewhere
    price_table = prices.pivot(index='Date', columns='Fund',values='Price')
    
    # Join prices
    all_prices = pd.concat([price_table, purchase_prices]).sort_index()
    all_prices.fillna(method='ffill', inplace=True)
    
    # Cumulative Amount of Funds
    fund_table = pd.pivot_table(funds, values=['Quantity'], aggfunc=np.sum, 
        index=['Date'], columns=['Company Code'], fill_value=0).cumsum()

# Open Excel and parse worksheets

excel = pd.ExcelFile("~\python\Money1.2.xlsx")
uk = excel.parse('UK')
us = excel.parse('US')
tidyxacts(uk)
add_date_info(uk)
tidyxacts(us)
add_date_info(us)


