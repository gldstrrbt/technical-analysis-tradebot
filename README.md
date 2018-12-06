# Technical Analysis Tradebot

Crypto tradebot used for backtesting technical analysis strategies using historical data, and plotting the results to a graph using pyplot. Currently supports the following: 

* Relative Strength Index (RSI)
* Stochastic RSI
* Simple Moving Averages (SMA)
* Volumetric Moving Averages

Trading strategies can be tested under `def sim_trade(dataset)`

When the current strategy under sim_trade is ran on the provided CSV files, it returns 340%. $1000 on an initial investment, returns $3400

Install required libraries:
`pip3 install -r requirements.txt`
