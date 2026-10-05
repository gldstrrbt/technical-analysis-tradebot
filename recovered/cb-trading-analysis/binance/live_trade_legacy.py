import os, json, requests, time, csv, matplotlib, mpl_finance, random, math, new_history
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

###########################################################################
public_client = cbpro.PublicClient()
###########################################################################
binance_api_key = os.getenv("BINANCE_API_KEY", "")
binance_api_secret = os.getenv("BINANCE_API_SECRET", "")
###########################################################################

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


def check_buy_sell():
	global product_sym
	a 			= 0
	aa 			= 0
	
	b 			= 0
	bb 			= 0
	
	scale_tip 	= ""
	
	c = public_client.get_product_trades(product_id=product_sym+'-USD')
	for d in c:
		try:	
			if d["side"] == "buy":
				a+=1
				aa+=float(d["size"])
			else:
				b+=1
				b+=float(d["size"])
		except:
			pass
	print(b, bb)
	print(a, aa)

##################################################################
##################################################################
##################################################################

def get_ticker():
	global product_sym
	a = public_client.get_product_ticker(product_id=product_sym+'-USD')
	# a = auth().get_product_ticker(product_id='ETH-USD')
	return a

##################################################################
##################################################################
##################################################################

def get_hist(timing):
	global product_sym
	# a = public_client.get_product_historic_rates('ETH-USD', granularity=timing)
	a = auth().get_product_historic_rates(product_sym+'-USD', granularity=timing)
	return a

##################################################################
##################################################################
##################################################################

def my_fills():
	global product_sym
	a = auth()
	b = a.get_fills(product_sym+"-USD")
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
	global product_sym
	a = auth().get_product_ticker(product_id=product_sym+'-USD')
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
	print("#"*50)
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

def place_buy(current_price, product_sym, balance):
	print(current_price, product_sym, balance)
	
	buy_price = float(current_price)
	
	print(buy_price)

	buy_quant = float(balance)/buy_price
	# buy_quant = str(round(float(buy_quant),8))
	buy_quant = float(str(round_down(float(buy_quant), 2)))

	print(buy_quant)
	# buy_quant = str(round(float(buy_quant),8))
	buy_quant = str(round_down(float(buy_quant), 2))
	p = auth().buy(price=buy_price,size=buy_quant, order_type='limit', product_id=product_sym+'-USD', post_only='true')
	print(p)

def place_sell(current_price, product_sym, quantity):
	sell_price = str(current_price)
	# sell_price = str(float(get_ticker()["price"])+0.01).split(".")
	# sell_price = float(sell_price[0] + "." + sell_price[0][0] + sell_price[0][1])

	# sell_price = str(round_down(float(sell_price), 2))

	# sell_price = str(float(get_ticker()["price"]))
	# print("{0:.8f}".format(float(sell_quant)))
	# print(round(float(sell_quant),8))
	# print(round_down(float(sell_quant), 2))
	# print(round_down(float(sell_quant), 4))
	# print(round_down(float(sell_quant), 8))
	# sell_quant = str(round(float(sell_quant),8))
	sell_quant = quantity
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
	p = auth().sell(price=sell_price,size=sell_quant, order_type='limit', product_id=product_sym+'-USD', post_only='true')
	# p = auth().place_limit_order(product_id=product_sym+'-USD', side='sell', price=sell_price, size=sell_quant)
	print(p)









def check_balance(balance):
	a = ""
	if balance <= 1.00:
		a = True
	elif balance >= 5.00:
		a = False
	return a



def sort_sma(dataset, sma_appended):
	global sma_counter
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






































# start_balance 	= 1000.0
# product_sym 	= "LTC"
product_sym 	= "LTC"
num_days_data 	= 1
ltc_account = os.getenv("COINBASE_LTC_ACCOUNT_ID", "")
eth_account = os.getenv("COINBASE_ETH_ACCOUNT_ID", "")
usd_account = os.getenv("COINBASE_USD_ACCOUNT_ID", "")
account_in_use 	= ""

start_balance 	= float(auth().get_account(usd_account)["available"])
balance 		= start_balance
quantity 		= 0.0

if product_sym == "LTC":
	quantity 		= auth().get_account(ltc_account)["available"]
	account_in_use 	= ltc_account

elif product_sym == "ETH":
	quantity 		= auth().get_account(eth_account)["available"]
	account_in_use 	= eth_account
	
started 		= False

last_val 		= 0.0
prev_val 		= 0.0
buy 			= False
valuation 		= 0.0
signal 			= "BOUGHT"
diff 			= 100.0*(float(start_balance)/float(balance))
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

cancel_id 		= ""

def backtest(dataset):
	global started 	
	global start_balance 	
	global balance 		
	global quantity 		
	global last_val 		
	global buy 			
	global valuation 		
	global signal 			
	global diff 			
	global sma_counter 	
	global sma_total 		
	global sma_type 		
	global sma_appended 	
	# global sell_thresh  	
	# global buy_thresh  	
	global safety_net 		
	global last_price  	
	global init_buy 		
	global init_sell 		
	global rsi_var 		
	global close_var 		
	global mfi_var 		
	global std_var 	
	global current_price 	
	global set_trade_date 	
	global last_trade_date 
	global dataset_date 	
	global iter_count 	
	global order_queued 	
	global order_wait 	
	global fucked_csv 	
	global lagged_update
	global prev_val

	global product_sym 	
	global num_days_data 	
	global ltc_account 	
	global eth_account 	
	global usd_account 	
	global account_in_use

	global cancel_id

	print("QUEUED:" + str(order_queued))
	print("WAIT  :" + str(order_wait))
	print("FUCKED:" + str(fucked_csv))
	print("LAGGED:" + str(lagged_update))
	print("BUY:" + str(buy))

	balance 		= float(auth().get_account(usd_account)["available"])
	quantity 		= float(auth().get_account(account_in_use)["available"])
	current_price 	= check_ticker()
	current_price 	= current_price["price"]
	valuation		= float(quantity)*float(current_price)

	if sma_appended == False:
		for e in dataset[200]:
			if "sma_" in str(e):
				sma_counter+=1
				sma_inter = int(e.replace("sma_", ""))
				sma_type.append(sma_inter)
		sma_total = sma_counter
		sma_type.sort()
		sma_appended = True

	######################################################################################################################################################################################

	buy 			= check_balance(balance)
	# sma_appended 	= sort_sma(dataset, sma_appended) 

	######################################################################################################################################################################################

	# buy_thresh 	= 0
	# sell_thresh = 0

	# try:
	buy_thresh 	= float(get_sma_diff_range(dataset, sma_type)[0]  + (get_sma_diff_range(dataset, sma_type)[1] * 0.001))
	sell_thresh = float(get_sma_diff_range(dataset, sma_type)[1] + (get_sma_diff_range(dataset, sma_type)[1] * 0.01))
	# except:
		# pass

	######################################################################################################################################################################################

	# test_fract 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])/float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	test_diff 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])-float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	one_up 		= float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	one_down 	= -float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	iter_rsi 	= float(dataset[len(dataset)-1][rsi_var])
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
		# auth().cancel_all(product_id=product_sym+"-USD")
		auth().cancel_order(cancel_id)
		order_queued 	= False
		order_wait 		= 0
		cancel_id 		= ""
		
		if buy == True:
			buy = False
		elif buy == False:
			buy = True

	######################################################################################################################################################################################
		
	z = [a for a in auth().get_orders(product_id=product_sym+"-USD")]
			
	if len(z) > 2 and fucked_csv != True:
		# for k in auth().get_orders(product_id=product_sym+"-USD"):
		# 	if str(k["id"]) != "3e69fee4-80c5-449e-9fd4-3083447fdf41" and str(k["id"]) != "28872659-e271-44b0-bac4-efc8ec55df8f":
		order_queued 	= True
		cancel_id 		= str(z[0]["id"]) 
		order_wait+=1
	elif len(z) <= 2:
		order_queued = False
		order_wait=0

	######################################################################################################################################################################################

	# feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1]["money_flow_index"])
	
	if order_queued == False and float(iter_rsi) != None and fucked_csv == False and (init_sell == True or init_buy == True):
		print("PASSED CONDITION #1")

		print("CONDITIONS FOR A:")
		print(float(quantity) > 0.0) 
		print(buy == True) 
		print(float(quantity)*float(current_price) > float(start_balance)) 
		print(float(last_val)*1.002 < float(quantity)*float(current_price)) 
		print("+++AND+++")
		print(test_diff > sell_thresh)
		print(one_up < test_diff)
		print("---OR---")
		print(float(iter_rsi) > 0.90) 
		print("---OR---")
		print(buy == True) 
		print(float(current_price) > float(last_price)*1.02)
		print("-"*20)
		print("-"*20)
		print("-"*20)

		print("CONDITIONS FOR B:")
		print(buy == False) 
		print(float(balance) >= float(start_balance)) 
		print(test_diff < buy_thresh) 
		print(one_down < test_diff) 
		print("---OR---")
		print(float(iter_rsi) < 0.12)
		print(float(current_price) < float(last_price)-(float(last_price)*0.1)) 
		print(buy == False) 
		print(float(iter_rsi) < 0.2)

		# if order_queued == False and iter_rsi != None and init_buy == True and lagged_update == False:
		if (float(quantity) > 0.0 and buy == True and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price) and ((float(test_diff) > float(sell_thresh) and float(one_up) < float(test_diff)) or (float(iter_rsi) > 0.90))) or (buy == True and float(current_price) > float(last_price)*1.02):

			print("PASSED CONDITION #1.a")
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			buy 		= False
			signal 		= "SOLD"
			last_val 	= balance
			last_price  = float(current_price)


			place_sell(current_price, product_sym, quantity)

			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var])

		######################################################################################################################################################################################

		elif (buy == False and float(balance) >= float(start_balance) and ((float(test_diff) < float(buy_thresh) and float(one_down) < float(test_diff)) or (float(iter_rsi) < 0.12) or (float(current_price) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.2):

		######################################################################################################################################################################################
		
			print("PASSED CONDITION #1.b")
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			quantity 	= float(balance)/float(current_price)
			# valuation 	= valuation - (float(valuation)*0.003)
			last_val 	= float(valuation)
			buy 		= True
			signal 		= "BOUGHT"

			place_buy(dcurrent_price, product_sym, balance)

			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var])

	elif order_queued == False and float(iter_rsi) != None and init_buy == False and init_sell == False and lagged_update == False:
		print("*"*50)
		print("*"*50)
		print("FIRST SELL")
		print("float(test_diff) > float(sell_thresh)")
		print(float(test_diff) > float(sell_thresh))
		print("buy == True")
		print(buy == True)
		print("float(quantity) > 0.0")
		print(float(quantity) > 0.0)
		print("float(quantity)*float(dataset[len(dataset)-1][close_var])")
		print(float(quantity)*float(dataset[len(dataset)-1][close_var]) > float(start_balance))
		print("float(quantity)*float(dataset[len(dataset)-1][close_var]) > float(start_balance)")
		print("float(last_val)*1.002 < float(quantity)*float(dataset[len(dataset)-1][close_var])")
		print(float(last_val)*1.002 < float(quantity)*float(dataset[len(dataset)-1][close_var]))
		print("float(one_up) < float(test_diff)")
		print(float(one_up) < float(test_diff))
		print("*"*50)
		print("*"*50)
		if float(test_diff) > float(sell_thresh) and buy == True and float(quantity) > 0.0 and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price) and float(one_up) < float(test_diff):

		######################################################################################################################################################################################
			
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			balance 	= float(quantity)*float(current_price)
			# balance 	= balance - (float(balance)*0.003)
			quantity 	= 0.0
			buy 		= False
			signal 		= "SOLD"


			place_sell(current_price, product_sym, quantity)

			# sell_price = str(float(get_ticker()["price"])+0.01)
			# sell_quant = str(quantity)
			# auth().buy(price=sell_price,size=sell_quant, order_type='limit', product_id='ETH-USD')



			last_val 	= float(balance)
			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var])
			init_sell = True

		######################################################################################################################################################################################

		elif float(test_diff) < float(buy_thresh) and buy == False and float(balance) >= float(start_balance) and float(one_down) < float(test_diff) and float(iter_rsi) < 0.2:

		######################################################################################################################################################################################

			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			quantity 	= float(balance)/float(current_price)
			balance 	= 0.0
			# valuation 	= valuation - (float(valuation)*0.003)
			last_val 	= valuation
			buy 		= True
			signal 		= "BOUGHT"


			place_buy(current_price, product_sym, balance)

			# buy_price = str(float(get_ticker()["price"])-0.01)
			# buy_quant = str(float(balance)/float(buy_price))
			# auth().buy(price=buy_price,size=buy_quant, order_type='limit', product_id='ETH-USD')



			last_price  = float(current_price)
			feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1][mfi_var])
			init_buy = True



	if lagged_update == True:
		print("#"*50)
		print("STATUS: NO MATCH IN DATES")
		print("#"*50)
		print(current_price)
		print(last_trade_date)
		print(dataset_date)
		print("#"*50)
		z = [a for a in auth().get_orders(product_id=product_sym+"-USD")]
		if order_wait > 1:
			order_wait-=1
			# order_wait-=1
		# time.sleep(2)
		# pass
	
	elif lagged_update == False:
		print("#"*50)
		print("STATUS: GOOD")
		print(str(round_down((float(get_ticker()["price"])-0.01), 2)))
		print(str(round_down((float(get_ticker()["price"])-0.01), 2)))
		print("#"*50)
		print(current_price)
		print(last_trade_date)
		print(dataset_date)
		print("#"*50)
		print()
		print("#"*50)
		print("#"*50)
		print("STATS")
		# (buy == False and float(balance) >= float(start_balance) and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(dataset[len(dataset)-1][close_var]) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float()
		print("----------------------------------------------")
		print("INIT BUY:    " + str(init_buy))
		print("INIT SELL:   " + str(init_sell))
		print("SMA APPEND:  " + str(sma_appended))
		print("SMA TYPE:    " + str(sma_type))
		print("TEST DIFF:   " + str(test_diff))
		print("ONE UP:   	" + str(one_up))
		print("ONE DOWN:    " + str(one_down))
		print("-------------------------------")
		print("SIGNAL:      " + str(buy))
		print("START BAL:   " + str(start_balance))
		print("PRICE:       " + str(current_price))
		print("BALANCE:     " + str(balance))
		print("VALUATION:   " + str(float(dataset[len(dataset)-1]["close"])*float(quantity)))
		print("LAST VAL:    " + str(last_val))
		print("QUANTITY:    " + str(quantity))
		print("DATE:        " + str(dataset[len(dataset)-1]["date"]))
		print("OPEN:        " + str(dataset[len(dataset)-1]["open"]))
		print("HIGH:        " + str(dataset[len(dataset)-1]["high"]))
		print("LOW:         " + str(dataset[len(dataset)-1]["low"]))
		print("CLOSE:       " + str(dataset[len(dataset)-1]["close"]))
		print("VOLUME:      " + str(dataset[len(dataset)-1]["volume"]))
		print("SMA 1:       " + str(dataset[len(dataset)-1]["sma_1"]))
		print("SMA 6:       " + str(dataset[len(dataset)-1]["sma_6"]))
		print("SMA 20:      " + str(dataset[len(dataset)-1]["sma_20"]))
		print("RSI:         " + str(iter_rsi))
		print("MFI:         " + str(dataset[len(dataset)-1]["mfi"]))
		print("STD:         " + str(dataset[len(dataset)-1]["std"]))
		print("MACD:        " + str(dataset[len(dataset)-1]["macd"]))
		print("BUY THRESH:  " + str(buy_thresh))
		print("SELL THRESH: " + str(sell_thresh))
		print("#"*50)
		print("#"*50)
		print()
		print("#"*50)
		time.sleep(10)

	fucked_csv = False
	iter_count+=1






