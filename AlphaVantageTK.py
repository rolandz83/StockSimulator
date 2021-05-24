import tkinter as tk
from tkinter import messagebox
import AlphaVantageAPI as Trade

win = tk.Tk()
win.title("IBM Stock Simulator")
win.geometry("600x350")

trader = Trade.DayTrader()

stock_price_intvar = tk.StringVar()
stock_price_intvar.set("$---")

stock_num_input = tk.StringVar(value="1")

def nextday():
    if day_var['text'] == 30:
        tk.messagebox.showinfo("Game Over", "Day 30 reached.")
    else:
        trader.day_counter += 1
        day_var['text'] = trader.day_counter
        stock_price_intvar.set("$" + str(data[trader.day_counter-1][1]))
        date_var['text'] = data[trader.day_counter-1][0]

def buy():
    if trader.buy(int(stock_num_input.get()),data[trader.day_counter-1][1]): #Returns false if transaction fails.
        acc_var['text'] = "$" + "{:.2f}".format(trader.bank_account)
        shares_var['text'] = trader.num_of_shares
        nextday()
    else:
        tk.messagebox.showwarning("Not Enough funds!", "Sorry, You dont have enough cash to complete this transaction.")

def sell():
    if trader.sell(int(stock_num_input.get()),data[trader.day_counter-1][1]):
        acc_var['text'] = "$" + "{:.2f}".format(trader.bank_account)
        shares_var['text'] = trader.num_of_shares
        nextday()
    else:
        tk.messagebox.showwarning("Not Enough Shares!", "Sorry, You dont have enough shares to complete this transaction.")

def hold():
    nextday()

def load():
    global data
    data = Trade.load_data()
    buy_bt.configure(state="active")
    sell_bt.configure(state="active")
    hold_bt.configure(state="active")
    stock_price_intvar.set("$" + str(data[trader.day_counter][1]))
    date_var['text'] = data[trader.day_counter][0]
    nextday()
    load_bt.configure(state="disabled")

emptyspace = tk.Label(win, borderwidth=5, text="       ")

acc_bal_label = tk.Label(win, text="Account Balance: ", width=20, anchor='w', bg='gray')
acc_var = tk.Label(win, text="$" + "{:.2f}".format(trader.bank_account))

shares_label = tk.Label(win, text="Shares on hand:",  width=20, anchor='w', bg='gray')
shares_var = tk.Label(win, text=trader.num_of_shares)

day_label = tk.Label(win, text="Trading Day:",  width=20, anchor='w', bg='gray')
day_var = tk.Label(win, text="0")

stock_label = tk.Label(win, text="Stock Symbol: ")
stock_var = tk.Label(win, text="IBM")
stock_price_label = tk.Label(win, text="Stock Price: ")
stock_price_var = tk.Label(win, textvariable=stock_price_intvar)
date_label = tk.Label(win, text="Date: ")
date_var = tk.Label(win, text="date-variable")

buy_bt = tk.Button(win, text="Buy", state="disabled", command=buy)
sell_bt = tk.Button(win, text="Sell", state="disabled", command=sell)
hold_bt = tk.Button(win, text="Hold", state="disabled", command=hold)
quit_bt = tk.Button(win, text="Quit", command=win.destroy)
load_bt = tk.Button(win, text="Load Data", command=load)

def test_Var(entry_value, acttion_type):
    print("Value: ", entry_value)
    if acttion_type == '1': #inster detected
        if not entry_value.isdigit():
            print("false")
            return False  #entry denied
        return True
    if acttion_type == '0': #deleting accured
        print("Deleted")
        return True
    if acttion_type == '-1':
        print("something else happeened")

user_input = tk.Entry(win, width=5, validate='key', textvariable=stock_num_input)
user_input.configure(validatecommand=(win.register(test_Var), '%P', '%d'))

acc_bal_label.grid(column=0, row=0, columnspan=2)
acc_var.grid(column=2, row=0)
shares_label.grid(column=0, row=1, columnspan=2)
shares_var.grid(column=2, row=1)
day_label.grid(column=0, row=2, columnspan=2)
day_var.grid(column=2, row=2)
stock_label.grid(column=8, row=0, columnspan=2)
stock_var.grid(column=10, row=0)
stock_price_label.grid(column=8, row=1, columnspan=2)
stock_price_var.grid(column=10, row=1)
date_label.grid(column=8, row=2, columnspan=2)
date_var.grid(column=10, row=2)

emptyspace.grid(column=0, row=3, columnspan=5, pady=30)

buy_bt.grid(column=0, row=4, padx=10, pady=10)
sell_bt.grid(column=1, row=4, padx=10, pady=10)
hold_bt.grid(column=2, row=4, padx=10, pady=10)
quit_bt.grid(column=3, row=4, padx=10, pady=10)
load_bt.grid(column=5, row=1)
user_input.grid(column=5, row=3)

win.mainloop()
