import pandas as pd
import numpy as np
import datetime as dt
def some():
    print ("hello")

def get_funds(list_of_funds, start_date = "1990-01-01", end_date = dt.date.today()):
    sheet_id = '1fo3B5bkkZxI9q6eqiqnlmWb3hcNcpBwatQnXj-f59rc'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet="
    #generate urls
    urls = {}
    for item in list_of_funds:
        urls[item] = url + item

    data = {}
    for k, v in urls.items():
        data[k] = pd.read_csv(v, usecols=["Date", "Price"]).squeeze()

    series_of_datetime = {}
    for k, v  in data.items():
        series_of_datetime[k] = pd.to_datetime(v["Date"], dayfirst=True)

    series_of_price = {}
    for k, v  in data.items():
        series_of_price[k] = v["Price"].str.replace(",", ".", regex=False).astype(float)

    merged_series = {}
    iter = series_of_datetime.keys()
    for item in iter:
        merged_series[item] = pd.Series(series_of_price[item].values, index=series_of_datetime[item].values, name=item)

    df = pd.DataFrame( index=np.arange(start_date, end_date, dtype='datetime64[D]'))
    new_df = pd.DataFrame()
    for k, v in merged_series.items():
        df = df.merge(v, how="left", right_index=True, left_index=True)

    return df

def get_currency(list_of_currency):
    start_date = "19960902" #start of monetary reform
    end_date = dt.date.today().strftime("%Y%m%d")
    data = {}
    for currency_code in list_of_currency:
        url = f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={start_date}&end={end_date}&valcode={currency_code}&sort=exchangedate&order=desc&json"
        data[currency_code] = pd.read_json(url, convert_dates=['exchangedate'])

    for k, v in data.items():
        data[k] = pd.Series(v["rate_per_unit"].values, index= v["exchangedate"].values, name=k)
    
    df = pd.DataFrame( index=np.arange("1990-01-01", dt.date.today().strftime("%Y-%m-%d"), dtype='datetime64[D]'))
    for k in data.keys():
        df = df.merge(data[k], how="left", right_index=True, left_index=True)

    return df
