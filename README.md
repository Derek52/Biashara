# Biashara-cryptobot

I'm bad at naming things, so I just use words from languages my parents speak. Biashara is Swahili for the word 'Trade'. It can also mean business, and commerce.

This repo is made up of a few simple things, and 2 more complex things.

First, you've got a few utility scripts, like checkCoin.py, which can be run in the terminal to quickly check the most recent traded price of any coin.
You also have getOpenOrders.py and checkAccountBalances.py, that can quickly pull some of your data from binance.

Secondly, you have the meat of the repo. There are 2 different biashara scripts.

manualBiashara.py, is almost not a bot, because you have to supply buy targets for each coin you are watching. This can be pretty useful though. Using this script to watch coins for your buy and sell targets. It's better than using limit orders on binance, or staying up 24/7 to watch the prices yourself.
It may also be better than biashara.py, because biashara.py's algorithm for choosing buy targets is pretty simple at the moment. I'll be doing testing on more tradig algorithms in the coming months.

As was just hinted at, biashara.py is an automated bot, that calculates it's own buy targets. It does this using a method in the calculateSupport.py file. Right now all it does is take an average of the last 24 hours of trades, and try and buy at 3% below that average.

Using these bots is pretty simple. First, you will need python3 and pip install. Then you run

```
pip install python-binance
```

And you'll be setup to run the scripts.

Decide if you want the manual or automated biashara, and go in and supply your list of coins(each script has comments on how to do this).

Before you can run any of these scripts, you will need to provide api keys to your binance account. You put these keys in the biasharaConfig.py file.

In the biasharaConfig.py file, you also set your profit goal, which is the amount you want biashara to try and make on each trade. By default, biashara will wait for a 5% profit to sell any coins it buys.

More info on how to use python-binance can be found here, https://github.com/sammchardy/python-binance, and here https://python-binance.readthedocs.io/en/latest/

Use these scripts at your own risk.
