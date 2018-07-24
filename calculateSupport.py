import sys
from binance.client import Client

def average(a, b):
    return (float(a)+float(b))/2

runningTotal = 0
count = 0

def calculateBuyTarget(client, coinName):
    kLines = client.get_historical_klines(coinName, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    
    for line in kLines:
        runningTotal = average(line[2], line[3]) + runningTotal
        count = count + 1

    oneDayAveragePrice = runningTotal/count
    print(coinName + " 24 hour average = " + str(oneDayAveragePrice))
    print("3% down = " + str(oneDayAveragePrice - (oneDayAveragePrice * .03)))
    return oneDayAveragePrice


#kLines are in the format [openTime, open, high, low, close, volume, closeTime, quoteAssetVolume, numberOfTrades, takerBuyBaseAssetVolume, takerbuyQuoteAssetVolume, someNumberToBeIgnored]
