from flask import Flask, render_template, request
from wallet_analysis import complete_wallet_data
import creating_eth_analysis

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/wallet', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /wallet is accessed directly. Try going to the home page to submit the form"
    else:
        raw_address = request.form.get('walletAddress')
        the_data = complete_wallet_data(raw_address)
        if the_data == False:
            return render_template('invalid_wallet.html')
        return render_template('wallet.html', raw_address = raw_address, form_data = the_data)

@app.route('/research', methods = ['POST', 'GET'])
def open():
    if request.method == 'GET':
        return f"The URL /research is accessed directly. Try going to the home page to submit the form"
    else:
        num_days = int(request.form.get('radioButtons'))
        complete_data = creating_eth_analysis.get_eth_prices_crypto_compare(num_days)
        prices,times = complete_data[0],complete_data[1]
        the_data = creating_eth_analysis.return_key_stats(prices)
        the_plot = creating_eth_analysis.create_price_graph(prices,times)
        return render_template('research.html', num_days = num_days, form_data = the_data, the_plot= the_plot)

@app.route('/eth_to_btc', methods = ['POST', 'GET'])
def compare():
    if request.method == 'GET':
        return f"The URL /eth_btc is accessed directly. Try going to the home page to submit the form"
    else:
        num_days = int(request.form.get('radioButtonsCompare'))
        eth_data = creating_eth_analysis.get_eth_prices_crypto_compare(num_days)
        btc_data = creating_eth_analysis.get_btc_prices_crypto_compare(num_days)
        the_data = creating_eth_analysis.convert_eth_and_btc_to_percent_change(eth_data,btc_data)
        the_plot = creating_eth_analysis.compare_graph(the_data)

        return render_template('eth_btc.html', num_days = num_days, the_plot = the_plot)



if __name__ == '__main__':
    app.run(debug=True)