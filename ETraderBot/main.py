# Install necessary packages using pip install Flask requests

# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

app = Flask(__name__)

# Replace these placeholders with your actual credentials
CONSUMER_KEY = '5109a97aec4548ac21a4c0cd80b1f2d9'
CONSUMER_SECRET = 'c033d24362c344de6ee38162bfc0d86857b8cd2c44e5887c717931378ac221f2'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# E*TRADE API endpoints
REQUEST_TOKEN_URL = 'https://api.etrade.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.etrade.com/oauth/access_token'

# Step 1: Obtain a request token
response = requests.post(
    REQUEST_TOKEN_URL,
    auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
)
for x in response.text.split('&'):
    pair = x.split('=')
    print(pair)

# debug:
# response_text = response.text
# print(f"Response Text: {response_text}")

request_token_data = dict(x.split('=',1) for x in response.text.split('&'))
# oauth_token = request_token_data['oauth_token']
oauth_token = request_token_data.get('oauth_token', '')
# #debug
# print(request_token_data)

oauth_token_secret = request_token_data['oauth_token_secret']

# Step 2: Redirect the user to authorize the app (manual step)

# Step 3: Obtain an access token
access_token_url = f'{ACCESS_TOKEN_URL}?oauth_token={oauth_token}'
response = requests.post(
    access_token_url,
    auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
    data={'oauth_verifier': 'verifier_code'},  # Replace 'verifier_code' with the actual verifier code obtained during user authorization
)

# Debugging to identify the issue
# for x in response.text.split('&'):
#     pair = x.split('=')
#     print(pair)
    
# access_token_data = dict(x.split('=',1) for x in response.text.split('&'))
access_token_data = dict((x.split('=', 1) if '=' in x else (x, None)) for x in response.text.split('&'))
print(access_token_data)
oauth_token = request_token_data.get('oauth_token', '')
# ACCESS_TOKEN = access_token_data['oauth_token']
ACCESS_TOKEN_SECRET = access_token_data['oauth_token_secret']

# Now, you can use ACCESS_TOKEN and ACCESS_TOKEN_SECRET in your API requests

# Google Sheets API credentials
# Replace these with your own credentials
GOOGLE_SHEETS_API_KEY = 'https://docs.google.com/spreadsheets/d/1WPv4K7GNxwX8HnwXfTvAwCwI19hsQVAZ2ARSNxufoy4/edit#gid=335423734'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/get_account_info')
def get_account_info():
    url = 'https://api.etrade.com/v1/accounts'
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET)
    params = {'oauth_token': ACCESS_TOKEN, 'oauth_token_secret': ACCESS_TOKEN_SECRET}
    response = requests.get(url, headers=headers, auth=auth, params=params)
    account_info = response.json()
    return jsonify(account_info)

@app.route('/update_google_sheets', methods=['POST'])
def update_google_sheets():
    data = request.get_json()
    # Implement logic to update Google Sheets using the provided data
    # You may use the Google Sheets API or a library like gspread

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
