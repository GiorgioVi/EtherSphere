import requests
import datetime
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
from io import BytesIO
import base64


# #CryptoCompareKey
# key = 
# To try it out get a key and put here^

def get_eth_prices_crypto_compare(numDays):
    dates_raw = []
    start_date_raw = datetime.date.today()
    for i in reversed(range(numDays)):
        days = datetime.timedelta(i)
        dates_raw.append(start_date_raw - days)
    dates = [x.strftime('%m/%d/%y') for x in dates_raw]

    the_response = requests.get(f'https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=USD&limit={numDays - 1}&api_key={key}')
    json_data = the_response.json()
    price_data = json_data['Data']['Data']
    final_prices = [float(x['close']) for x in price_data]
    return final_prices, dates

def return_key_stats(a_list):
    the_min = min(a_list)
    the_max = max(a_list)
    the_avg = round(statistics.mean(a_list), 2)
    the_std = round(statistics.stdev(a_list), 2)
    return the_min, the_max, the_avg, the_std

def get_btc_prices_crypto_compare(numDays):
    dates_raw = []
    start_date_raw = datetime.date.today()
    for i in reversed(range(numDays)):
        days = datetime.timedelta(i)
        dates_raw.append(start_date_raw - days)
    dates = [x.strftime('%m/%d/%y') for x in dates_raw]

    the_response = requests.get(f'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit={numDays - 1}&api_key={key}')
    json_data = the_response.json()
    price_data = json_data['Data']['Data']
    final_prices = [float(x['close']) for x in price_data]
    return final_prices, dates

def convert_eth_and_btc_to_percent_change(eths, btcs):
    eth_list = eths[0]
    btc_list = btcs[0]

    converted_eth = [(x/eth_list[0]) - 1 for x in eth_list]
    converted_btc = [(x/btc_list[0]) - 1 for x in btc_list]

    df = pd.DataFrame({
        'ETH': converted_eth,
        'BTC': converted_btc
    },
    index = eths[1])
    return df



#Stops window from opening
matplotlib.use('Agg')

def create_price_graph(rates,time):
    a_dict = {'Day': time, 'Rate': rates}
    df = pd.DataFrame(a_dict)
    img = BytesIO()

    plt.plot(df['Day'],df['Rate'], label = 'Price Of Ethereum')
    if len(rates) == 7:
        df['FiveDayRolling'] = df['Rate'].rolling(window=2).mean()
        plt.plot(df['Day'], df['FiveDayRolling'], label = 'Two Day Rolling Average')
    elif len(rates) == 30:
        df['FiveDayRolling'] = df['Rate'].rolling(window=5).mean()
        plt.plot(df['Day'], df['FiveDayRolling'], label = 'Five Day Rolling Average')
    else:
        df['FiveDayRolling'] = df['Rate'].rolling(window=30).mean()
        plt.plot(df['Day'], df['FiveDayRolling'], label = 'Thirty Day Rolling Average')
    plt.title('ETH to USD')
    plt.xlabel('Time')
    plt.ylabel('Price in Dollars')
    plt.xticks(rotation=45, fontsize=7)
    if len(time) == 30:
        plt.xticks(np.arange(0, len(time)+1, 4))
    if len(time) == 365:
        plt.xticks(np.arange(0, len(time)+1, 30))
    plt.legend(loc='lower right', prop={'size': 6})
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url




def compare_graph(a_frame):
    
    index = a_frame.index.tolist()
    btc = a_frame['BTC'].tolist()
    btc[0] = 0
    eth = a_frame['ETH'].tolist()
    eth[0] = 0
    img = BytesIO()
    plt.plot(index,eth, label = 'ETH percent Change')
    plt.plot(index,btc, label = 'BTC percent Change')
    plt.title('ETH to BTC Growth')
    plt.xlabel('Time')
    plt.ylabel('Price in Dollars')
    plt.xlabel('Time')
    plt.ylabel('Percent Change From First Day In Range')
    plt.xticks(rotation=45, fontsize=7)
    if len(index) == 30:
        plt.xticks(np.arange(0, len(index)+1, 4))
    if len(index) == 365:
        plt.xticks(np.arange(0, len(index)+1, 30))
    plt.legend(loc='lower right', prop={'size': 6})
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()]) 
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url