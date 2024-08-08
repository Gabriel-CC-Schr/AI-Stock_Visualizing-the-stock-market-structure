import alpaca_trade_api as tradeapi
import pandas as pd
import time

# Your API credentials
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize the Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Define your trading strategy
def trading_strategy():
    # Get account information
    account = api.get_account()

    # Fetch the most recent bar data for a stock (e.g., AAPL)
    barset = api.get_barset('AAPL', 'minute', limit=1)
    aapl_bars = barset['AAPL']

    # Example: simple moving average strategy
    close_prices = [bar.c for bar in aapl_bars]
    sma = sum(close_prices) / len(close_prices)

    # Fetch the current price
    current_price = close_prices[-1]

    # Trading logic
    if current_price > sma:
        # Buy if the current price is above the SMA
        try:
            api.submit_order(
                symbol='AAPL',
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print("Buy order placed.")
        except Exception as e:
            print(f"Error placing buy order: {e}")

    elif current_price < sma:
        # Sell if the current price is below the SMA
        try:
            api.submit_order(
                symbol='AAPL',
                qty=1,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print("Sell order placed.")
        except Exception as e:
            print(f"Error placing sell order: {e}")

# Main loop to run the trading bot
while True:
    trading_strategy()
    time.sleep(60)  # Wait for 1 minute before running the strategy again
