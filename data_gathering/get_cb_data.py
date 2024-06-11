import requests
from requests.exceptions import HTTPError
import pandas as pd
import json as js
from datetime import datetime, timedelta


REST_API = 'https://api.pro.coinbase.com'
PRODUCTS_URL = REST_API+'/products'
# I am only interested in a few currencies that I want to trade, so let's add them here:
MY_CURRENCIES = ['BTC-USD','ETH-USD','SOL-USD','UNI-USD'] 


def connect(url, *args, **kwargs):
    try:
        if kwargs.get('param', None) is not None:
            response = requests.get(url,params)
        else:
            response = requests.get(url)
        response.raise_for_status()
        #print('HTTP connection success!')
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


#### Testing the API

response = connect(PRODUCTS_URL)
response_content = response.content
response_text = response.text
response_headers = response.headers

df_currencies = pd.read_json (response_text)
print("\nNumber of columns in the dataframe: %i" % (df_currencies.shape[1]))
print("Number of rows in the dataframe: %i\n" % (df_currencies.shape[0]))
columns = list(df_currencies.columns)
print(columns)
print() 
#df_currencies[df_currencies.id.isin(MY_CURRENCIES)][['id', 'quote_currency']].head(5)
df_currencies[df_currencies.id.isin(MY_CURRENCIES)]

currency_rows = []
for currency in MY_CURRENCIES:
    response = connect(PRODUCTS+'/'+currency+'/stats')
    response_content = response.content
    data = js.loads(response_content.decode('utf-8'))
    currency_rows.append(data)
# Create dataframe and set row index as currency name
df_statistics = pd.DataFrame(currency_rows, index = MY_CURRENCIES)
df_statistics


##### Actual fetching call

df_history = pd.DataFrame()
look_back_days = 30
hour_increments = 5 
n_calls = look_back_days * hour_increments
for i in range(n_calls):
    start_date = (datetime.today() - timedelta(hours=hour_increments*(i+1))).isoformat()
    end_date = (datetime.today() - timedelta(hours=hour_increments*(i))).isoformat()
    # Please refer to the coinbase documentation on the expected parameters
    params = {'start':start_date, 'end':end_date, 'granularity':'60'}

    for currency in MY_CURRENCIES:
        response = connect(PRODUCTS+'/'+currency+'/candles', param = params)
        response_text = response.text
        df_history_temp = pd.read_json(response_text)
        df_history_temp['symbol'] = currency
        df_history = pd.concat([df_history, df_history_temp])
# Add column names in line with the Coinbase Pro documentation
df_history.columns = ['time','low','high','open','close','volume','symbol']

# We will add a few more columns just for better readability
df_history['date'] = pd.to_datetime(df_history['time'], unit='s')
df_history['year'] = pd.DatetimeIndex(df_history['date']).year
df_history['month'] = pd.DatetimeIndex(df_history['date']).month
df_history['day'] = pd.DatetimeIndex(df_history['date']).day

out_file_name = "Dataset_Crypto_2024_05_to_06.csv"
df_history.to_csv(out_file_name)