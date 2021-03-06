import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import AlphaVantageAPI as Trade

win = tk.Tk()
win.title("Stock Simulator")
win.geometry("540x330")

trader = Trade.DayTrader()

stock_price_intvar = tk.StringVar()
stock_price_intvar.set("$---")

stock_num_input = tk.StringVar(value="1")

def nextday():
    if day_var['text'] == 29:
        account_total = trader.bank_account + trader.num_of_shares * trader.getTodaysPrice(trader.day_counter-1)
        if account_total < 10000:
            tk.messagebox.showinfo("Game Over", """Day 30 reached.
                                    Your total account worth is ${:.2f}
                                    You lost some $$$ dont play the stock market it isn't for you!
                                   """.format(account_total))
        else:
            tk.messagebox.showinfo("Game Over", """Day 30 reached.
                                   Your total account worth is ${:.2f}
                                   You Won! now go play on the real stock market, You're good at this!
                                   """.format(account_total))
    else:
        trader.day_counter += 1
        day_var['text'] = trader.day_counter
        stock_price_intvar.set("${:.2f}".format(trader.getTodaysPrice(trader.day_counter)))
        date_var['text'] = trader.getTodaysDate(trader.day_counter)

def buy():
    if stock_num_input.get() != "0":
        if trader.buy(int(stock_num_input.get()), trader.getTodaysPrice(trader.day_counter-1)): #Returns false if transaction fails.
            acc_var['text'] = "${:.2f}".format(trader.bank_account)
            shares_var['text'] = trader.num_of_shares
            trans_history.insert(tk.END, "Day#:{} = Bought {} of shares @ ${} \n".format(trader.day_counter, stock_num_input.get(), trader.getTodaysPrice(trader.day_counter-1)))
            nextday()
        else:
            tk.messagebox.showwarning("Not Enough funds!", "Sorry, You dont have enough cash to complete this transaction.")
    else:
        tk.messagebox.showwarning("Invalid transaction", """You can't buy "zero" shares""")

def sell():
    if stock_num_input.get() != "0":
        if trader.sell(int(stock_num_input.get()),trader.getTodaysPrice(trader.day_counter-1)):
            acc_var['text'] = "${:.2f}".format(trader.bank_account)
            shares_var['text'] = trader.num_of_shares
            trans_history.insert(tk.END, "Day#:{} = Sold {} of shares @ ${} \n".format(trader.day_counter, stock_num_input.get(), trader.getTodaysPrice(trader.day_counter-1)))
            nextday()
        else:
            tk.messagebox.showwarning("Not Enough Shares!", "Sorry, You dont have enough shares to complete this transaction.")
    else:
        tk.messagebox.showwarning("Invalid transaction", """You can't buy "zero" shares""")

def hold():
    nextday()

def about():
    tk.messagebox.showinfo("About", "Stock Simulator App Version 3.0.1 \n by Roland Zeren")

def load():
    if stock_var['text'] != '':
        trader.load_data(stock_var['text'])
        buy_bt.configure(state="active")
        sell_bt.configure(state="active")
        hold_bt.configure(state="active")
        max_bt.configure(state="active")
        stock_price_intvar.set("${:.2f}".format(trader.getTodaysPrice(trader.day_counter)))
        date_var['text'] = trader.getTodaysDate(trader.day_counter)
        #sub_menu_file.entryconfig('Load', state=tk.DISABLED)
    else:
        tk.messagebox.showinfo("Load Error", "Stock Symbol not selected, please go to File > Settings to pick a stock symbol to load.")

def check(event, myEntry, myListBox):
    searchTerm = myEntry.get()
    if searchTerm == '':
        myListBox.delete(0, tk.END)
    else:
        if len(searchTerm) > 2:
            results = []
            for stock in trader.stockSearch(searchTerm):
                if searchTerm.lower() in stock.lower():
                    results.append(stock)
            updateSearchList(myListBox, results)

def fillout(event, myEntry, myListBox):  #listbox event.
    myEntry.delete(0, tk.END)
    myEntry.insert(0, myListBox.get(tk.ANCHOR))

def updateSearchList(myListBox, data): #update listbox
    myListBox.delete(0, tk.END)
    for item in data:
        myListBox.insert(tk.END, item)

def applyChanges(label, symbol):
    label['text'] = symbol

def settings(stock_var):
    childSettingWin = tk.Toplevel(win)
    childSettingWin.geometry("400x300")
    childSettingWin.title("Settings")
    label_child = tk.Label(childSettingWin, text="Please enter the stock symbol or description")
    label_child.pack(pady=10)

    stockSearchEntry = tk.Entry(childSettingWin)
    stockSearchEntry.pack()

    searchResultList = tk.Listbox(childSettingWin, width=60)
    searchResultList.pack(pady=10)

    applyButton = tk.Button(childSettingWin, text="Apply", command=lambda : applyChanges(stock_var, stockSearchEntry.get().split(" - ")[0]))
    applyButton.pack()

    okButton = tk.Button(childSettingWin, text="OK", command=childSettingWin.destroy)
    okButton.pack()

    searchResultList.bind("<<ListboxSelect>>", lambda e, entry=stockSearchEntry, list=searchResultList : fillout(entry, entry, list))

    stockSearchEntry.bind("<KeyRelease>", lambda e, entry=stockSearchEntry, list=searchResultList : check(entry, entry, list))

main_menu = tk.Menu(win)
win.config(menu=main_menu)

sub_menu_file = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", underline=0, menu=sub_menu_file)

sub_menu_file.add_command(label="Load", underline=0, command=load)
sub_menu_file.add_command(label="Settings", underline=0, command=lambda:settings(stock_var))
sub_menu_file.add_separator()
sub_menu_file.add_command(label="Exit", underline=0, command=win.destroy)

sub_menu_about = tk.Menu(main_menu)
main_menu.add_command(label="About", command=about)



acc_bal_label = tk.Label(win, text="Account Balance: ", width=16, anchor='w', bg='gray')
acc_var = tk.Label(win, text="${:.2f}".format(trader.bank_account))

shares_label = tk.Label(win, text="Shares on hand:",  width=16, anchor='w', bg='gray')
shares_var = tk.Label(win, text=trader.num_of_shares)

day_label = tk.Label(win, text="Trading Day:",  width=16, anchor='w', bg='gray')
day_var = tk.Label(win, text="0")

stock_label = tk.Label(win, text="Stock Symbol: ", width=18, anchor='w', bg='green')
stock_var = tk.Label(win, text='')
stock_price_label = tk.Label(win, text="Stock Price: ", width=18, anchor='w', bg='green')
stock_price_var = tk.Label(win, textvariable=stock_price_intvar)
date_label = tk.Label(win, text="Date: ", width=18, anchor='w', bg='green')
date_var = tk.Label(win, text="--/--/--")

buy_bt = tk.Button(win, text="Buy", state="disabled", command=buy)
sell_bt = tk.Button(win, text="Sell", state="disabled", command=sell)
hold_bt = tk.Button(win, text="Hold", state="disabled", command=hold)
max_bt = tk.Button(win, text="Max", state="disabled", justify=tk.LEFT, command=lambda:stock_num_input.set(int(trader.bank_account / trader.getTodaysPrice(trader.day_counter-1))))

trans_history = tk.scrolledtext.ScrolledText(win, height=10, width=60)

def test_Var(entry_value, acttion_type):
    if acttion_type == '1': #inster detected
        if not entry_value.isdigit():
            return False  #entry denied
        return True
    if acttion_type == '0': #deleting accured
        return True
    if acttion_type == '-1': #when var is changed by set()
        return True

user_input = tk.Entry(win, width=5, validate='key', textvariable=stock_num_input)
user_input.configure(validatecommand=(win.register(test_Var), '%P', '%d'))

acc_bal_label.grid(column=0, row=0, columnspan=2,  padx=10, pady=(10,0))
acc_var.grid(column=2, row=0)
shares_label.grid(column=0, row=1, columnspan=2, padx=10)
shares_var.grid(column=2, row=1)
day_label.grid(column=0, row=2, columnspan=2, padx=10)
day_var.grid(column=2, row=2)
stock_label.grid(column=5, row=0, columnspan=2, pady=(10,0))
stock_var.grid(column=7, row=0)
stock_price_label.grid(column=5, row=1, columnspan=2)
stock_price_var.grid(column=7, row=1)
date_label.grid(column=5, row=2, columnspan=2)
date_var.grid(column=7, row=2)
max_bt.grid(column=5, row=3, pady=10)
trans_history.grid(row=5, column=0, columnspan=8, padx=10, pady=10)

buy_bt.grid(column=0, row=4, padx=10)
sell_bt.grid(column=1, row=4, padx=10)
hold_bt.grid(column=2, row=4, padx=10)
user_input.grid(column=4, row=3, pady=10)

if __name__ == '__main__':
    win.mainloop()
