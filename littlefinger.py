import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# read Excel
excel = pd.ExcelFile('Money1.2.xlsx')

uk = excel.parse('UK')
us = excel.parse('US')

def tidyxacts(df):
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

def money_usd(df):
    """
    Format like money
    """
    df['Net'] = pd.to_string(df['Net'])
    df['Net'] = df['Net'].apply('${:,.2f}'.format)
    return df
    
def money_gbp(df):
    """
    Format like money
    """
    return "£{:,.2f}".format(x)
    
tidyxacts(uk)
add_date_info(uk)
tidyxacts(us)
add_date_info(us)


# Create Year/Month columns
uk['Year'], uk['Month'] = uk['Date'].dt.year, uk['Date'].dt.month
uk = uk.sort_values(by='Date')
uk.head()

"""
Weekly

    Top 10 expenses that week
    Balance of main accounts
    Week on week change
    Date of last update (or most recent transaction)

"""

# Account balance
ukacc = pd.pivot_table(uk,index=["Account"], values=["Net"],aggfunc=np.sum)
usacc = pd.pivot_table(us,index=["Account"], values=["Net"],aggfunc=np.sum)
# Combined in one table
result = pd.concat([ukacc, usacc])
print(result.sort_values(by='Net'))

# use cumsum to get running total
uk.Net.cumsum()

