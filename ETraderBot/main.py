import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# E*Trade credentials
ETRADE_API_KEY = '5109a97aec4548ac21a4c0cd80b1f2d9'
ETRADE_API_SECRET = 'c033d24362c344de6ee38162bfc0d86857b8cd2c44e5887c717931378ac221f2'
ETRADE_ACCESS_TOKEN = 'your_etrade_access_token'
ETRADE_ACCESS_TOKEN_SECRET = 'your_etrade_access_token_secret'

# Google Sheets credentials
GOOGLE_SHEET_CREDS_FILE = '/Users/elizabethgarcia/Documents/ETraderBot/stocktradingproject-7153c47c293e.json'
GOOGLE_SHEET_NAME = 'https://docs.google.com/spreadsheets/d/1WPv4K7GNxwX8HnwXfTvAwCwI19hsQVAZ2ARSNxufoy4/edit#gid=35094487'

# Function to get screener data from Simfin
def get_screener_data():
    # Implement code to fetch screener data from Simfin
    pass

# Function to get price data from financialmodelingprep
def get_price_data():
    # Implement code to fetch price data from financialmodelingprep
    pass

# Function to authenticate and connect to Google Sheets
def connect_to_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEET_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    return sheet

# Function to add new tickers to Google Sheets for approval
def add_ticker_to_sheet(sheet, ticker):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append_row([timestamp, ticker])

# Function to trade using E*Trade
def trade(ticker, action, quantity):
    # Implement code to execute trades using E*Trade API
    pass

# Main function
def main():
    # Get screener data from Simfin
    screener_data = get_screener_data()

    # Get price data from financialmodelingprep
    price_data = get_price_data()

    # Connect to Google Sheets
    sheet = connect_to_google_sheets()

    # Iterate through screener data
    for stock in screener_data:
        ticker = stock['ticker']
        # Check if the ticker is already in Google Sheets
        if ticker not in [row[1] for row in sheet.get_all_values()]:
            # Add the new ticker to Google Sheets for approval
            add_ticker_to_sheet(sheet, ticker)
        else:
            # Check if the fundamentals look good but notify for approval
            if stock['fundamentals'] == 'good' and stock['fraud'] == 'potential':
                # Notify for approval
                print(f"New ticker {ticker} with potential fraud. Please approve.")

    # Implement trading logic based on screener and price data
    # For example:
    # trade('AAPL', 'buy', 10)

if __name__ == "__main__":
    main()
