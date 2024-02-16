import gspread
import requests
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from datetime import datetime
from gspread.exceptions import SpreadsheetNotFound  # Import SpreadsheetNotFound explicitly

# Google Sheets credentials
GOOGLE_SHEET_CREDS_FILE = '/Users/elizabethgarcia/Documents/ETraderBot/stocktradingproject-7153c47c293e.json'
GOOGLE_SHEET_NAME = 'Test'

# Function to get screener data from Simfin
def get_screener_data():
    # Example implementation fetching screener data from Simfin
    # Replace this with your actual implementation
    screener_data = [
        {'ticker': 'AAPL', 'fundamentals': 'good', 'fraud': 'potential'},
        {'ticker': 'GOOG', 'fundamentals': 'good', 'fraud': 'potential'},
        {'ticker': 'MSFT', 'fundamentals': 'good', 'fraud': 'potential'},
    ]
    return screener_data

# Function to get price data from financialmodelingprep
def get_price_data(tickers):
    price_data = {}
    for ticker in tickers:
        url = f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'price' in data:
                price_data[ticker] = data['price']
            else:
                print(f"No price data available for {ticker}.")
                price_data[ticker] = None
        else:
            print(f"Failed to fetch price data for {ticker}. Status code: {response.status_code}")
            price_data[ticker] = None
    return price_data

GOOGLE_SHEET_ID = '1WPv4K7GNxwX8HnwXfTvAwCwI19hsQVAZ2ARSNxufoy4'
# Function to authenticate and connect to Google Sheets
def connect_to_google_sheets(tab_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_service_account_file(GOOGLE_SHEET_CREDS_FILE, scopes=scope)
    # print("Credentials:", creds)  # Print credentials for debugging
    client = gspread.authorize(creds)
    try:
        sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(tab_name)
        return sheet
    except SpreadsheetNotFound as e:  # Handle the exception
        print(f"Spreadsheet '{GOOGLE_SHEET_ID}' not found.")
        print(e)
        return None
    except gspread.exceptions.APIError as e:
        if e.response['status'] == 403:
            print("Permission error: The caller does not have permission to access the spreadsheet.")
        else:
            print("Error accessing Google Sheets API:", e)
        return None
    
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
    tickers = [stock['ticker'] for stock in screener_data]
    price_data = get_price_data(tickers)

    # Connect to Google Sheets
    sheet = connect_to_google_sheets("Stock_Tracker")
    if sheet is None:
        return

    # Iterate through screener data
    for stock in screener_data:
        ticker = stock['ticker']
        price = price_data.get(ticker)
        if price is not None:
            # Add pricing data to Google Sheets
            sheet.append_row([ticker, price])
        else:
            print(f"No price data available for {ticker}.")
        # Check if the ticker is already in Google Sheets
        values = sheet.get_all_values()
        if not values:
            # Sheet is empty, no need to check for ticker
            add_ticker_to_sheet(sheet, ticker)
        elif ticker not in [row[1] for row in values if len(row) >= 2]:
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
