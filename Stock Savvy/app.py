from flask import Flask, request, render_template, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import sqlite3
import numpy as np

app = Flask(__name__)

@app.route('/')
def welcompage():
    return render_template('welcompage.html')

@app.route('/stock_details')
def stock_details():
    return render_template('stock_details.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/get_stock_prices', methods=['POST'])
def get_stock_prices():
    name = request.form['stock_name']
    ed = datetime.today().strftime('%Y-%m-%d')
    sd = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    data = get_stock_data(name, sd, ed)
    if data is None:
        return {'error': 'Unable to fetch stock data'}
    stock_prices = [price for date, price in data.items()]
    return {'stock_data': data}

def Meanofdata(stock_prices):
    m1=np.mean(stock_prices)
    return {'mean_of_price':mean_price}

def get_stock_data(name, sd, ed):
    try:
        stock = yf.Ticker(name)
        history = stock.history(start=sd, end=ed)
        return history[['Close']].to_dict(orient='list')  
    except:
        return None

if __name__ == '__main__':
    app.run(debug=True)

