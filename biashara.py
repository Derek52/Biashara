import sys
import time
import biasharaConfig
import calculateSupport
from binance.client import Client
from binance.enums import *

api_key = biasharaConfig.api_key
secret_key = biasharaConfig.secret_key
profitPercentage = biasharaConfig.profitGoal

client = Client(api_key, secret_key)

class Coin:
    def __init__(self, name):
        self.name = name + 'BTC'
        self.buyTarget = calculateSupport.calculateBuyTarget(client, name)
        self.sellTarget = buyTarget + (buyTarget * (profitPercentage * .01)) #sell at the profit goal, above the buy price. .01 converts the percentage to the proper decimal. E.g. 5% * .01 = .05
        self.coinsBought = 0 #when we buy coins, we set this to that number, so the script knows how many to sell. This could probably be automated further by checking our wallet, but this was simpler for me to get up and running.
        self.buyTriggered = False #This tells us if we are currently in mode to buy or sell coins.
        self.currentPrice = 0.0
        self.highPrice = 0#this will keep track of the highest value we see the entire time the bot runs
        self.lowPrice = 1000000#this keeps track of the lowest value the bot sees

#Here we put our coins into the list. Coins are to be given to binance, in the form of their name, plus the coin you trading them with. E.g., their trading pair.
#For example to buy the coin ZIL, with bitcoin, we would send 'ZILBTC' as the name of the coin. You could also do 'ZILETH'(I'm not sure if ZIL has an ETH pair, it probably does though)
#In our coin's constructor, I append BTC, to whatever names you put here, because at the moment, I'm only trading in BTC pairs.
#This script should work with any other pairs though, if you take out the BTC I put in the constructor
#It also means putting BTC in the sample line here, means we'd get BTCBTC, which is not a thing, and would break this script.
coins = [Coin('BTC')]

coins = [Coin('BTC'),
            Coin('ZIL'),
            Coin('ETH')

spendingAmount = 0.0 #This is how much BTC you want the bot to be able to use, in BTC. E.g, if you have .2 BTC, but only want the bot to have access to this, set it to 0.1.
#This could be set to load your wallet's amount of BTC, and just use it all, but I didn't want to do that, during the testing phase of this bot.


#we use this as a timer to make sure we don't run our loop too often. We don't want to abuse binance's api. That can get you banned.
lastTimePriceWasChecked = time.time()

#this timer we use to print out information on our bot periodically. Printing the price everytime we check it, prints way too much into the terminal, and it's hard to read.
#at some point, I'll change this script to write to a file instead of just printing to the terminal, and this will become irrelevant.
timeToNotify = time.time()


while 1 == 1:

    currentTime = time.time()
    if currentTime - lastTimePriceWasChecked > 5:
        for (coin in coins):
            coinInfo = client.get_ticker(symbol=coin.name)
            coin.currentPrice = float(coinInfo['lastPrice'])
            if currentTime - timeToNotify > 300: #print information every 5 minutes
                print(coin.name)
                print("Buy in Price: "+ str(coin.buyTarget))#Leaving this script running for awhile, you will forget your buy price
                print("Current Price: " + str(coin.currentPrice))
                print("High Price: " + str(coin.highPrice))
                print("Low Price: " + str(coin.lowPrice))
                timeToNotify = time.time()

        if not coin.buyTriggered:
            if coin.currentPrice <= coin.buyTarget:
                coin.coinsBought = int(spendingAmount/coin.currentPrice)#we use an int, because different coins have different decimal precision, and I don't want to add all that.
                                                                        #e.g, some coins let you place orders with decimals to the 2nd decimal place, 1.23, 
                                                                        #some let you go to 6 places, 3.123456, and It's too much for me to add all that.
                order = client.order_market_buy(
                    symbol=coin.name,
                    quantity=coin.coinsBought)
                coin.buyTriggered = True
                print("tried to buy " + str(coin.coinsBought) + " for " + str(coin.currentPrice) + " btc each")
                coin.buyTriggered = True #this flips our boolean so we can go into sell mode

        if coin.buyTriggered:
            if coin.currentPrice >= coin.sellTarget:
                order = client.order_market_sell(
                        symbol=coin.name,
                        quantity=coin.coinsBought - 1)#I subtract one coin, to account for binance's trading fee. As a hypothetical example
                                                    #you could buy 5.05 coins of something, pay .06 coins as a fee, and then you'd have 4.99 coins left.
                                                    #Our coinsBought variable would be equal to 5, so we'd get an error trying to sell that many.
                                                    #spending higher amounts of money, subtracting 1 might not even be enough, but it's worked for the small amounts of money
                                                    #I've tested this bot with. I'll be extending this to work by checking the number of coins, of the given coin,
                                                    #in the wallet, at some point.
                print("tried to sell " + (coin.coinsBought - 1) + " for " + coin.currentPrice + " btc each")
                coin.buyTriggered = False #puts us back into buy mode, to try and buy this coin again. You could also kill the program here, if you don't want have it loop forever

        oldTime = time.time()

