import streamlit as st
import time
import requests
import json
import pandas as pd
import plotly.express as px
from dotenv import dotenv_values
from decouple import config
import calendar as cal
import datetime

config = dotenv_values(".env")
API_Key = config['API_Key']

ticker = st.sidebar.text_input("Ticker")
month = st.sidebar.selectbox("Month", ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
year = st.sidebar.selectbox("Year", (2021, 2020, 2019, 2018, 2017, 2016, 2015))
query = st.sidebar.button("Query")

def date_range(month, year):
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = datetime_object.month
    last_day_month = cal.monthrange(year, month_number)[1]
    first_day = str(year) + '-' + str(month_number).zfill(2) + '-01'
    last_day = str(year) + '-' + str(month_number).zfill(2) + '-' + str(last_day_month)
    return [first_day, last_day]


if query:
    url = 'https://www.alphavantage.co/query'
    params = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
          'symbol': ticker,
          'outputsize': 'full',
          'apikey': API_Key}
    r = requests.get(url, params = params)
    data = r.json()
    df = pd.DataFrame.from_dict(data['Time Series (Daily)']).T
    df.reset_index(inplace=True)
    df = df.rename(columns = {'index':'date'})
    df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')
    df['4. close'] = df['4. close'].astype(float)
    df['1. open'] = df['1. open'].astype(float)
    df['2. high'] = df['2. high'].astype(float)
    df['3. low'] = df['3. low'].astype(float)
    df['5. adjusted close'] = df['5. adjusted close'].astype(float)
    df['6. volume'] = df['6. volume'].astype(int)
    date_filter = date_range(month, year)
    df_filtered = df.loc[(df['date'] >= date_filter[0]) & (df['date'] <= date_filter[1])]
    chart_title = 'Closing Price for ' + str(ticker)
    fig = px.line(df_filtered, x="date", y="5. adjusted close", labels = {"date": "Date",
                        "5. adjusted close": "Adjusted Closing ($)"},title=chart_title)
    # fig.show()
    st.write(fig)

    query = False


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
