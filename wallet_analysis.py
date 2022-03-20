import requests

#Giorgio Vidali
#Practicing with etherscan api key



# api_token = 
#Insert api key for etherscan here^

def return_fees_paid(an_address):
    the_response = requests.get(f'https://api.etherscan.io/api?module=account&action=txlist&address={an_address.lower()}&startblock=0&endblock=99999999&sort=asc&apikey={key}')
    json_data = the_response.json()
    total_spent_on_gas = 0
    total_spent_on_failed_transactions = 0
    total_spent_on_receiving_transactions = 0
    for i in json_data['result']:
        if i['from'].lower() == an_address.lower():
            total_spent_on_gas += (int(i['gasUsed']) * int(i['gasPrice']))
            if i['isError'] == '1':
                total_spent_on_failed_transactions += (int(i['gasUsed']) * int(i['gasPrice']))
        else:
            total_spent_on_receiving_transactions += (int(i['gasUsed']) * int(i['gasPrice']))
    adjustedTSonGas = total_spent_on_gas / 1000000000000000000
    adjustedTSonFailed = total_spent_on_failed_transactions / 1000000000000000000
    adjustedTSonRecieve = total_spent_on_receiving_transactions / 1000000000000000000
    return round(adjustedTSonGas,5),round(adjustedTSonFailed, 5),round(adjustedTSonRecieve, 5)

def get_val_wallet(an_andress):
    the_response = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={an_andress}&tag=latest&apikey={api_token}')
    json_data = the_response.json()
    tempVal = int(json_data['result']) / 1000000000000000000
    final_val = round(tempVal, 5)
    return final_val

def get_eth_last_price():
    the_response = requests.get(f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={api_token}')
    json_data = the_response.json()
    return float(json_data['result']['ethusd'])

def complete_wallet_data(an_address):
    '''
    Inputs a wallet address
    Outputs a list of 5 tuples
    .. WalletAddress
    .. (walletValEth, inUSD)
    .. (SpendingOnGasEth, inUSD)
    .. (SpendingOnFailed, inuSD)
    .. (sepmdingOnRecieve, inUSD)
    '''
    price_of_eth = get_eth_last_price()
    try: 
        wallet_val = get_val_wallet(an_address)
        total_fees = return_fees_paid(an_address)
        WalletTuple = (wallet_val, round(wallet_val * price_of_eth, 2))
        SpendingOnTrans = (total_fees[0], round(total_fees[0] * price_of_eth,2 ))
        SpendingOnFail = (total_fees[1], round(total_fees[1] * price_of_eth, 2))
        SpendingOnRec = (total_fees[2], round(total_fees[2] * price_of_eth,2))
        return [an_address.upper(), WalletTuple,SpendingOnTrans,SpendingOnFail,SpendingOnRec]
    except ValueError:
        return False