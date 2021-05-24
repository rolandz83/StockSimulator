import requests

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

    def __str__(self):
        return "Bank account balance $" + str("{:.2f}".format(self.bank_account)) + " and You own {} shares".format(self.num_of_shares)

    def buy(self, shares, price):
        if shares * price > self.bank_account:
            print("Sorry not enough cash in your bank account.")
        else:
            self.bank_account -= shares * price
            self.num_of_shares += shares
            return True

    def sell(self, shares, price):
        if shares > self.num_of_shares:
            print("You dont have {} shares to sell".format(shares))
        else:
            self.bank_account += shares * price
            self.num_of_shares -= shares
            return True

def load_data():
    MYFUNCTION = "TIME_SERIES_DAILY" # "GLOBAL_QUOTE"
    MYKEY = "A7SW5BBTJ4PNLKAK"
    MYSYMBOL = "IBM"
    #print("NOT Making a request.!!!!!")
    #print("Data made up and sent.")
    #data = [('2021-04-12', 134.59), ('2021-04-13', 144.59), ('2021-04-14', 154.59), ('2021-04-15', 184.59), ('2021-04-16', 194.59)]
    #return data
    r = requests.get("https://www.alphavantage.co/query?function="+ MYFUNCTION +"&symbol=IBM&apikey=" + MYKEY)
    data = r.json()

    load_prices = []
    counter = 0
    for k , v in data["Time Series (Daily)"].items():
        load_prices.append((k, float(v["4. close"])))
        counter += 1
        if counter == 30:
            break
        print("Date: ", k ," price ", v["4. close"])

    print("Price Load complete... Lets play")
    load_prices.reverse()
    return load_prices
