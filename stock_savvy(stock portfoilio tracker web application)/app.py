from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import yfinance as yf
from pymongo import MongoClient
import binascii
import pandas as pd
import csv
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

client = MongoClient("mongodb://localhost:27017/")
db = client['clients']
collection = db['client']

def get_stock_data(symbol, duration):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=duration)
        return hist
    except Exception as e:
        print("Error fetching data:", e)
        return None

def data():
    stock = pd.read_csv("stock_info.csv")
    symbols = stock['symbol'].tolist()
    return symbols

def namedata():
    stock_dict = {}
    stock = pd.read_csv("stock_info.csv")
    symbols = stock['symbol'].tolist()
    names = stock['Name'].tolist()
    stock_dict = {}
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Check if user already exists
    user = collection.find_one({"email": email})
    if user:
        flash("Email already registered. Please log in.")
        return redirect(url_for('index'))

    # Insert the new user document
    document = {
        "name": name,
        "email": email,
        "password": password
    }
    collection.insert_one(document)
    flash("Sign up successful.")
    return redirect(url_for('index'))

@app.route('/index2')#decoraters
def index2():
    symbols = data()
    stock_dict = namedata()
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
    elif request.method == 'GET':
        symbol = request.args.get('symbol', '').upper()
    return render_template('index2.html', symbols = symbols, stock_dict = stock_dict)

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        duration = request.form['duration']
    elif request.method == 'GET':
        symbol = request.args.get('symbol', '').upper()
        duration = request.args.get('duration', '1y')  # Default to 1 year if not provided
    
    data = get_stock_data(symbol, duration)
    if data is not None:
        dates = data.index.strftime('%Y-%m-%d').tolist()
        prices = data['Close'].tolist()
        compare_price = prices[-2]
        latest_price = data['Close'].tolist()[-1]
        if(latest_price<100):
            pe=latest_price/10
        elif(1000>latest_price>100):
            pe=latest_price/100
        elif(10000>latest_price>1000):
            pe=latest_price/1000
        latest_price="{:.2f}".format(latest_price)
        pe="{:.2f}".format(pe)
        highest_price="{:.2f}".format(max(prices))
        open_price=data['Close'].tolist()[-2]
        open_price="{:.2f}".format(open_price)
        return jsonify(success=True, dates=dates, prices=prices, latest_price=latest_price, pe=pe, highest_price=highest_price, open_price=open_price, compare_price=compare_price)
    else:
        return jsonify(success=False, error="Error fetching stock data",latest_price="101*", pe="101*")

if __name__ == '__main__':
    app.run(debug=True)


