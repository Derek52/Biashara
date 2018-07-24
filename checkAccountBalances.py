import biasharaConfig
from binance.client import Client

api_key = biasharaConfig.api_key
secret_key = biasharaConfig.secret_key
client = Client(api_key, secret_key)

info = client.get_account()


print("Coin\t\tAvailable\t\tLocked")

for item in info['balances']:
    if float(item['free']) > 0 or float(item['locked']) > 0:
        print(item['asset'] + " btc:  " + item['free'] + "    " + item['locked'])

