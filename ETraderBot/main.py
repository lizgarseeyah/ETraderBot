import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
def get_price_data():
    # Implement code to fetch price data from financialmodelingprep
    pass

GOOGLE_SHEET_ID = '1WPv4K7GNxwX8HnwXfTvAwCwI19hsQVAZ2ARSNxufoy4'
# Function to authenticate and connect to Google Sheets
def connect_to_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEET_CREDS_FILE, scope)
    print("Credentials:", creds)  # Print credentials for debugging
    client = gspread.authorize(creds)
    try:
        # sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
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
    price_data = get_price_data()

    # Connect to Google Sheets
    sheet = connect_to_google_sheets()
    if sheet is None:
        return

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
