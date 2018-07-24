import biasharaConfig
from binance.client import Client

api_key = biasharaConfig.api_key
secret_key = biasharaConfig.secret_key
client = Client(api_key, secret_key)

for order in orders:
    print(order)
