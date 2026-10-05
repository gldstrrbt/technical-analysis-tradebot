import os, json, requests, time, csv, matplotlib, mpl_finance, random, math, new_history, pytz
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

from binance.client import Client

######################################################################################################################################################
######################################################################################################################################################
def auth():
	binance_api_key = os.getenv("BINANCE_API_KEY", "")
	binance_api_secret = os.getenv("BINANCE_API_SECRET", "")
	client = Client(binance_api_key, binance_api_secret)
	return client
######################################################################################################################################################
######################################################################################################################################################
def moving_average_alt(df, n):
	compiled_sma 	= pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df
######################################################################################################################################################
######################################################################################################################################################
def get_sma_diff_range(dataset, sma_type):
	diffs 			= []
	dataset_end 	= len(dataset)
	dataset_start 	= dataset_end-75
	# dataset_start = dataset_end-100
	while dataset_start < dataset_end:
		a = dataset[dataset_start]
		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
		diffs.append(float(test_diff))
		dataset_start += 1
	diffs.sort()
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
######################################################################################################################################################
######################################################################################################################################################
def relative_strength_index(df, n):
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
######################################################################################################################################################
######################################################################################################################################################
def money_flow_index(df, n):
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
######################################################################################################################################################
######################################################################################################################################################
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
######################################################################################################################################################
######################################################################################################################################################
def product_ticker(product_sym):
	a = auth().get_ticker(symbol=product_sym)
	return a
######################################################################################################################################################
######################################################################################################################################################
def standard_deviation(df, n):
	df = df.join(pd.Series(df['close'].rolling(n, min_periods=n).std(), name='std'))
	return df
######################################################################################################################################################
######################################################################################################################################################
def macd(df, n_fast, n_slow):
	ema_fast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
	ema_slow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
	macd = pd.Series(ema_fast - ema_slow, name='macd')
	macd_sign = pd.Series(macd.ewm(span=9, min_periods=9).mean(), name='macd_sign_' + str(n_fast) + '_' + str(n_slow))
	macd_diff = pd.Series(macd - macd_sign, name='macd_diff_' + str(n_fast) + '_' + str(n_slow))
	df = df.join(macd)
	df = df.join(macd_sign)
	df = df.join(macd_diff)
	return df
######################################################################################################################################################
######################################################################################################################################################
def convert_csv(filename):
	a = open(str(filename)+".csv", "r+")
	b = csv.reader(a)
	
	c = open(str(filename)+"_header.csv", "w+")
	d = csv.writer(c)
	d.writerow(["date", "open", "high", "low", "close", "volume"])

	for e in b:
		d.writerow(e)
######################################################################################################################################################
######################################################################################################################################################
def convert_json(json_array, filename):
	a = open(str(filename)+".csv", "w+")
	b = csv.writer(a)
	
	for c in json_array:	
		b.writerow([c[0], c[1], c[2], c[3], c[4], c[5]])
######################################################################################################################################################
######################################################################################################################################################
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
######################################################################################################################################################
######################################################################################################################################################
def round_down(num,digits):
    factor = 10.0 ** digits
    return math.floor(num * factor) / factor
######################################################################################################################################################
######################################################################################################################################################
def place_buy(current_price, product_sym, balance, buy, last_val, quantity, last_price):
	print(current_price, product_sym, balance)
	buy_price = float(current_price)
	
	print(buy_price)

	buy_quant = (float(balance)-1)/buy_price
	buy_quant = float(str(buy_quant).split(".")[0])

	print(buy_quant)
	print("------------------------------------------------------")
	print("BUY")
	print("------------------------------------------------------")
	p = auth().order_market_buy(symbol=product_sym, quantity=buy_quant)
	print(p)
	quantity 	= float(balance)/float(current_price)
	last_val 	= float(quantity)*float(current_price)
	last_price  = float(current_price)
	buy 		= True
	print("BUY == " + str(buy))
	return [buy, last_val, quantity, last_price]
	
######################################################################################################################################################
######################################################################################################################################################
def place_sell(current_price, product_sym, quantity, buy):
	print("------------------------------------------------------")
	print(quantity)
	quantity = float(str(quantity).split(".")[0])
	print(quantity)
	print("------------------------------------------------------")
	print("SELL")
	print("------------------------------------------------------")
	p = auth().order_market_sell(symbol=product_sym, quantity=float(quantity))
	print(p)
	buy = False
	print("BUY == " + str(buy))
	return buy

######################################################################################################################################################
######################################################################################################################################################
def check_balance(balance):
	a = ""
	if balance <= 4.00:
		a = True
	elif balance >= 5.00:
		a = False
	return a
######################################################################################################################################################
######################################################################################################################################################
product_sym 	= "ETCUSDT"
start_balance 	= float(auth().get_asset_balance(asset="USDT")["free"])
balance 		= start_balance
quantity 		= float(auth().get_asset_balance(asset="ETC")["free"])

# if product_sym == "LTC":
# 	quantity 		= auth().get_account(ltc_account)["available"]
# 	account_in_use 	= ltc_account

# elif product_sym == "ETH":
# 	quantity 		= auth().get_account(eth_account)["available"]
# 	account_in_use 	= eth_account

started 		= False
last_val 		= 0.0
prev_val 		= 0.0
buy 			= False
valuation 		= 0.0
signal 			= "BOUGHT"
diff 			= 100.0*(float(start_balance)/float(balance))
sma_counter 	= 0
sma_type 		= []
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

current_price 	= 0
set_trade_date 	= False
last_trade_date = 0
dataset_date 	= 0

def backtest(dataset):
	global start_balance 	
	global balance 		
	global quantity 		
	global last_val 		
	global buy 			
	global valuation 		
	global signal 			
	global diff 			
	global sma_counter 	
	global sma_type 		
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
	global order_queued 	
	global lagged_update
	global prev_val

	global product_sym 	
	global num_days_data 	
	global ltc_account 	
	global eth_account 	
	global usd_account 	
	global account_in_use
	global started

	balance 	= float(auth().get_asset_balance(asset="USDT")["free"])
	quantity 	= float(auth().get_asset_balance(asset="ETC")["free"])
	current_price 	= product_ticker(product_sym)
	current_price 	= float(current_price["lastPrice"])
	valuation		= float(quantity)*current_price

	if started == False:
		last_val = valuation
		started = True

	print("BALANCE:  " + str(balance))
	print("QUANTITY: " + str(quantity))
	print("QUEUED:" + str(order_queued))
	print("LAGGED:" + str(lagged_update))
	print("BUY:" + str(buy))
	print(current_price)

	######################################################################################################################################################################################

	buy 		= check_balance(balance)

	######################################################################################################################################################################################

	buy_thresh 	= float(get_sma_diff_range(dataset, sma_type)[0]  + (get_sma_diff_range(dataset, sma_type)[1] * 0.001))
	sell_thresh = float(get_sma_diff_range(dataset, sma_type)[1] + (get_sma_diff_range(dataset, sma_type)[1] * 0.01))

	######################################################################################################################################################################################

	# test_fract 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])/float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	test_diff 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])-float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	one_up 		= float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	one_down 	= -float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	iter_rsi 	= float(dataset[len(dataset)-1][rsi_var])
	iter_mfi 	= dataset[len(dataset)-1][mfi_var]
	order_date 	= dataset[len(dataset)-1]["date"]
	
	######################################################################################################################################################################################
		
	# feedback(order_date, signal, dataset[len(dataset)-1][close_var], balance, valuation, quantity, iter_rsi, dataset[len(dataset)-1]["money_flow_index"])
	# place_sell(float(current_price), product_sym, float(quantity))
	# place_buy(float(current_price), product_sym, balance, buy)

	if init_sell == True or init_buy == True:
		print("PASSED CONDITION #1")
		
		if (float(quantity) > 0.0 and buy == True and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price)) and ((float(test_diff) > float(sell_thresh) and float(one_up) < float(test_diff)) or (float(iter_rsi) > 0.90)) or (buy == True and float(current_price)) > float(last_price)*1.02:
			signal 		= "SOLD"
			last_val 	= float(current_price)*float(quantity)
			last_price  = current_price
			buy 		= place_sell(float(current_price), product_sym, float(quantity), buy)
			feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, iter_mfi, current_price)

		######################################################################################################################################################################################

		elif (buy == False and float(balance) >= float(start_balance) and ((float(test_diff) < float(buy_thresh) and float(one_down) < float(test_diff)) or (float(iter_rsi) < 0.12) or (float(current_price) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.2):
			quantity 	= float(balance)/float(current_price)
			last_val 	= float(quantity)*float(current_price)
			signal 		= "BOUGHT"
			
			order_return 	= place_buy(float(current_price), product_sym, balance, buy, last_val, quantity, last_price)
			buy 		= order_return[0]
			last_val 	= order_return[1]
			quantity 	= order_return[2]
			last_price 	= order_return[3]
			
			feedback(order_date, signal, float(current_price), balance, valuation, quantity, iter_rsi, iter_mfi, current_price)

	elif init_buy == False and init_sell == False:
		if float(test_diff) > float(sell_thresh) and buy == True and float(quantity) > 0.0 and float(quantity)*float(current_price) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(current_price) and float(one_up) < float(test_diff):

		######################################################################################################################################################################################
			
			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			signal 		= "SOLD"

			buy = place_sell(float(current_price), product_sym, float(quantity), buy)

			last_val 	= float(current_price)*float(quantity)
			last_price  = float(current_price)
			init_sell = True
			feedback(order_date, signal, float(current_price), balance, valuation, quantity, iter_rsi, iter_mfi, current_price)

		######################################################################################################################################################################################

		elif float(test_diff) < float(buy_thresh) and buy == False and float(balance) >= float(start_balance) and float(one_down) < float(test_diff) and float(iter_rsi) < 0.2:

		######################################################################################################################################################################################

			print(buy_thresh)
			print(sell_thresh)
			print(test_diff)
			print(iter_rsi)
			quantity 	= float(balance)/float(current_price)
			last_val 	= float(quantity)*float(current_price)
			signal 		= "BOUGHT"

			buy = place_buy(current_price, product_sym, balance, buy)

			last_price  = float(current_price)
			feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, iter_mfi, current_price)
			init_buy = True



	print("#"*50)
	print("STATUS: GOOD")
	print(str(round_down((current_price-0.01), 2)))
	print(str(round_down((current_price-0.01), 2)))
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
	print("VAL PRICE:   " + str(float(last_val)*1.002))
	print("-------------------------------")
	print("SIGNAL:      " + str(buy))
	print("START BAL:   " + str(start_balance))
	print("PRICE:       " + str(current_price))
	print("BALANCE:     " + str(balance))
	print("VALUATION:   " + str(current_price*float(quantity)))
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

##################################################################
##################################################################
##################################################################

def feedback(order_date, signal, price_per, balance, valuation, quantity, iter_rsi, mfi, current_price):
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

##################################################################
##################################################################
##################################################################

def trade_file_or_array(file_or_array, datas):
	a = []
	convert_csv(datas)
	datas 		= str(datas) + "_header"
	a 			= pd.read_csv(datas + ".csv", parse_dates=True, infer_datetime_format=True)
	a.columns 	= ['date','open','high','low','close','volume']
	return a

##################################################################
##################################################################
##################################################################

def process_datset():
	a 			= auth().get_historical_klines("ETCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
	convert_json(a, "binance_test")
	b 			= trade_file_or_array("file", "binance_test")
	dataset 	= moving_average_alt(b, 1)
	dataset 	= moving_average_alt(dataset, 6)
	dataset 	= moving_average_alt(dataset, 20)
	dataset 	= relative_strength_index(dataset, 14)
	dataset 	= money_flow_index(dataset, 14)
	dataset 	= macd(dataset, 12, 26)
	dataset 	= standard_deviation(dataset, 21)
	dataset 	= dataset.to_json(orient='records')
	dataset 	= json.loads(dataset)
	return dataset

##################################################################
##################################################################

init_dataset = process_datset()
if sma_appended == False:
		for e in init_dataset[200]:
			if "sma_" in str(e):
				sma_counter+=1
				sma_type.append(int(e.replace("sma_", "")))
		sma_type.sort()
		sma_appended = True

while True:
	try:
		backtest(process_datset())
	except:
		pass

##################################################################
##################################################################
##################################################################
