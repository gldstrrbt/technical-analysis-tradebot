import os, json, requests, time, csv, matplotlib, mpl_finance, random, math
from Robinhood import Robinhood
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
from mpl_finance import candlestick2_ohlc
from mpl_finance import index_bar
from mpl_finance import plot_day_summary_oclh
from datetime import datetime, timedelta
import cbpro
public_client = cbpro.PublicClient()

###########################################################################
###########################################################################
###########################################################################

def moving_average_alt(df, n):
	"""Calculate the moving average for the given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	compiled_sma 	= pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df

###########################################################################
###########################################################################
###########################################################################

def get_sma_diff_range(dataset, sma_type):
	diffs 	= []

	dataset_end = len(dataset)
	dataset_start = dataset_end-75
	# dataset_start = dataset_end-100
	while dataset_start < dataset_end:
	# for a in dataset:
		a = dataset[dataset_start]
		# print(a)
		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
		# print(test_diff)
		diffs.append(float(test_diff))
		dataset_start += 1

	diffs.sort()
	# print(diffs)
	front 	= []
	back  	= []
	counter = 0
	ends 	= int(len(diffs)*.4)
	backend = len(diffs)-ends

	while counter < ends:
		front.append(diffs[counter])
		counter+=1
	
	counter = 1

	while (ends-counter)+backend > backend:
		back.append(diffs[(ends-counter)+backend])
		counter+=1
	return [np.mean(front), np.mean(back)]

###########################################################################
###########################################################################
###########################################################################

def relative_strength_index(df, n):
	"""Calculate Relative Strength Index(RSI) for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	i = 0
	UpI = [0]
	DoI = [0]
	# print(df.columns())
	while i + 1 <= df.index[-1]:
		UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
		DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
		if UpMove > DoMove and UpMove > 0:
			UpD = UpMove
		else:
			UpD = 0
		UpI.append(UpD)
		if DoMove > UpMove and DoMove > 0:
			DoD = DoMove
		else:
			DoD = 0
		DoI.append(DoD)
		i = i + 1
	UpI = pd.Series(UpI)
	DoI = pd.Series(DoI)
	PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
	NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
	# RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI_' + str(n))
	RSI = pd.Series(PosDI / (PosDI + NegDI), name='rsi')
	df = df.join(RSI)
	return df

###########################################################################
###########################################################################
###########################################################################

# x = open("Gdax_ETHUSD_1h.json", "r+")
# x = open("gemini_BTCUSD_1hr.json", "r+")
# x = open("gemini_ETHUSD_1hr.json", "r+")
# x = open("gemini_ETHUSD_2018_1min.json", "r+")
# x = open("20190120_192023___data.json", "r+")
# x = open("20190122_185923___data.json", "r+")
# x = open("20190122_185923___data.json", "r+")
# x = open("20190122_185923___data.json", "r+")
# x = open("20190122_194125___data.json", "r+")
# x = open("20190123_201930___data.json", "r+")
# x = open("20190123_203432___data.json", "r+")
# x = open("20190122_194125___data.json", "r+")
# x = open("csv_delimit_1.json", "r+")
# x = open("20190122_212440___data.json", "r+")
# x = open("20190122_194125___data.json", "r+")



# BEGINNING OF DEC 2018
# x = open("20190123_205145___data.json", "r+")

# END OF DEC 2018
# x = open("20190122_212440___data.json", "r+")

# END OF SEPT 2018
# x = open("20190123_203432___data.json", "r+")

# BEGINNING OF 2017
# x = open("yy.json", "r+")


# print(ff)
# print(w)
# print(w)
# print(len(w))
# print(len(jj))
# ETH GEMINI HR 2017 - Han 2019 = 100K+ off 1k
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 3)

# ETH GEMINI 1 MIN TOTAL 2016-2018 = 330K+ off 1k 
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 7)

# BTC GEMINI 1 MIN TOTAL 2015-2017 = 443501.71825211716 off 1k 
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 7)


# LAST LEFT OFF GDAX 20190120_192023___data ETH - FULL CONDITIONAL - 12289 return
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 2)
# dataset = get_sma(testing, 12)

################################################################################################### 
####################################### NEW STRATEGY TEST #######################################
################################################################################################### 
# OLD STRATEGY WAS DETERMINED BY A LARGE DATASET WHERE THE DIFF VARIABLES WERE DECLARED ONCE
# THIS NEW STRATEGY ADAPTS TO THE FORWARD MOVEMENTS AND MEASURES FROM A SET RANGE WHERE THE HEAD 
# IS THE CURRENT INDEX AND THE SET NUMBER OF NEIGHBORS BEHIND IT DETERMINE THE THRESHOLDS FOR ORDERS
# THEN BASED ON A VISUAL ESTIMATE A VALUE IS GIVEN IN THE CONDITIONALS FOR DIFFERENCE BETWEEN HIGHER 
# SMA AND POSITION OF THE LOWER SMA
# IN THE FOLLOWING TESTS THE PEAK DIFF IN BUY IS AROUND .002-.006 AND SELL .002
################################################################################################### 

############################################################
# 39% ON NOV 2018-JAN 2019 - SMA 1 + 5 with ONEUP AND ONE DOWN AT .002 - 20190122_194125___data - get_sma_diff_range = 100 range - .4 edges
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 5)
############################################################

############################################################
# 69% ON NOV 2018-JAN 2019 - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190122_194125___data - get_sma_diff_range = 100 range - .4 edges
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
############################################################

############################################################
# 65% ON NOV 2018-JAN 2019 - SMA 1 + 7 with ONEUP AND ONE DOWN AT .002 - 20190122_194125___data - get_sma_diff_range = 100 range - .4 edges
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 7)
############################################################

############################################################
# 53% ON DEC 2018-JAN 2019 - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190122_185923___data - get_sma_diff_range = 100 range - .4 edges
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
############################################################

############################################################
# 25.6% ON JAN 2019 - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190122_212440___data - get_sma_diff_range = 75 range - .4 edges - SELL ABOVE *1.002
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
############################################################

############################################################
# 74.9% ON JAN 2019 - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190122_194125___data - get_sma_diff_range = 75 range - .4 edges - SELL ABOVE *1.002
# buy_thresh = get_sma_diff_range(yy, sma_type)[0]  + (get_sma_diff_range(yy, sma_type)[1] * 0.001)
# sell_thresh = get_sma_diff_range(yy, sma_type)[1] + (get_sma_diff_range(yy, sma_type)[1] * 0.003)
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
############################################################

############################################################
# 75.3% ON JAN 2019 - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190122_194125___data - get_sma_diff_range = 75 range - .4 edges - SELL ABOVE *1.002
# buy_thresh = get_sma_diff_range(yy, sma_type)[0]  + (get_sma_diff_range(yy, sma_type)[1] * 0.001)
# sell_thresh = get_sma_diff_range(yy, sma_type)[1] + (get_sma_diff_range(yy, sma_type)[1] * 0.01)
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
############################################################

############################################################
# 94% ON  2018-12-06 20:52:00+00:00 UTC - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190123_205145___data - get_sma_diff_range = 75 range - .4 edges - SELL ABOVE *1.002
# buy_thresh = get_sma_diff_range(yy, sma_type)[0]  + (get_sma_diff_range(yy, sma_type)[1] * 0.001)
# sell_thresh = get_sma_diff_range(yy, sma_type)[1] + (get_sma_diff_range(yy, sma_type)[1] * 0.01)
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
# rsi < 12 and rsi > 90 
# last_val*1.002
############################################################

############################################################
# 96.8% ON  2018-12-06 20:52:00+00:00 UTC - SMA 1 + 6 with ONEUP AND ONE DOWN AT .002 - 20190123_205145___data - get_sma_diff_range = 75 range - .4 edges - SELL ABOVE *1.002
# buy_thresh = get_sma_diff_range(yy, sma_type)[0]  + (get_sma_diff_range(yy, sma_type)[1] * 0.001)
# sell_thresh = get_sma_diff_range(yy, sma_type)[1] + (get_sma_diff_range(yy, sma_type)[1] * 0.01)
# dataset = get_sma(testing, 1)
# dataset = get_sma(testing, 6)
# rsi < 12 and rsi > 90 
# last_val*1.002
############################################################

##################################################################
##################################################################
##################################################################

# def auth():
# 	key = os.getenv("COINBASE_API_KEY", "")
# 	b64secret = os.getenv("COINBASE_API_SECRET", "")
# 	passphrase = os.getenv("COINBASE_API_PASSPHRASE", "")
# 	auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
# 	print(auth_client)
# 	# Use the sandbox API (requires a different set of API access credentials)
# 	# auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, api_url="https://api-public.sandbox.pro.coinbase.com")
# 	return auth_client

# AUTH AWAY FROM HOME
def auth():
	key = os.getenv("COINBASE_API_KEY", "")
	b64secret = os.getenv("COINBASE_API_SECRET", "")
	passphrase = os.getenv("COINBASE_API_PASSPHRASE", "")
	auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
	# print(auth_client)
	# auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, api_url="https://api-public.sandbox.pro.coinbase.com")
	return auth_client

##################################################################
##################################################################
##################################################################

def money_flow_index(df, n):
	"""Calculate Money Flow Index and Ratio for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	PP = (df['high'] + df['low'] + df['close']) / 3
	i = 0
	PosMF = [0]
	while i < df.index[-1]:
	# while i < len(df):
		if PP[i + 1] > PP[i]:
			PosMF.append(PP[i + 1] * df.loc[i + 1, 'volume'])
		else:
			PosMF.append(0)
		i = i + 1
	PosMF = pd.Series(PosMF)
	TotMF = PP * df['volume']
	MFR = pd.Series(PosMF / TotMF)
	# MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name='MFI_' + str(n))
	MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name='mfi')
	df = df.join(MFI)
	return df

##################################################################
##################################################################
##################################################################

def get_ticker():
	a = public_client.get_product_ticker(product_id='ETH-USD')
	# a = auth().get_product_ticker(product_id='ETH-USD')
	return a

##################################################################
##################################################################
##################################################################

def get_hist(timing):
	# a = public_client.get_product_historic_rates('ETH-USD', granularity=timing)
	a = auth().get_product_historic_rates('ETH-USD', granularity=timing)
	return a

##################################################################
##################################################################
##################################################################

def my_fills():
	a = auth()
	b = a.get_fills("ETH-USD")
	return b

##################################################################
##################################################################
##################################################################

def standard_deviation(df, n):
	"""Calculate Standard Deviation for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	df = df.join(pd.Series(df['close'].rolling(n, min_periods=n).std(), name='std'))
	return df

##################################################################
##################################################################
##################################################################

def macd(df, n_fast, n_slow):
	"""Calculate macd, macd Signal and macd difference
	
	:param df: pandas.DataFrame
	:param n_fast: 
	:param n_slow: 
	:return: pandas.DataFrame
	"""
	ema_fast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
	ema_slow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
	macd = pd.Series(ema_fast - ema_slow, name='macd')
	macd_sign = pd.Series(macd.ewm(span=9, min_periods=9).mean(), name='macd_sign_' + str(n_fast) + '_' + str(n_slow))
	macd_diff = pd.Series(macd - macd_sign, name='macd_diff_' + str(n_fast) + '_' + str(n_slow))
	df = df.join(macd)
	df = df.join(macd_sign)
	df = df.join(macd_diff)
	return df

##################################################################
##################################################################
##################################################################

def convert_csv(filename):
	a = open(str(filename)+".csv", "r+")
	b = csv.reader(a)
	
	c = open(str(filename)+"_header.csv", "w+")
	d = csv.writer(c)
	d.writerow(["date", "open", "high", "low", "close", "volume"])

	for e in b:
		d.writerow(e)
	# c.close()

##########################################################################################
##########################################################################################

def check_ticker():
	a = auth().get_product_ticker(product_id='ETH-USD')
	return a

##################################################################
##################################################################
##################################################################

def compare_time(date_a, date_b):
	global last_trade_date 
	# print(date_a)
	# print(date_a)
	# print(date_a)
	# date_b = str(date_a["created_at"]).replace("T", " ")
	# date_b = str(date_a["created_at"]).split("T")
	# print()
	# print(date_b)
	# print(date_b)
	# print(date_b)
	date_a = str(date_a).split("+")[0]
	date_b = str(date_b).split("+")[0]
	# print()
	# print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	# print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	# print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	# print()
	# print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	# print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	# print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	# print("#"*50)
	# z = datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S")
	if date_b < date_a:
		time.sleep(3)
		return True
	elif date_b >= date_a:
		last_trade_date = date_b
		return False

##################################################################
##################################################################
##################################################################

def round_down(num,digits):
    factor = 10.0 ** digits
    return math.floor(num * factor) / factor

def place_buy(place_buy_price):
	curr_balance = auth().get_account("85fbceca-80be-4546-8391-cba7c50b762c")["available"]
	curr_balance = float(curr_balance) - 0.2
	buy_price = str(place_buy_price)
	# buy_price = str(round_down((float(get_ticker()["price"])-0.01), 2)).split(".")
	# buy_price = float(buy_price[0] + "." + buy_price[0][0] + buy_price[0][1])

	mah_orders = [a for a in auth().get_orders(product_id="ETH-USD")]
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	print(buy_price)
	print(buy_price)
	print(buy_price)
	print(buy_price)
	print(buy_price)
	print(buy_price)
	# buy_price = str(float(get_ticker()["price"]))
	buy_quant = str(float(curr_balance)/float(buy_price))
	# buy_quant = str(round(float(buy_quant),8))
	buy_quant = str(round_down(float(buy_quant), 2))
	p = auth().buy(price=buy_price,size=buy_quant, order_type='limit', product_id='ETH-USD', post_only='true')
	print(p)

def place_sell(place_sell_price):
	sell_price = str(place_sell_price)
	# sell_price = str(float(get_ticker()["price"])+0.01).split(".")
	# sell_price = float(sell_price[0] + "." + sell_price[0][0] + sell_price[0][1])

	mah_orders = [a for a in auth().get_orders(product_id="ETH-USD")]
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	print(mah_orders)
	# sell_price = str(round_down(float(sell_price), 2))

	# sell_price = str(float(get_ticker()["price"]))
	# print("{0:.8f}".format(float(sell_quant)))
	# print(round(float(sell_quant),8))
	# print(round_down(float(sell_quant), 2))
	# print(round_down(float(sell_quant), 4))
	# print(round_down(float(sell_quant), 8))
	# sell_quant = str(round(float(sell_quant),8))
	sell_quant = float(auth().get_account("8c185a82-147d-40c7-ba82-9e95d99b6b97")["available"])
	sell_quant = str(round_down(float(sell_quant), 2))
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_price)
	print(sell_quant)
	p = auth().sell(price=sell_price,size=sell_quant, order_type='limit', product_id='ETH-USD', post_only='true')
	# p = auth().place_limit_order(product_id='ETH-USD', side='sell', price=sell_price, size=sell_quant)
	print(p)









def order_toggle(balance):
	a = ""
	if balance <= 1.00:
		a = True
	elif balance >= 5.00:
		a = False
	return a



def sort_sma(dataset, sma_appended, sma_counter):
	if sma_appended == False:
		for e in dataset[200]:
			if "sma_" in str(e):
				sma_counter+=1
				sma_inter = int(e.replace("sma_", ""))
				sma_type.append(sma_inter)
		sma_total 		= sma_counter
		sma_type.sort()
		return True
	else:
		return False
		# sma_appended 	= True














def reset_vars():
	global start_balance
	global quantity
	global start_balance
	global last_val
	global prev_val
	global buy
	global signal
	global diff
	global sma_counter
	global sma_total
	global sma_type
	global sma_appended
	global sell_thresh
	global buy_thresh
	global safety_net
	global last_price
	global init_buy
	global init_sell
	global rsi_var
	global close_var
	global mfi_var
	global std_var
	global iter_count
	global current_price
	global set_trade_date
	global last_trade_date
	global dataset_date
	global order_queued
	global order_wait
	global fucked_csv
	global lagged_update
	global prev_val
	global reset_iter
	global reset_price
	global new_high
	
	print("RESET")

	start_balance 	= 43.0
	# start_balance 	= auth().get_account("85fbceca-80be-4546-8391-cba7c50b762c")["available"]
	# quantity 		= auth().get_account("8c185a82-147d-40c7-ba82-9e95d99b6b97")["available"]
	last_val 		= 0.0
	prev_val 		= 0.0
	buy 			= False
	signal 			= "BOUGHT"
	try:
		diff 			= 100.0*(float(start_balance)/float(balance))
	except ZeroDivisionError:
		diff 			= 0

	sma_counter 	= 0
	sma_total 		= 0
	sma_type 		= []
	sma_appended 	= False
	# sell_thresh  	= 0.02
	# buy_thresh  	= 0.03
	safety_net 		= False
	last_price  	= 0.0
	init_buy 		= False
	init_sell 		= False
	rsi_var 		= "rsi"
	close_var 		= "close"
	mfi_var 		= "mfi"
	std_var 		= "std"

	iter_count 		= 0
	current_price 	= 0
	set_trade_date 	= False
	last_trade_date = 0
	dataset_date 	= 0

	order_queued 	= False
	order_wait 		= 0

	fucked_csv 		= False
	lagged_update 	= False




trade_status
last_trade_status
last_trade_iter






def get_start_balance(start_balance):
	return start_balance

def get_start_quantity(start_quantity):
	return start_quantity

def get_balance(balance):
	return balance

def get_quantity(quantity):
	return quantity

def new_trade_check(trade_status, last_trade_status, last_trade_iter):
	if trade_status == last_trade_status:
		last_trade_iter+=1
	else:
		last_trade_iter=0
	return last_trade_iter

def check_new_highs(current_price, reset_price, reset_iter):
	if current_price > reset_price:
		print("*PASSED NEW HIGH*")
		print("PRICE: 	      " + str(current_price))
		print("RESET PRICE:   " + str(reset_price))
		print("NEW HIGH:      " + str(new_high))
		
		return [reset_price, new_high, reset_iter]


################################################# DRY TESTING
################################################# DRY VARS
write_filename = "live_test_buffer_data.csv"
blank_test_slate(write_filename)
################################################# DRY VARS
################################################# DRY TESTING
reset_iter 		= 0
reset_price 	= 0
new_high 		= False
################################################# DRY VARS
################################################# DRY TESTING
start_balance 	= 43.0
quantity 		= 0.0
################################################# DRY VARS
################################################# DRY TESTING


################################################# LIVE VARS
################################################# LIVE
# start_balance 	= auth().get_account("85fbceca-80be-4546-8391-cba7c50b762c")["available"]
# quantity 			= auth().get_account("8c185a82-147d-40c7-ba82-9e95d99b6b97")["available"]
################################################# LIVE VARS
################################################# LIVE


################################################# UNIVERSAL VARS
################################################# UNIVERSAL
balance 		= start_balance
last_val 		= 0.0
prev_val 		= 0.0
buy 			= False
valuation 		= 0.0
signal 			= "BOUGHT"
try:
	diff = 100.0*(float(start_balance)/float(balance))
except ZeroDivisionError:
	diff = 0
################################################# UNIVERSAL VARS
################################################# UNIVERSAL


sma_counter 	= 0
sma_total 		= 0
sma_type 		= []
sma_appended 	= False
# sell_thresh  	= 0.02
# buy_thresh  	= 0.03
safety_net 		= False
last_price  	= 0.0
init_buy 		= False
init_sell 		= False
rsi_var 		= "rsi"
close_var 		= "close"
mfi_var 		= "mfi"
std_var 		= "std"

iter_count 		= 0
current_price 	= 0
set_trade_date 	= False
last_trade_date = 0
dataset_date 	= 0

order_queued 	= False
order_wait 		= 0

fucked_csv 		= False
lagged_update 	= False





while True:
# def dry_test(dataset):
	# print("QUEUED:" + str(order_queued))
	# print("WAIT  :" + str(order_wait))
	# print("FUCKED:" + str(fucked_csv))
	# print("LAGGED:" + str(lagged_update))

	# balance 		= float(auth().get_account("85fbceca-80be-4546-8391-cba7c50b762c")["available"])
	# quantity 		= float(auth().get_account("8c185a82-147d-40c7-ba82-9e95d99b6b97")["available"])
	# current_price 	= check_ticker()
	# current_price 	= current_price["price"]
	current_price 	= float(dataset[len(dataset)-1][close_var])
	# print(current_price)
	# valuation		= float(quantity)*float(current_price)
	valuation		= float(quantity)*current_price

	######################################################################################################################################################################################
	
	high_price_check 	= check_new_highs(current_price, reset_price, reset_iter)
	reset_price 		= high_price_check[0]
	new_high 			= high_price_check[1]
	reset_iter 			= high_price_check[2]

	######################################################################################################################################################################################

	buy 			= order_toggle(balance)
	sma_appended 	= sort_sma(dataset, sma_appended, sma_counter) 

	######################################################################################################################################################################################

	buy_thresh 	= get_sma_diff_range(dataset, sma_type)[0]  + (get_sma_diff_range(dataset, sma_type)[1] * 0.001)
	sell_thresh = get_sma_diff_range(dataset, sma_type)[1] + (get_sma_diff_range(dataset, sma_type)[1] * 0.01)

	######################################################################################################################################################################################

	test_diff 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])-float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	one_up 		= (float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002)-0.12
	one_down 	= -float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	iter_rsi 	= dataset[len(dataset)-1][rsi_var]
	iter_mfi 	= dataset[len(dataset)-1][mfi_var]
	order_date 	= dataset[len(dataset)-1]["date"]
	
	######################################################################################################################################################################################

	lagged_update 	= False

	if set_trade_date == False:
		last_trade_date = dataset[len(dataset)-1]["date"]
		set_trade_date 	= True
		# print(last_trade_date)
		# print(dataset_date)
	else:
		dataset_date 	= dataset[len(dataset)-1]["date"]
		lagged_update  	= compare_time(last_trade_date, dataset_date)


	######################################################################################################################################################################################

	if order_wait == 60:
		auth().cancel_all(product_id='ETH-USD')
		order_queued 	= False
		order_wait 		= 0
		
		if buy == True:
			buy = False
		else:
			buy = True

	######################################################################################################################################################################################
		
	z = [a for a in auth().get_orders(product_id="ETH-USD")]
	if len(z) > 0 and fucked_csv != True:
		order_queued = True
		order_wait+=1
	elif len(z) <= 0:
		order_queued = False
		order_wait=0

	# print(z)

	######################################################################################################################################################################################

	# feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1]["money_flow_index"]], sell_thresh, buy_thresh)
	
	if order_queued == False and iter_rsi != None and lagged_update == False and (init_sell == True or init_buy == True):
	
	# if order_queued == False and iter_rsi != None and init_buy == True and lagged_update == False:
		# if (float(quantity) > 0.0 and buy == True and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(dataset[len(dataset)-1][close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90))) or (buy == True and float(dataset[len(dataset)-1][close_var]) > float(last_price)*1.02):
		if (float(quantity) > 0.0 and buy == True and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90))) or (buy == True and float(current_price) > float(last_price)*1.02) or (buy == True and reset_iter == 60):

			print("PASSED CONDITION #1.a")
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			balance 	= quantity*float(current_price)
			# balance 	= quantity*float(dataset[len(dataset)-1][close_var])
			# balance 	= balance - (float(balance)*0.003)
			valuation	= 0.0
			quantity 	= 0.0
			buy 		= False
			signal 		= "SOLD"


			# place_sell(current_price)
			# place_sell(dataset[len(dataset)-1][close_var])


			# sell_price = str(float(get_ticker()["price"])+0.01)
			# sell_quant = str(quantity)
			# auth().buy(price=sell_price,size=sell_quant, order_type='limit', product_id='ETH-USD')



			last_val 	= balance
			# last_price  = float(dataset[len(dataset)-1][close_var])
			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var], sell_thresh, buy_thresh)

		######################################################################################################################################################################################

		# elif (buy == False and float(balance) >= float(start_balance) and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(dataset[len(dataset)-1][close_var]) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.2):
		elif (buy == False and float(balance) >= float(start_balance) and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(current_price) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.2):

		######################################################################################################################################################################################
		
			print("PASSED CONDITION #1.b")
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			quantity 	= float(balance)/float(current_price)
			# quantity 	= float(balance)/float(dataset[len(dataset)-1][close_var])
			balance 	= 0.0
			valuation	= float(quantity)*float(current_price)
			# valuation	= float(quantity)*float(dataset[len(dataset)-1][close_var])
			# valuation 	= valuation - (float(valuation)*0.003)
			last_val 	= float(valuation)
			buy 		= True
			signal 		= "BOUGHT"


			# place_buy(current_price)
			# place_buy(dataset[len(dataset)-1][close_var])


			# buy_price = str(float(get_ticker()["price"])-0.01)
			# buy_quant = str(float(balance)/float(buy_price))
			# auth().buy(price=buy_price,size=buy_quant, order_type='limit', product_id='ETH-USD')


			# last_price  = float(dataset[len(dataset)-1][close_var])
			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var], sell_thresh, buy_thresh)

	elif order_queued == False and iter_rsi != None and init_buy == False and init_sell == False and lagged_update == False:
		# print("SECOND IF")
		# if test_diff > sell_thresh and buy == True and float(quantity) > 0.0 and float(quantity)*float(dataset[len(dataset)-1][close_var]) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(dataset[len(dataset)-1][close_var]) and one_up < test_diff:
		if test_diff > sell_thresh and buy == True and float(quantity) > 0.0 and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price) and one_up < test_diff or (buy == True and reset_iter == 60):

		######################################################################################################################################################################################
			
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			# balance 	= float(quantity)*float(dataset[len(dataset)-1][close_var])
			balance 	= float(quantity)*float(current_price)
			# balance 	= balance - (float(balance)*0.003)
			valuation	= 0.0
			quantity 	= 0.0
			buy 		= False
			signal 		= "SOLD"


			# place_sell(current_price)
			# place_sell(dataset[len(dataset)-1][close_var])

			# sell_price = str(float(get_ticker()["price"])+0.01)
			# sell_quant = str(quantity)
			# auth().buy(price=sell_price,size=sell_quant, order_type='limit', product_id='ETH-USD')



			last_val 	= float(balance)
			last_price  = float(current_price)
			# last_price  = float(dataset[len(dataset)-1][close_var])
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var], sell_thresh, buy_thresh)
			init_sell = True

		######################################################################################################################################################################################

		elif test_diff < buy_thresh and buy == False and float(balance) >= float(start_balance) and one_down < test_diff and float(iter_rsi) < 0.2:

		######################################################################################################################################################################################

			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			quantity 	= float(balance)/float(current_price)
			# quantity 	= float(balance)/float(dataset[len(dataset)-1][close_var])
			balance 	= 0.0
			valuation	= float(quantity)*float(current_price)
			# valuation	= float(quantity)*float(dataset[len(dataset)-1][close_var])
			# valuation 	= valuation - (float(valuation)*0.003)
			last_val 	= valuation
			buy 		= True
			signal 		= "BOUGHT"


			# place_buy(current_price)
			# place_buy(dataset[len(dataset)-1][close_var])

			# buy_price = str(float(get_ticker()["price"])-0.01)
			# buy_quant = str(float(balance)/float(buy_price))
			# auth().buy(price=buy_price,size=buy_quant, order_type='limit', product_id='ETH-USD')



			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var], sell_thresh, buy_thresh)
			init_buy = True

	# print("RESET ITER:    " + str(reset_iter))
	# print("*"*50)
	# print("*"*50)

	if new_high == True:
		reset_iter+=1
	else:
		reset_iter=0
		
	if reset_iter == 60:
		reset_vars()
		new_high = False
		reset_price = current_price
		reset_iter=0

	fucked_csv = False
	iter_count+=1







def feedback(order_date, signal, price_per, balance, valuation, quantity, iter_rsi, mfi, sell_thresh, buy_thresh):
	# print("-"*50)
	# print(test_fract)
	# print(test_diff)
	# print("-"*50)
	global current_price
	print("-----------------")
	print("SIGNAL:    " + str(signal))
	print("DATE:      " + str(order_date))
	print("CURR PRICE:" + str(current_price))
	print("RSI:       " + str(iter_rsi))
	print("MFI:       " + str(mfi))
	print("PRICE PER: " + str(price_per))
	print("BALANCE:   " + str(balance))
	print("VALUATION: " + str(valuation))
	print("QUANTITY:  " + str(quantity))
	print("-----------------")
	write_results("sim_results.csv", [start_balance,balance,quantity,last_val,buy,valuation,signal,diff,sma_counter,sma_total,sma_type,sma_appended,sell_thresh,buy_thresh,safety_net,last_price,init_buy,init_sell,rsi_var,close_var,mfi_var,std_var,current_price,set_trade_date,last_trade_date,dataset_date,iter_count,order_queued,order_wait,fucked_csv,lagged_update,prev_val
])

##################################################################
##################################################################
##################################################################

def trade_file_or_array(file_or_array, datas):
	a = []
	if file_or_array == "file":
		convert_csv(datas)
		# datas 	= str(datas) + "_header"
		a 	= pd.read_csv(datas + ".csv", parse_dates=True, infer_datetime_format=True)
		a.columns = ['date','low','high','open','close','volume']
	elif file_or_array == "array":