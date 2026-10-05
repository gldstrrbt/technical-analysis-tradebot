# -*- coding: utf-8 -*-

import os, sys, csv, ccxt, asyncio, json
# -----------------------------------------------------------------------------

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

import ccxt.async_support as ccxt  # noqa: E402
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------

binance = ccxt.binance()
# symbol = 'BTC/USDT'
# timeframe = '1h'
timeframe = '1w'

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle

height = 15
length = 80

def load_json(dataset):
	return json.loads(dataset)


def csv_read(filepath):
	a = open(filepath+".csv", "r")
	b = csv.reader(a)
	return [c for c in b]


def csv_write(filepath):
	a = open(filepath+".csv", "w", newline="")
	b = csv.writer(a)
	return b


def get_active_symbols(exchange):
	return [symbol for symbol in exchange.symbols if is_active_symbol(exchange, symbol)]


def is_active_symbol(exchange, symbol):
	return ('.' not in symbol) and (('active' not in exchange.markets[symbol]) or (exchange.markets[symbol]['active']))


async def get_ath_range_and_last(exchange, symbol, timeframe):
	print("exchange, symbol, timeframe", exchange, symbol, timeframe)
	print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

	# get a list of ohlcv candles
	# ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
	# print(ohlcv)
	# test = [x[4] for x in ohlcv]

	# lo,hi = sys.maxsize,-sys.maxsize-1
	# for x in (item[4] for item in ohlcv):
		# print(x)
		# print(item)

	# if str(symbol).split("/") == "USDT":
	try:	
		ohlcv           = await exchange.fetch_ohlcv(symbol, timeframe)
		new_ohlcv       = []

		for a in ohlcv:
			convert_time    = exchange.iso8601(a[0])
			split_year      = str(convert_time).split("-")[0] 
			split_month      = int(str(convert_time).split("-")[1]) 
			if (split_year == "2020") or (split_year == "2021" and split_month < 7):
				new_ohlcv.append(a)
			print(new_ohlcv)

		# maxPricedItem   = max(ohlcv, key=lambda x:x[4])
		# print(maxPricedItem)

			# lo,hi = min(x,lo),max(x,hi)
			# print(lo,hi)
		# print(max(test))

		# for asdf in ohlcv:
		#     print(exchange.iso8601(asdf[0]))

		# get the ohlCv (closing price, index == 4)
		series 	= [x[index] for x in ohlcv]
		last 	= ohlcv[len(ohlcv) - 1][index]  # last closing price
		return [new_ohlcv, last]
		# else:
		# 	return ["null", "null"]
	except:
		pass


def filter_dates(dataset):
	new_data=[]
	for a in dataset:
		convert_time = datetime.fromtimestamp(a[0]/1000)
		print(convert_time)
		split_year     = str(convert_time).split("-")[0] 
		split_month    = int(str(convert_time).split("-")[1]) 
		if (split_year == "2020"  and split_month > 8) or (split_year == "2021" and split_month < 7):
			new_data.append(a)
	return new_data



def process_dataset():
	a = csv_read("1w_list_clean")
	b = csv_write("1w_ratios")
	headers = ["symbol", "latest_price", "ath_price", "atl_price","ratio_curr_to_ath", "ath_double", "ath_price/atl_price", "potential_multiplier", "ath_volume", "ath_date","atl_date", "ath_timestamp"]
	b.writerow(headers)
	for c in a:
		symbol 			= c[0]
		latest_price 	= float(c[1])
		d 				= load_json(c[2])
		# print(latest_price)
		d = filter_dates(d)

		if float(d[-1][4]) > float(latest_price):
			print(d[-1])
			print(d[-1][4])
			print(latest_price)
			print("*"*50)
			print("*"*50)
			print("*"*50)
		ath_row  		= max(d, key=lambda x:x[4])
		ath_timestamp 	= ath_row[0]
		ath_price 		= float(ath_row[4])
		ath_double 		= ath_price*2
		ath_volume 		= float(ath_row[5])
		ath_date 		= datetime.fromtimestamp(ath_timestamp/1000)

		atl_row  		= min(d, key=lambda x:x[4])
		atl_timestamp 	= atl_row[0]
		atl_price 		= float(atl_row[4])
		atl_double 		= atl_price*2
		atl_volume 		= float(atl_row[5])
		atl_date 		= datetime.fromtimestamp(atl_timestamp/1000)

		ratio_curr_to_ath = latest_price/ath_price
		potential_multiplier = ath_double/latest_price
		compiled_row = [symbol, latest_price, ath_price, atl_price, ratio_curr_to_ath, ath_double, ath_price/atl_price, potential_multiplier, ath_volume, ath_date, atl_date, ath_timestamp]
		b.writerow(compiled_row)

# async def get_write_data():
	# a 				= csv_write("1w_list")
	# binance         = ccxt.binance({
	# 	'enableRateLimit': True,
	# 	'rateLimit': 1000,
	# })
	# ticker_list = ['1INCH/USDT','AAVE/USDT','ACM/USDT','ADA/USDT','AION/USDT','AKRO/USDT','ALGO/USDT','ALICE/USDT','ALPACA/USDT','ALPHA/USDT','ANKR/USDT','ANT/USDT','AR/USDT','ARDR/USDT','ARPA/USDT','ASR/USDT','ATA/USDT','ATM/USDT','ATOM/USDT','AUD/USDT','AUDIO/USDT','AUTO/USDT','AVA/USDT','AVAX/USDT','AXS/USDT','BADGER/USDT','BAKE/USDT','BAL/USDT','BAND/USDT','BAR/USDT','BAT/USDT','BCH/USDT','BEAM/USDT','BEL/USDT','BLZ/USDT','BNB/USDT','BNT/USDT','BOND/USDT','BTC/USDT','BTCST/USDT','BTG/USDT','BTS/USDT','BTT/USDT','BURGER/USDT','BUSD/USDT','BZRX/USDT','C98/USDT','CAKE/USDT','CELO/USDT','CELR/USDT','CFX/USDT','CHR/USDT','CHZ/USDT','CKB/USDT','CLV/USDT','COCOS/USDT','COMP/USDT','COS/USDT','COTI/USDT','CRV/USDT','CTK/USDT','CTSI/USDT','CTXC/USDT','CVC/USDT','DASH/USDT','DATA/USDT','DCR/USDT','DEGO/USDT','DENT/USDT','DEXE/USDT','DGB/USDT','DIA/USDT','DNT/USDT','DOCK/USDT','DODO/USDT','DOGE/USDT','DOT/USDT','DREP/USDT','DUSK/USDT','EGLD/USDT','ELF/USDT','ENJ/USDT','EOS/USDT','EPS/USDT','ERN/USDT','ETC/USDT','ETH/USDT','EUR/USDT','FARM/USDT','FET/USDT','FIL/USDT','FIO/USDT','FIRO/USDT','FIS/USDT','FLM/USDT','FLOW/USDT','FOR/USDT','FORTH/USDT','FTM/USDT','FTT/USDT','FUN/USDT','GBP/USDT','GHST/USDT','GNO/USDT','GRT/USDT','GTC/USDT','GTO/USDT','GXS/USDT','HARD/USDT','HBAR/USDT','HIVE/USDT','HNT/USDT','HOT/USDT','ICP/USDT','ICX/USDT','INJ/USDT','IOST/USDT','IOTA/USDT','IOTX/USDT','IRIS/USDT','JST/USDT','JUV/USDT','KAVA/USDT','KEEP/USDT','KEY/USDT','KLAY/USDT','KMD/USDT','KNC/USDT','KSM/USDT','LINA/USDT','LINK/USDT','LIT/USDT','LPT/USDT','LRC/USDT','LSK/USDT','LTC/USDT','LTO/USDT','LUNA/USDT','MANA/USDT','MASK/USDT','MATIC/USDT','MBL/USDT','MBOX/USDT','MDT/USDT','MDX/USDT','MFT/USDT','MINA/USDT','MIR/USDT','MITH/USDT','MKR/USDT','MLN/USDT','MTL/USDT','NANO/USDT','NBS/USDT','NEAR/USDT','NEO/USDT','NKN/USDT','NMR/USDT','NU/USDT','NULS/USDT','OCEAN/USDT','OG/USDT','OGN/USDT','OM/USDT','OMG/USDT','ONE/USDT','ONG/USDT','ONT/USDT','ORN/USDT','OXT/USDT','PAXG/USDT','PERL/USDT','PERP/USDT','PHA/USDT','PNT/USDT','POLS/USDT','POND/USDT','PSG/USDT','PUNDIX/USDT','QNT/USDT','QTUM/USDT','QUICK/USDT','RAMP/USDT','RAY/USDT','REEF/USDT','REN/USDT','REP/USDT','REQ/USDT','RIF/USDT','RLC/USDT','ROSE/USDT','RSR/USDT','RUNE/USDT','RVN/USDT','SAND/USDT','SC/USDT','SFP/USDT','SHIB/USDT','SKL/USDT','SLP/USDT','SNX/USDT','SOL/USDT','SRM/USDT','STMX/USDT','STORJ/USDT','STPT/USDT','STRAX/USDT','STX/USDT','SUN/USDT','SUPER/USDT','SUSD/USDT','SUSHI/USDT','SXP/USDT','TCT/USDT','TFUEL/USDT','THETA/USDT','TKO/USDT','TLM/USDT','TOMO/USDT','TORN/USDT','TRB/USDT','TRIBE/USDT','TROY/USDT','TRU/USDT','TRX/USDT','TUSD/USDT','TVK/USDT','TWT/USDT','UMA/USDT','UNFI/USDT','UNI/USDT','USDC/USDT','UTK/USDT','VET/USDT','VITE/USDT','VTHO/USDT','WAN/USDT','WAVES/USDT','WAXP/USDT','WIN/USDT','WING/USDT','WNXM/USDT','WRX/USDT','WTC/USDT','XEC/USDT','XEM/USDT','XLM/USDT','XMR/USDT','XRP/USDT','XTZ/USDT','XVG/USDT','XVS/USDT','YFI/USDT','YFII/USDT','ZEC/USDT','ZEN/USDT','ZIL/USDT','ZRX/USDT']
	# print("binance", binance)
	# print("binance", binance)
	# print("binance", binance)
	# print("binance", binance)
	# await binance.load_markets()
	# print(binance.id, 'fetching all tickers by simultaneous multiple concurrent requests')
	# symbols_to_load = get_active_symbols(binance)
	# print("symbols_to_load", symbols_to_load)
	# timeframe       = '1w'
	# for symbol in ticker_list:
	# 	# if str(symbol).split("/") == "USDT":
	# 	print("symbol", symbol)
		# new_ohlcv, last = await get_ath_range_and_last(binance, symbol, timeframe)
		# a.writerow([symbol, last, new_ohlcv])
	# 	print(new_ohlcv, last)
	# 	print("*"*50)


# asyncio.get_event_loop().run_until_complete(init())
# asyncio.run(init())
# asyncio.get_event_loop().run_until_complete(get_write_data())


process_dataset()