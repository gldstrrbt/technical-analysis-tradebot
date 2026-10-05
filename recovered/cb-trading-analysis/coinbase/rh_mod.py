import os, json, requests, time, csv, matplotlib, mpl_finance, random
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
import datetime as datetime
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
	print(auth_client)
	# Use the sandbox API (requires a different set of API access credentials)
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
	MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name='money_flow_index')
	df = df.join(MFI)
	return df

##################################################################
##################################################################
##################################################################


def check_buy_sell():
	a 			= 0
	aa 			= 0
	
	b 			= 0
	bb 			= 0
	
	scale_tip 	= ""
	
	c = public_client.get_product_trades(product_id='ETH-USD')
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

##################################################################
##################################################################
##################################################################

def backtest(dataset):
	start_balance 	= 1000.0
	balance 		= start_balance
	quantity 		= 0.0
	last_val 		= 0.0
	buy 			= False
	valuation 		= 0.0
	signal 			= "BOUGHT"
	diff 			= 100.0*(float(start_balance)/float(balance))
	sma_counter 	= 0
	sma_total 		= 0
	sma_type 		= []
	sma_appended 	= False
	sell_thresh  	= 0.02
	buy_thresh  	= 0.03
	safety_net 		= False
	last_price  	= 0.0
	init_buy 		= False
	rsi_var 		= "rsi"
	close_var 		= "close"
	mfi_var 		= "money_flow_index"
	std_var 		= "std"



	if sma_appended == False:
		for e in dataset[200]:
			if "sma_" in str(e):
				sma_counter+=1
				sma_inter = int(e.replace("sma_", ""))
				sma_type.append(sma_inter)
		sma_total = sma_counter
		sma_type.sort()
		sma_appended = True

	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	# strat_support_resist(dataset, sma_type)
	buy_thresh = 0
	sell_thresh = 0
	# buy_thresh = get_sma_diff_range(dataset, sma_type)[0]
	# sell_thresh = get_sma_diff_range(dataset, sma_type)[1]
	# buy_thresh = get_sma_diff_range_from_center(dataset, sma_type)[0]
	# sell_thresh = get_sma_diff_range_from_center(dataset, sma_type)[1]
	test_end 		= len(dataset) 
	test_start 		= test_end-100000
	# -4.960080557818564
	# 4.9140145637349075

	tt = []
	yy = []
	for e, d in enumerate(dataset):
		# print("----------")
		# print("----------")
		# print("----------")
		# print("----------")
		# print(dataset[200])
	# while test_start < test_end:
		test_start = test_start
		# print(test_start)
		# d = dataset[test_start]
		# tt.append(d)
		yy.append(d)
		try:
			# buy_thresh = get_sma_diff_range(yy, sma_type)[0]
			# sell_thresh = get_sma_diff_range(yy, sma_type)[1]
			buy_thresh = get_sma_diff_range(yy, sma_type)[0]  + (get_sma_diff_range(yy, sma_type)[1] * 0.001)
			# print("BUY THRESH: " + str(buy_thresh))
			sell_thresh = get_sma_diff_range(yy, sma_type)[1] + (get_sma_diff_range(yy, sma_type)[1] * 0.01)
			# print("SELL THRESH: " + str(sell_thresh))
			# print(buy_thresh)
			# print(sell_thresh)
		except:
			pass
		# print(d)
		# print(d["sma_" + str(sma_type[1]))
		# print(d["sma_" + str(sma_type[1]))
		# test_fract 	= float(d["sma_" + str(sma_type[1])])/float(d["sma_" + str(sma_type[2])])
		# test_diff 	= float(d["sma_" + str(sma_type[1])])-float(d["sma_" + str(sma_type[2])])
		if e >= int(sma_type[1]):
			# print(sma_type)
			# print(sma_type)
			# print(sma_type)
			# print(d["sma_" + str(sma_type[0])])

			test_fract 	= float(d["sma_" + str(sma_type[0])])/float(d["sma_" + str(sma_type[1])])
			test_diff 	= float(d["sma_" + str(sma_type[0])])-float(d["sma_" + str(sma_type[1])])
			one_up 		= (float(d["sma_" + str(sma_type[1])])*0.002)-0.4
			one_down 	= -float(d["sma_" + str(sma_type[1])])*0.002
			iter_rsi 	= d[rsi_var]
			iter_mfi 	= d[rsi_var]
			rand_order  = bool(random.getrandbits(1))

			# if one_up < test_diff:	
			# 	print("-"*50)
			# 	print("TEST DIFF: " + str(test_diff))
			# 	print("ONE UP:    " + str(one_up))
			# 	print("-"*50)
			# order_date 	= d["date"]
			order_date 	= d["date"]
			# print(order_date)
			# print(iter_rsi)
			# print(iter_mfi)
			# print("#"*50)
			# if test_fract > 1.007 and buy == True and float(start_balance) > 0.0:
			# if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val < quantity*float(d[close_var]):
			# if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val < quantity*float(d[close_var]) and one_up < test_diff:
			

			######################################################################################################################################################################################
			######################################################################################################################################################################################
			# if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff:
			if iter_rsi != None and init_buy == True:
				# if (test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff) or (buy == True and quantity*float(d[close_var]) > float(start_balance) and float(iter_rsi) > 80.0 and last_val*1.002 < quantity*float(d[close_var])):
				# if (test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff) or (buy == True and quantity*float(d[close_var]) > float(start_balance) and float(iter_rsi) > 90.0 and last_val < quantity*float(d[close_var])):
				# if (test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff) or (buy == True and quantity*float(d[close_var]) > float(start_balance) and float(iter_rsi) > 90.0 and last_val*1.002 < quantity*float(d[close_var])):
				# if (quantity*float(d[close_var]) < float(start_balance)*1.0 and safety_net == False and buy == True ):
				# 	print(buy_thresh)
				# 	print(sell_thresh)
				# 	print(test_diff)
				# 	print(iter_rsi)
				# 	balance 	= quantity*float(d[close_var])
				# 	# balance 	= balance - (float(balance)*0.003)
				# 	valuation	= 0.0
				# 	quantity 	= 0.0
				# 	buy 		= False
				# 	signal 		= "SOLD"
				# 	last_val 	= balance
				# 	safety_net  = True
				# 	feedback(order_date, signal, d[close_var], balance, valuation, quantity)

				######################################################################################################################################################################################
				######################################################################################################################################################################################
				
				# if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and one_up < test_diff:
				# if (test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff) or (buy == True and quantity*float(d[close_var]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and float(iter_rsi) > 90.0):
				# if buy == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0) or (float(d["money_flow_index"]) > float(iter_rsi) and float(iter_rsi) > 70 and d["neg_flow"] != 0)):
				# if buy == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0)):
				# if buy == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90)):
				# if (buy == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90))) or (buy == True and last_val - (last_val*0.02) > quantity*float(d[close_var])):
				if (buy == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90))) or (buy == True and float(d[close_var]) > last_price*1.02):
				# if buy == True and rand_order == True and quantity*float(d["close"]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0)):
				# if buy == True and quantity*float(d["close"]) > start_balance and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0)):
				# if buy == True and quantity*float(d[close_var]) > start_balance and last_val*1.002 < quantity*float(d[close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0) or (float(d["money_flow_index"]) > float(iter_rsi) and float(iter_rsi) > 70 and d["neg_flow"] != 0) or (float(d[close_var]) < last_price+(last_price*0.1))):
					print(buy_thresh)
					print(sell_thresh)
					print(test_diff)
					print(iter_rsi)
					balance 	= quantity*float(d[close_var])
					# balance 	= balance - (float(balance)*0.003)
					valuation	= 0.0
					quantity 	= 0.0
					buy 		= False
					signal 		= "SOLD"
					last_val 	= balance
					last_price  = float(d[close_var])
					feedback(order_date, signal, d[close_var], balance, valuation, quantity, iter_rsi, d["money_flow_index"], init_buy, sma_appended, sma_type, test_diff, one_up, one_down)
				# elif test_fract < 0.990 and buy == False and float(d[close_var]) > 0.0:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and balance >= 1000:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and balance >= 1000  and one_down < test_diff:
				
				######################################################################################################################################################################################
				######################################################################################################################################################################################
				# elif test_diff < buy_thresh and buy == False and balance >= 1000 and one_down < test_diff:
				elif (buy == False and float(balance) >= 1000 and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(d[close_var]) < last_price-(last_price*0.1)))) or (buy == False and float(iter_rsi) < 0.2):
				# elif (buy == False and float(balance) >= 1000 and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(d[close_var]) < last_price-(last_price*0.1)))) or (buy == False and float(iter_rsi) < 0.2):
				# elif buy == False and float(balance) >= 1000 and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 12.0) or (float(d[close_var]) < last_price-(last_price*0.05))):
				# elif buy == False and float(balance) >= 1000 and rand_order == False and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 12.0) or (float(d[close_var]) < last_price-(last_price*0.05))):
				######################################################################################################################################################################################
				######################################################################################################################################################################################
				
				# elif test_fract < 0.990 and buy == False and float(d[close_var]) > 0.0 and one_down < test_diff:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and d[close_var] != 0.06:
					print(buy_thresh)
					print(sell_thresh)
					print(test_diff)
					print(iter_rsi)
					quantity 	= balance/float(d[close_var])
					balance 	= 0.0
					valuation	= quantity*float(d[close_var])
					# valuation 	= valuation - (float(valuation)*0.003)
					last_val 	= valuation
					buy 		= True
					signal 		= "BOUGHT"
					last_price  = float(d[close_var])
					feedback(order_date, signal, d[close_var], balance, valuation, quantity, iter_rsi, d["money_flow_index"], init_buy, sma_appended, sma_type, test_diff, one_up, one_down)

			# else:
			elif iter_rsi != None and init_buy == False:
				if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and last_val*1.002 < quantity*float(d[close_var]) and one_up < test_diff:
				######################################################################################################################################################################################
				######################################################################################################################################################################################
				
				# if test_diff > sell_thresh and buy == True and quantity*float(d[close_var]) > float(start_balance) and one_up < test_diff:
					print(buy_thresh)
					print(sell_thresh)
					print(test_diff)
					print(iter_rsi)
					balance 	= quantity*float(d[close_var])
					# balance 	= balance - (float(balance)*0.003)
					valuation	= 0.0
					quantity 	= 0.0
					buy 		= False
					signal 		= "SOLD"
					last_val 	= balance
					last_price  = float(d[close_var])
					feedback(order_date, signal, d[close_var], balance, valuation, quantity, iter_rsi, d["money_flow_index"], init_buy, sma_appended, sma_type, test_diff, one_up, one_down, init_buy, sma_appended, sma_type, test_diff, one_up, one_down)
				# elif test_fract < 0.990 and buy == False and float(d[close_var]) > 0.0:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and balance >= 1000:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and balance >= 1000  and one_down < test_diff:
				
				######################################################################################################################################################################################
				######################################################################################################################################################################################
				# elif test_diff < buy_thresh and buy == False and balance >= 1000 and one_down < test_diff and float(iter_rsi) < 0.12:
				elif test_diff < buy_thresh and buy == False and balance >= 1000 and one_down < test_diff and float(iter_rsi) < 0.2:
				######################################################################################################################################################################################
				######################################################################################################################################################################################
				
				# elif test_fract < 0.990 and buy == False and float(d[close_var]) > 0.0 and one_down < test_diff:
				# elif test_diff < buy_thresh and buy == False and float(d[close_var]) > 0.0 and d[close_var] != 0.06:
					print(buy_thresh)
					print(sell_thresh)
					print(test_diff)
					print(iter_rsi)
					quantity 	= balance/float(d[close_var])
					balance 	= 0.0
					valuation	= quantity*float(d[close_var])
					# valuation 	= valuation - (float(valuation)*0.003)
					last_val 	= valuation
					buy 		= True
					signal 		= "BOUGHT"
					last_price  = float(d[close_var])
					feedback(order_date, signal, d[close_var], balance, valuation, quantity, iter_rsi, d["money_flow_index"], init_buy, sma_appended, sma_type, test_diff, one_up, one_down)
					init_buy = True



def feedback(order_date, signal, price_per, balance, valuation, quantity, iter_rsi, mfi, init_buy, sma_appended, sma_type, test_diff, one_up, one_down):
	# print("-"*50)
	# print(test_fract)
	# print(test_diff)
	# print("-"*50)
	print("-------------------------------")
	print("-----------------")
	print("DATE:      " + str(order_date))
	print("SIGNAL:    " + str(signal))
	print("RSI:       " + str(iter_rsi))
	print("MFI:       " + str(mfi))
	print("PRICE PER: " + str(price_per))
	print("BALANCE:   " + str(balance))
	print("VALUATION: " + str(valuation))
	print("QUANTITY:  " + str(quantity))
	print("")
	print("INIT BUY:    " + str(init_buy))
	print("SMA APPEND:  " + str(sma_appended))
	print("SMA TYPE:    " + str(sma_type))
	print("TEST DIFF:   " + str(test_diff))
	print("ONE UP:   	" + str(one_up))
	print("ONE DOWN:    " + str(one_down))
	print("-----------------")

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
		# a 	= pd.DataFrame(datas, columns={'date', 'open', 'high', 'low', 'close', 'volume'})
		a 	= pd.DataFrame(datas, columns={'date','low','high','open','close','volume'})
	return a

##################################################################
##################################################################
##################################################################

# check_buy_sell()
# get_ticker()

def test_area():
	# a 		= get_hist(60)
	# print(a)
	# b 		= trade_file_or_array("array", a)
	# b 		= trade_file_or_array("file", "20190122_212440___data")
	# b 		= trade_file_or_array("file", "buffer_data")
	# b 		= trade_file_or_array("file", "20190122_145449___data")
	# b 		= trade_file_or_array("file", "20190122_142459___data")
	# b 		= trade_file_or_array("file", "20190122_194125___data")
	# b 		= trade_file_or_array("file", "20190122_185923___data")
	# b 		= trade_file_or_array("file", "20190122_235349___data")
	b 		= trade_file_or_array("file", "buffer_data")
	dataset = moving_average_alt(b, 1)
	dataset = moving_average_alt(dataset, 6)
	dataset = moving_average_alt(dataset, 12)
	dataset = relative_strength_index(dataset, 14)
	dataset = money_flow_index(dataset, 14)
	dataset = macd(dataset, 12, 26)
	dataset = standard_deviation(dataset, 21)
	
	dataset = dataset.to_json(orient='records')
	dataset = json.loads(dataset)

	backtest(dataset)

##################################################################
##################################################################
##################################################################

time_inc = 0
def test_loop():
	start = 1
	
	while True:
		
		csv_open_test = open("csv_test.csv", "a+")
		writer_test   = csv.writer(csv_open_test)

		if start != 1:        
		    do_run = input('Restart?  y/n:')
		    if do_run == 'y':
		        pass
		    elif do_run == 'n':
		        break
		    else: 
		        print('Invalid input')
		        continue
		a = get_ticker()
		print(a)
		time_inc+=1
		# print('Doing stuff!!!')
		# if start == 1:
		    # start = 0

##################################################################
##################################################################
##################################################################

# test_loop()
test_area()