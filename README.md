# Technical Analysis Tradebot

> **Originally built: 2018.** Historical archive. This code reflects the tools, APIs, browser constraints, and coding practices of that period, not my current stack or standards.

Crypto tradebot used for backtesting technical analysis strategies using historical data, and plotting the results to a graph using pyplot. Currently supports the following: 

* Relative Strength Index (RSI)
* Stochastic RSI
* Simple Moving Averages (SMA)
* Volumetric Moving Averages

Trading strategies can be tested under `def sim_trade(dataset)`

When the current strategy under sim_trade is ran on the provided CSV files, it returns 340%. $1000 on an initial investment, returns $3400

Install required libraries:
`pip3 install -r requirements.txt`


## Recovered `cb` trading / analysis archive

A cleaned archive of related 2019–2020 Coinbase, Binance, Robinhood, Cobinhood, market-cap, backtesting, and strategy experiments has been recovered under [`recovered/cb-trading-analysis/`](./recovered/cb-trading-analysis/README.md). The recovered code is preserved as historical development work; credentials, duplicate backups, third-party vendored packages, logs, browser binaries, large market-data dumps, and wallet recovery material were intentionally excluded.
