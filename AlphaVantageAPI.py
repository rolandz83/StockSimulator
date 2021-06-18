import requests
import os
'''
Simple stock simulator:
Game simulates real stock market data provided by Alpha Vantage
API key can be obtained freely please use your own key on their web site
https://www.alphavantage.co/documentation/

This is the second version of this game, first version was text based.
New version features GUI using Tkinter library. I focused on functinality,
cosmetics was not priority therefore excuse the apearance.

Current version is hardcoded to request past 30 days of IBM stock data.
Futere versions will provide ability to use different stock options and
timeframes.

AlphaVantageAPI.py is the code making the request and running the simulation
AlphaVantageTK.py is the main app with GUI.

Enjoy.
'''

class DayTrader:
    def __init__(self):
        self.bank_account = 10000
        self.num_of_shares = 0
        self.day_counter = 0
        self.__marketData = []

    def __str__(self):
        return "Bank account balance $" + str("{:.2f}".format(self.bank_account)) + " and You own {} shares".format(self.num_of_shares)

    def buy(self, shares, price):
        if shares * price > self.bank_account:
            print("Sorry not enough cash in your bank account.")
            return False
        else:
            self.bank_account -= shares * price
            self.num_of_shares += shares
            return True

    def sell(self, shares, price):
        if shares > self.num_of_shares:
            print("You dont have {} shares to sell".format(shares))
            return False
        else:
            self.bank_account += shares * price
            self.num_of_shares -= shares
            return True

    def load_data(self, stockSymbol):
        MYFUNCTION = "TIME_SERIES_DAILY" # "GLOBAL_QUOTE"
        MYKEY = os.environ.get('MY_AVAPI_KEY')
        MYSYMBOL = stockSymbol
        r = requests.get("https://www.alphavantage.co/query?function="+ MYFUNCTION +"&symbol="+ MYSYMBOL + "&apikey=" + MYKEY)
        data = r.json()
        counter = 0
        for k , v in data["Time Series (Daily)"].items():
            self.__marketData.append((k, float(v["4. close"])))
            counter += 1
            if counter == 30:
                break
        self.__marketData.reverse()

    def getTodaysPrice(self, day):
        return self.__marketData[day][1]

    def getTodaysDate(self, day):
        return self.__marketData[day][0]

    def stockSearch(self, keyword):
        MYFUNCTION = "SYMBOL_SEARCH"
        MYKEY = os.environ.get('MY_AVAPI_KEY')
        r = requests.get("https://www.alphavantage.co/query?function="+ MYFUNCTION +"&keywords="+ keyword + "&apikey=" + MYKEY)
        data = r.json()
        searchResults = []
        for stock in data["bestMatches"]:
            searchResults.append(stock["1. symbol"] + " - " + stock["2. name"])
        return searchResults
