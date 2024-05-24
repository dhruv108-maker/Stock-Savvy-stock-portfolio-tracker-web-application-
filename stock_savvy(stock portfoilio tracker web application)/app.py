from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pymysql
import binascii

app = Flask(__name__)

host = "localhost"
user = "root"
password = "dhruv_100"
database = "users"

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1y")
        return hist
    except Exception as e:
        print("Error fetching data:", e)
        return None

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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Generate a unique token
        token = binascii.hexlify(os.urandom(24)).decode()

        try:
            # Establish a connection to the MySQL server
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )

            with connection.cursor() as cursor:
                print("Connected to MySQL")

                # Insert data into the table, excluding user_id since it is AUTO_INCREMENT
                sql_insert = "INSERT INTO users (username, email, password, token) VALUES (%s, %s, %s, %s)"
                data_to_insert = (username, email, password, token)
                cursor.execute(sql_insert, data_to_insert)

            # Commit the changes
            connection.commit()

            print("Data inserted successfully")

            # Send email with the tokenized link
            send_email(email, token)

        except pymysql.Error as e:
            print(f"Error: {e}")

        finally:
            if 'connection' in locals() and connection.open:
                connection.close()
                print("MySQL connection closed")
        name="Welcom "+name
    return render_template('index.html', name=username)

@app.route('/index2')#decoraters
def index2():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
    elif request.method == 'GET':
        symbol = request.args.get('symbol', '').upper()
    return render_template('index2.html')


@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
    elif request.method == 'GET':
        symbol = request.args.get('symbol', '').upper()
    data = get_stock_data(symbol)
    if data is not None:
        dates = data.index.strftime('%Y-%m-%d').tolist()
        prices = data['Close'].tolist()
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
        open_price=data['Close'].tolist()[-5]
        open_price="{:.2f}".format(open_price)
        return jsonify(success=True, dates=dates, prices=prices, latest_price=latest_price, pe=pe, highest_price=highest_price, open_price=open_price)
    else:
        return jsonify(success=False, error="Error fetching stock data",latest_price="101*", pe="101*")

if __name__ == '__main__':
    app.run(debug=True)
