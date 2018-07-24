import sys
import biasharaConfig
from binance.client import Client

api_key = biasharaConfig.api_key
secret_key = biasharaConfig.secret_key
client = Client(api_key, secret_key)

coin = sys.argv[1] + 'BTC'

coinPrice = client.get_ticker(symbol=coin)
print(coinPrice.get("lastPrice"))
