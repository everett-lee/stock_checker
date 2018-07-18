import datetime
import requests
import json
import pandas as pd
import numpy

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#get dates and deltas
today = datetime.datetime.now()
time_delta_week = datetime.timedelta(days = 7)
time_delta_year = datetime.timedelta(days = 365)
last_week = today - time_delta_week
last_year = today - time_delta_year
str_today = today.strftime("%Y-%m-%d")
str_last_week = last_week.strftime("%Y-%m-%d")
str_last_year = last_year.strftime("%Y-%m-%d")

#format dates
years = mdates.YearLocator()
months = mdates.MonthLocator()
months_format = mdates.DateFormatter("%b")
years_format = mdates.DateFormatter("\n\n%Y")

key = "XXXXXXXXXXX"
stocks = {"AAPL": 100, "MSFT": 42, "TSLA": 50}

def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def save_text_to_html(symbol, latest_price, current_profit, yearly_max, weekly_max, count):
    html_body = """
    <body>
        <h1 style="color:#007399; font-family:arial"> %s </h1>
        <div style="color:#007399; font-family:arial">
          <p> Price: $%s</p>
          <p> Profit/loss: $%s</p>
          <p> Weekly max: $%s</p>
          <p> Yearly max: $%s</p>
        </div>
        <div style="color:#007399; font-family:arial">
            <img src="cid:image%s">
        </div>    
    </body>
    """ %(symbol, latest_price, current_profit, weekly_max, yearly_max, count)
    output_html = open("stock_data.html", "a")
    output_html.write(html_body)
    output_html.close()

 def pull_data()
    #create output file
    output_html = open("stock_data.html", "w")
    output_html.close()
    count = 1
    for symbol, purchase_price in stocks.items():
        
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=" + key   
        stock_data = get_json(url)

        if len(stock_data) == 1:
            print("Stock not found")
        
        else:

            df = pd.DataFrame.from_dict(stock_data["Time Series (Daily)"],
                                           orient="index",
                                           )

            df.columns = ["Open", "High", "Low", "Close", "Adjusted close", "Volume", "Dividend", "Split coefficient"]
            
            # converts column values to numeric type
            df = df.apply(pd.to_numeric)
            
            df["Rolling mean"] = df["Close"].rolling(window=4).mean()

            # gets latest price and profit
            latest_date = df.index[-1]
            latest_data = df.ix[latest_date]
            latest_price = latest_data["Close"]
            current_profit = str(round(latest_price - purchase_price, 2))

            past_week = df.loc[str_last_week:str_today]
            past_year = df.loc[str_last_year:str_today]
            yearly_max = past_year["Close"].max()
            weekly_max = past_week["Close"].max()

            fig, ax = plt.subplots()
            close = ax.plot(pd.to_datetime(past_year.index), past_year["Close"])
            rolling_mean = ax.plot(pd.to_datetime(past_year.index), past_year["Rolling mean"])
            
            #format axes    
            ax.xaxis.set_minor_locator(months)
            ax.xaxis.set_minor_formatter(months_format)
            ax.xaxis.set_major_locator(years)
            ax.xaxis.set_major_formatter(years_format)
            plt.legend(handles=[close[0], rolling_mean[0]])
            plt.title(symbol)
            plt.ylabel("Close($)")
            plt.savefig("%s.png" %(symbol))

            save_text_to_html(symbol, latest_price, current_profit, yearly_max, weekly_max, count
                              )
            count += 1
