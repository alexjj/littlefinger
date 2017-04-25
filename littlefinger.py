# -*- coding: utf-8 -*-
"""
Littlefinger

Performing calculations on personal financial transactions

Reports:
  

"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.parser import parse
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.tseries.offsets import *


pd.set_option('float_format', '{:.2f}'.format)
plt.style.use('seaborn-colorblind')

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
      Adds columns for year, month, quarter, week number
      Sets date as index
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df['Inflow'] = pd.to_numeric(df['Inflow'])
    df['Outflow'] = pd.to_numeric(df['Outflow'])
    df['Net'] = pd.to_numeric(df['Net'])
    # df['Master Category'] = df['Master Category'].astype("category")
    # df['Sub Category'] = df['Sub Category'].astype("category")
    # df['Year'], df['Month'] = df['Date'].dt.year, df['Date'].dt.strftime('%b')
    df['Year'], df['Month'] = df['Date'].dt.year, df['Date'].dt.month
    df['Quarter'], df['Week'] = df['Date'].dt.quarter, df['Date'].dt.week
    df.set_index(['Date'], inplace=True)


def add_date_info(df):
    """
    Adds columns for year, month, quarter, week number
    """
    df['Year'], df['Month'] = df['Date'].dt.year, df['Date'].dt.strftime('%b')
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
            'Outflow', 'Type']
    df2 = df[cols]
    filtered = df2[(df2['Date'] >= starttime) & (df2['Date'] <= endtime) & 
                   df['Type'] == 'Expense']
    return filtered.sort_values(by='Outflow', ascending=False).head(10)


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
    return pd.pivot_table(uk, index=['Master Category'], columns=['Year'],
                          values=["Net"], aggfunc=np.sum)


# Each account's balance
def accounttrend(df):
    """
    Plot running total of each account over all time
    """
    plt.figure()

    grouped = df['Net'].groupby(df['Account'])
    for account, net in grouped:
        net.cumsum().plot(label=account, legend=True)


def funds_net_worth():
    """
    This function calculates the net worth of each fund over time, plots it
    and calculates the total
    """
    funds = excel.parse('Investments')
    prices = excel.parse('Funds')
    funds.set_index(['Date'], inplace=True)
    prices.set_index(['Date'], inplace=True)

    # Prices at point of purchase
    purchase_prices = funds.pivot(index='Date', columns='Company Code',
                                  values='Price (GBP)')
    # Price Table
    # TODO - import from somewhere
    price_table = prices.pivot(index='Date', columns='Fund', values='Price')

    # Join prices
    all_prices = pd.concat([price_table, purchase_prices]).sort_index()
    all_prices.fillna(method='ffill', inplace=True)

    # Cumulative Amount of Funds
    fund_table = pd.pivot_table(funds, values=['Quantity'], aggfunc=np.sum,
                                index=['Date'], columns=['Company Code'],
                                fill_value=0).cumsum()

    return all_prices, fund_table


def xact_type(df):
    """
    Adds transfer, expense, income category column to df
    """
    def categorise(row):
        if row['Master Category'] == "Transfer":
            return 'Transfer'
        if row['Master Category'] == "Income":
            return 'Income'
        return 'Expense'

    df['Type'] = df.apply(lambda row: categorise(row), axis=1)

"""
Extra things to play with

Groupby:

grouped = df.groupby(lambda x: x.year)
for year, group in grouped:
   ....:     print (year)
   ....:     print (group)

usexpenses = us.query('Type == ["Expense"]')

Last month date
lastmonth = now - DateOffset(months=1)
filter = str(lastmonth.year) + "-" + str(lastmonth.month)
df[filter]



Plot expenses graph:
    usexpenses = us.query('Type == ["Expense"]').copy()
    usexpenses.Net = usexpenses.Net * -1
    usexpenses.groupby('Master Category')['Net'].sum().plot(kind="bar") ; plt.axhline(0, color='k')


Graph of stacked subcategoryies per master category
usexpenses.groupby(['Master Category', 'Sub Category'])['Net'].sum().unstack().plot(kind='bar', stacked=True)

summary = pd.pivot_table(us['2017'], index=['Master Category'], columns=['Month'], values=['Net'], aggfunc=np.sum, fill_value=0)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

summary.columns = months[:now.month] # Renames to months based off current month
summary.loc['Total']= summary.sum() # adds total row at bottom
"""



def monthly_pivot(df):
    pass

# Open Excel and parse worksheets

excel = pd.ExcelFile("C:\\Users\\aowd\OneDrive - Chevron\\Special Projects\\littlefinger\\Money1.2.xlsx")
uk = excel.parse('UK')
us = excel.parse('US')
tidyxacts(uk)
tidyxacts(us)
xact_type(uk)
xact_type(us)


def all_gbp_transactions():
    # Creating GBP only table
    forex = excel.parse('Forex')
    forex.set_index(['Date'], inplace=True) # Set date to be index
    forex = forex['Exchange Rate'] # Only keep exchange column
    usex =  us.join(other=forex, how='outer')
    usex['Exchange Rate'].fillna(method='ffill', inplace=True)
    usex['Net GBP'] = usex['Net'] / usex['Exchange Rate']
    usgbp = usex.drop(['Net', 'Exchange Rate'], axis=1)
    usgbp.rename(columns={'Net GBP':'Net'}, inplace=True)
    allgbp = pd.concat([uk, usgbp], axis=0)
    return allgbp
