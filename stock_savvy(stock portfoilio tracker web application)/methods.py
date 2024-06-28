import yfinance as yf
from pymongo import MongoClient
import pandas as pd

def get_stock_data(symbol, duration='1y'):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=duration)
        return hist
    except Exception as e:
        print("Error fetching data:", e)
        return None

def mean(prices):
    avg = sum(prices)/len(prices)
    return "{:.3f}".format(avg)

def correlation(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['date_ordinal'] = df['date'].apply(lambda x: x.toordinal())
    corr = df['date_ordinal'].corr(df['price'])
    return corr

def data():
    stock = pd.read_csv("stock_info.csv")
    symbols = stock['symbol'].tolist()
    return symbols

def namedata():
    stock_dict = {}
    stock = pd.read_csv("stock_info.csv")
    symbols = stock['symbol'].tolist()
    names = stock['Name'].tolist()
    for i in range(len(symbols)):
        stock_dict[names[i]] = symbols[i]
    return stock_dict

def get_stock_prices(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        prices = data['Close'].tolist()
        return prices
    except Exception as e:
        print("Error fetching stock prices:", e)
        return None

def get_current_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.history(period="1d")['Close'].iloc[-1]  # Get the last closing price
        return current_price
    except Exception as e:
        print("Error fetching data:", e)
        return None

def mean(prices):
    return sum(prices) / len(prices)

