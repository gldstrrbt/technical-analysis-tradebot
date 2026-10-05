import os, json, requests, time, csv, matplotlib, mpl_finance, random, math, new_history, pytz, requests, email, smtplib, imaplib
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
from email.mime.text import MIMEText
from itertools import chain
# from threading import Thread


######################################################################################################################################################
######################################################################################################################################################
this_is 	= True
hard_stop   = False
hard_reset  = False
######################################################################################################################################################
def send_test(some_data):
	some_data = str(some_data)
	a 		= open("ep.txt", "r+")
	b 		= [c for c in a]
	f 	= b[0]
	g 	= b[1]
	d 	= "smtp.gmail.com"
	e 	= "465"
	h 	= f
	i 	= [f]
	j = MIMEText(some_data)
	j["Subject"] = some_data
	j["From"] = f
	j["To"] = f
	j.set_charset("utf-8")
	k = smtplib.SMTP_SSL(d, e)
	k.login(f, g)
	k.sendmail(h, i, j.as_string())
	k.quit()
######################################################################################################################################################
######################################################################################################################################################
def open_config_req():
	a = requests.get("http://shanelessa.com/config_test.json")
	a = a.content
	a = json.loads(a)
	return a
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
def stochastic_oscillator_k(df):
	"""Calculate stochastic oscillator %K for given data.
	
	:param df: pandas.DataFrame
	:return: pandas.DataFrame
	"""
	SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='so_k')
	df = df.join(SOk)
	return df
##########################################################################################
##########################################################################################
def stochastic_oscillator_d(df, n):
	"""Calculate stochastic oscillator %D for given data.
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='so_k')
	SOd = pd.Series(SOk.ewm(span=n, min_periods=n).mean(), name='so_d')
	df = df.join(SOd)
	return df
##########################################################################################
##########################################################################################
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
def place_buy(current_price, product_sym, balance, buy, last_val):
	print(current_price, product_sym, balance)
	buy_price = float(current_price)
	buy_quant = float(balance-1)/float(buy_price)
	if buy_quant < 0:
		buy_quant = -1*buy_quant
		print("---")
		print(buy_quant)
		print("---")
	buy_quant = split_quantity(buy_quant)
	print(buy_quant)
	print(buy_quant)
	print(buy_quant)
	print(buy_quant)
	print(buy_quant)
	print(buy_quant)

	print("------------------------------------------------------")
	print("ORDER:    BUY")
	print("SYMBOL:   " + str(product_sym))
	print("PRICE: 	 " + str(buy_price))
	print("QUANTITY: " + str(buy_quant))
	print("BALANCE:  " + str(balance))
	print("------------------------------------------------------")
	p = auth().order_market_buy(symbol=product_sym, quantity=buy_quant)
	print(p)
	last_val 	= float(p["cummulativeQuoteQty"])
	# last_val 	= (balance/current_price)*current_price
	buy 		= True
	return [buy, last_val]
	
######################################################################################################################################################
######################################################################################################################################################
def place_sell(current_price, product_sym, quantity, buy, last_val):
	quantity = float(str(quantity).split(".")[0])
	print("------------------------------------------------------")
	print("SELL")
	print("------------------------------------------------------")
	print(quantity)
	p = auth().order_market_sell(symbol=product_sym, quantity=quantity)
	print(p)
	# last_val 	= float(p["cummulativeQuoteQty"])
	# last_val 	= current_price*quantity
	buy 		= False
	print("BUY == " + str(buy))
	# return [buy, last_val]
	return [buy]

######################################################################################################################################################
######################################################################################################################################################
def check_balance(balance, trigger_threshold_buy_var, quantity, current_price):
	a = ""
	if quantity != 0.0 and balance != 0.0:
		if quantity*current_price > balance:
			a = True
		elif quantity*current_price < balance:
			a = False
	elif quantity == 0.0 and balance > 0.0:
		a = False
	elif balance == 0.0 and quantity > 0.0:
		a = True

	# if balance < 0.99:
	# 	a = True
	# elif balance > 5.00:
	# 	a = False
	return a
######################################################################################################################################################
######################################################################################################################################################
def open_config():
	a = open("config_test.json", "r+")
	b = json.load(a)
	a.close()
	return b
#################################################
#################################################
def split_quantity(quantity_var):
	quantity_var = str(quantity_var).split(".")
	quantity_var = float(quantity_var[0])
	# if len(quantity_var[1]) > 1:
	# 	quantity_var = float(quantity_var[0]+"."+quantity_var[1][0]+quantity_var[1][1])
	# else:
	# 	quantity_var = float(quantity_var[0]+".0")
	return quantity_var
#################################################
#################################################

crypto_currency = "BTT"
pegged_currency = "USDT"
product_sym 	= crypto_currency+pegged_currency

# start_balance 	= float(auth().get_asset_balance(asset=pegged_currency)["free"])
start_balance 	= 50.0
balance 		= start_balance
# quantity 		= float(auth().get_asset_balance(asset=crypto_currency)["free"])
quantity 		= 0.0
current_price 	= product_ticker(product_sym)
current_price 	= float(current_price["lastPrice"])


# quantity 		= float(auth().get_asset_balance(asset="ETC")["free"])

# if product_sym == "LTC":
# 	quantity 		= auth().get_accoun)["available"]
# 	

# elif product_sym == "ETH":
# 	quantity 		= auth().get_accoun)["available"]
# 	

config_override = open_config()
######################################################################################################################################################################################
trigger_threshold_buy_var = config_override[0]["trigger_threshold_buy_var"]

started 		= False
last_val 		= 0.0
prev_val 		= 0.0
buy 			= False
valuation 		= 0.0
signal 			= "BOUGHT"

sma_counter 	= 0
sma_type 		= []
sma_appended 	= False

last_price  	= 0.0
init_buy 		= False
init_sell 		= False
rsi_var 		= "rsi"
close_var 		= "close"
std_var 		= "std"

sell_thresh  	= 0.02
buy_thresh  	= 0.03


############################################
############### CONFIG VARS ################
############################################
current_price 	= 0
set_trade_date 	= False
last_trade_date = 0
dataset_date 	= 0
############################################
buy_rsi 			= 0.25
sell_rsi 			= 0.8
last_val_increase 	= 1.006
mod_buy_last_price 	= 0.9
mod_sell_last_price = 1.006
mod_buy_thresh		= 0.001
mod_sell_thresh		= 0.01
############################################
emergency_stop 		= False
emergency_cutoff 	= 0.95
emergency_period 	= 400
emergency_counter 	= 0
############################################
############################################
rsi_period 			= 7
sleep_wait 			= 5
############################################
last_stoch_k 		= 0.0
last_stoch_d 		= 0.0
############################################
low_balance 		= start_balance
reset_low_balance 	= False
low_quantity 		= 0.0
last_quantity 		= 0.0
############################################
# current_price 	= 0
# set_trade_date 	= False
# last_trade_date = 0
# dataset_date 	= 0

# buy_rsi 			= 0.45
# sell_rsi 			= 0.98
# last_val_increase 	= 1.006
# mod_buy_last_price 	= 0.9
# mod_sell_last_price = 1.006
# mod_buy_thresh		= 0.001
# mod_sell_thresh		= 0.01
# emergency_stop 		= False

############################################
############################################
def print_the_fucker (start_balance, balance, quantity, last_val, buy, valuation, signal, sma_counter, sma_type, sell_thresh, buy_thresh, last_price, init_buy, init_sell, rsi_var, close_var, std_var, current_price, set_trade_date, last_trade_date, dataset_date, prev_val, product_sym, started, buy_rsi, sell_rsi, last_val_increase, mod_buy_last_price, mod_sell_last_price, mod_buy_thresh, mod_sell_thresh, emergency_stop, emergency_cutoff, emergency_period, emergency_counter, rsi_period, sleep_wait, trigger_threshold_buy_var):
	print("------------------------------------")
	print(start_balance)
	print(balance)
	print(quantity)
	print(last_val)
	print(buy)
	print(valuation)
	print(signal)
	print(sma_counter)
	print(sma_type)
	print(sell_thresh)
	print(buy_thresh)
	print(last_price)
	print(init_buy)
	print(init_sell)
	print(rsi_var)
	print(close_var)
	print(std_var)
	print(current_price)
	print(set_trade_date)
	print(last_trade_date)
	print(dataset_date)
	print(prev_val)
	print(product_sym)
	print(started)
	print(buy_rsi)
	print(sell_rsi)
	print(last_val_increase)
	print(mod_buy_last_price)
	print(mod_sell_last_price)
	print(mod_buy_thresh)
	print(mod_sell_thresh)
	print(emergency_stop)
	print(emergency_cutoff)
	print(emergency_period)
	print(emergency_counter)
	print(rsi_period)
	print(sleep_wait)
	print(trigger_threshold_buy_var)
	print("------------------------------------")

def backtest(dataset):
	global start_balance 	
	global balance 		
	global quantity 		
	global last_val 		
	global buy 			
	global valuation 		
	global signal 			
	global sma_counter 	
	global sma_type 		
	global sell_thresh  	
	global buy_thresh  	
	global last_price  	
	global init_buy 		
	global init_sell 		
	global rsi_var 		
	global close_var 		
	global std_var 	
	global current_price 	
	global set_trade_date 	
	global last_trade_date 
	global dataset_date 	
	global order_queued 	
	global lagged_update
	global prev_val

	global product_sym 	
	global started

	global buy_rsi
	global sell_rsi
	global last_val_increase
	global mod_buy_last_price
	global mod_sell_last_price
	global mod_buy_thresh
	global mod_sell_thresh
	global emergency_stop
	global emergency_cutoff
	global emergency_period
	global emergency_counter
	global rsi_period
	global sleep_wait
	global trigger_threshold_buy_var
	
	global last_stoch_k
	global last_stoch_d

	global low_balance
	global reset_low_balance
	global low_quantity
	global last_quantity
	# buy = buy
	curr_stoch_k 	=  dataset[len(dataset)-1]["so_k"]
	curr_stoch_d 	=  dataset[len(dataset)-1]["so_d"]
	# balance 		= float(auth().get_asset_balance(asset="USDT")["free"])
	# quantity 		= float(auth().get_asset_balance(asset="ETC")["free"])
	last_quantity 	= last_quantity
	balance 		= balance
	low_balance 	= low_balance
	quantity 		= quantity
	low_quantity 	= low_quantity
	# quantity 		= split_quantity(quantity)
	valuation		= float(quantity*current_price)
	current_price 	= float(product_ticker(product_sym)["lastPrice"])
	order_date 		= datetime.fromtimestamp(float(dataset[len(dataset)-1]["date"])/1000)
	# current_price 	= float(current_price)

	# if start_balance < 4.00 and started == False:
	# 	start_balance = valuation
	# 	print("START BALANCE: " + str(start_balance))
	if reset_low_balance == False and valuation >= start_balance:
		low_balance 	  = start_balance
		reset_low_balance = True

	print("BALANCE:            " + str(balance))
	print("QUANTITY:           " + str(quantity))
	print("BUY:                " + str(buy))
	print("CURRENT PRICE:      " + str(current_price))
	print("LOWEST BALANCE:     " + str(low_balance))
	print("LOWEST QUANTITY:    " + str(low_quantity))
	print("PROJECTED QUANTITY: " + str(balance/current_price))

	# if start_balance < 4.00:
	# 	start_balance = valuation

	# else:
		# emergency_stop = False

	# if valuation < start_balance*0.9:

	# print("BALANCE:       " + str(balance))
	# print("QUANTITY:      " + str(quantity))
	# print("BUY:           " + str(buy))
	# print("CURRENT PRICE: " + str(current_price))

	######################################################################################################################################################################################
	if started == False:
		# buy 	= check_balance(balance, trigger_threshold_buy_var, quantity, current_price)
		started = True
	######################################################################################################################################################################################

	buy_thresh 	= float(get_sma_diff_range(dataset, sma_type)[0] + (get_sma_diff_range(dataset, sma_type)[1] * 0.001))
	sell_thresh = float(get_sma_diff_range(dataset, sma_type)[1] + (get_sma_diff_range(dataset, sma_type)[1] * 0.01))

	######################################################################################################################################################################################

	test_diff 	= float(dataset[len(dataset)-1]["sma_" + str(sma_type[0])])-float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])
	one_up 		= float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	one_down 	= -float(dataset[len(dataset)-1]["sma_" + str(sma_type[1])])*0.002
	iter_rsi 	= float(dataset[len(dataset)-1][rsi_var])
	
	######################################################################################################################################################################################

	# if valuation > 100 and valuation < start_balance*emergency_cutoff and emergency_stop == False and buy == True:	
	# 	print("EMERGENCY STOP")
	# 	print("EMERGENCY STOP")
	# 	print("EMERGENCY STOP")
	# 	print("EMERGENCY STOP")
	# 	print("EMERGENCY STOP")
	# 	print("EMERGENCY STOP")
	# 	send_test("EMERGENCY STOP")
	# 	signal 		= "SOLD"
	# 	# order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
	# 	buy 			= False
	# 	last_price  	= current_price
	# 	balance 		= current_price*quantity 
	# 	quantity 		- 0
		
	# 	feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
	# 	emergency_stop = True


	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	config_override 			= open_config()
	######################################################################################################################################################################################
	trigger_threshold_buy_var 	= config_override[0]["trigger_threshold_buy_var"]
	sleep_wait 					= config_override[0]["sleep_wait"]
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	if config_override[0]["start_balance_override"] == True:
		start_balance 	= config_override[0]["start_balance"]
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	if config_override[0]["last_val_override"] == True:
		last_val 		= config_override[0]["last_val"]
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	if config_override[0]["buy_override"] == True:
		buy 			= config_override[0]["buy"]
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	# if config_override[0]["force_sell"] == True:
	# 	signal 		= "SOLD"
	# 	order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
	# 	buy 			= order_return[0]
	# 	last_price  	= current_price
		
	# 	feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	# if config_override[0]["force_buy"] == True:
	# 	signal 			= "BOUGHT"
	# 	order_return 	= place_buy(current_price, product_sym, balance, buy, last_val)
		
	# 	buy 			= order_return[0]
	# 	last_val 		= order_return[1]
	# 	valuation 		= last_val
	# 	last_price  	= current_price
		
	# 	feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
	#####################################################################################################################################################################################
	if config_override[0]["conditional_override"] == True:
		buy_rsi 			= config_override[0]["buy_rsi"]
		sell_rsi 			= config_override[0]["sell_rsi"]
		last_val_increase 	= config_override[0]["last_val_increase"]
		mod_buy_last_price 	= config_override[0]["mod_buy_last_price"]
		mod_sell_last_price = config_override[0]["mod_sell_last_price"]
		mod_buy_thresh 		= config_override[0]["mod_buy_thresh"]
		mod_sell_thresh 	= config_override[0]["mod_sell_thresh"]
	#####################################################################################################################################################################################
	if config_override[0]["emergency_override"] == True:
		emergency_cutoff 	= config_override[0]["emergency_cutoff"]
		emergency_period 	= config_override[0]["emergency_period"]
	
	if config_override[0]["force_emergency_stop"] == True:
		emergency_stop 	= config_override[0]["emergency_stop"]
	######################################################################################################################################################################################
	if emergency_stop == True and emergency_counter <= emergency_period:
		emergency_counter+=1
		print(emergency_counter)
	elif emergency_counter > emergency_period: 
		print(emergency_counter)
		print(emergency_cutoff)
		emergency_stop 		= False
		emergency_counter 	= 0
		start_balance 		= balance
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	# place_sell(current_price, product_sym, quantity, buy, last_val)
	# place_buy(current_price, product_sym, balance, buy, last_val)
	# print_the_fucker (start_balance, balance, quantity, last_val, buy, valuation, signal, sma_counter, sma_type, sell_thresh, buy_thresh, last_price, init_buy, init_sell, rsi_var, close_var, std_var, current_price, set_trade_date, last_trade_date, dataset_date, prev_val, product_sym, started, buy_rsi, sell_rsi, last_val_increase, mod_buy_last_price, mod_sell_last_price, mod_buy_thresh, mod_sell_thresh, emergency_stop, emergency_cutoff, emergency_period, emergency_counter, rsi_period, sleep_wait, trigger_threshold_buy_var)
	# if emergency_stop == False and (init_buy == True or init_sell == True):	
	######################################################################################################################################################################################
		# if ((quantity > 0.01 and buy == True and quantity*current_price > start_balance and last_val*last_val_increase < quantity*current_price) and ((test_diff >= sell_thresh and one_up < test_diff) or (iter_rsi >= sell_rsi)) or (buy == True and current_price > last_price*mod_sell_last_price and quantity*current_price > start_balance)):
		# if buy == True and quantity*float(current_price) > start_balance and last_val*1.002 < quantity*float(current_price) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > sell_rsi)):
		# if buy == True and quantity*float(current_price) > start_balance and last_val*1.002 < quantity*float(current_price) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 90.0) or (float(d["mfi"]) > float(d["rsi"]) and float(d["rsi"]) > 70 and d["neg_flow"] != 0)):
	######################################################################################################################################################################################
	if quantity*current_price <= low_balance and buy == True:
		signal 		= "BELOW START BALANCE"
		signal 		= "SOLD"
		# order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
		buy 				= False
		last_price  		= current_price
		balance  			= quantity*current_price
		low_quantity 		= quantity
		quantity 			= 0.0
		valuation 			= 0.0
		low_balance 		= balance
		reset_low_balance 	= False

		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)

######################################################################################################################################################################################
	if curr_stoch_k >= 1.0 and buy == True and quantity > 0.0 and quantity*current_price >= low_balance:
######################################################################################################################################################################################
		signal 		= "SOLD"
		# order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
		buy 			= False
		last_price  	= current_price
		balance  		= quantity*current_price
		quantity 		= 0.0
		valuation 		= 0.0

		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)

######################################################################################################################################################################################
	# elif buy == False and float(balance) >= start_balance and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(current_price) < last_price-(last_price*buy_rsi))):
	# elif buy == False and float(balance) >= start_balance and ((test_diff < buy_thresh and one_down < test_diff) or (float(iter_rsi) < 0.12) or (float(current_price) < last_price*mod_buy_last_price)):
######################################################################################################################################################################################
	# elif buy == False and balance >= start_balance and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	elif buy == False and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k) and balance/current_price >= low_quantity and balance/current_price >= last_quantity*1.01:
######################################################################################################################################################################################
		signal 			= "BOUGHT"
		# order_return 	= place_buy(current_price, product_sym, balance, buy, last_val)
		
		buy 			= True
		quantity 		= balance/current_price
		last_quantity 	= quantity
		valuation 		= current_price*quantity
		balance 		= 0.0
		last_val 		= valuation
		last_price  	= current_price

		
		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
		######################################################################################################################################################################################

		# elif buy == False and balance >= start_balance and ((test_diff < buy_thresh and one_down < test_diff) or (iter_rsi <= buy_rsi) or (current_price < last_price*mod_buy_last_price)):

	######################################################################################################################################################################################

	# elif emergency_stop == False and init_buy == False and init_sell == False:
	# 	# print_the_fucker (start_balance, balance, quantity, last_val, buy, valuation, signal, sma_counter, sma_type, sell_thresh, buy_thresh, last_price, init_buy, init_sell, rsi_var, close_var, std_var, current_price, set_trade_date, last_trade_date, dataset_date, prev_val, product_sym, started, buy_rsi, sell_rsi, last_val_increase, mod_buy_last_price, mod_sell_last_price, mod_buy_thresh, mod_sell_thresh, emergency_stop, emergency_cutoff, emergency_period, emergency_counter, rsi_period, sleep_wait, trigger_threshold_buy_var)
	# ######################################################################################################################################################################################
	# 	# if (test_diff >= sell_thresh and buy == True and quantity > 0.0 and quantity*current_price > start_balance and last_val*last_val_increase < quantity*current_price and one_up < test_diff) or (buy == True and iter_rsi >= sell_rsi):
	# ######################################################################################################################################################################################
	# 	# if (test_diff >= sell_thresh and buy == True and quantity > 0.0 and quantity*current_price > start_balance and last_val*last_val_increase < quantity*current_price and one_up < test_diff) or (buy == True and iter_rsi >= sell_rsi):
	# 	if curr_stoch_k >= 1.0 and buy == True and quantity > 0.0 and quantity*current_price > start_balance:
	# ######################################################################################################################################################################################
	# 		signal 			= "SOLD"
	# 		# order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
	# 		buy 			= False
	# 		last_price  	= current_price
	# 		balance  		= quantity*current_price
	# 		quantity 		= 0.0
	# 		valuation 		= 0.0
			
	# 		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
	# 		init_sell 		= True

	# 	######################################################################################################################################################################################

	# ######################################################################################################################################################################################
	# 	# elif (test_diff < buy_thresh and buy == False and balance >= start_balance and one_down > test_diff and iter_rsi <= 0.12) or (iter_rsi <= buy_rsi and buy == False and balance >= start_balance):
	# ######################################################################################################################################################################################
	# 	elif buy == False and balance >= start_balance and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	# ######################################################################################################################################################################################
	# 		signal 			= "BOUGHT"
	# 		# order_return 	= place_buy(current_price, product_sym, balance, buy, last_val)
			
	# 		buy 			= True
	# 		quantity 		= balance/current_price
	# 		valuation 		= current_price*quantity
	# 		balance 		= 0.0
	# 		last_val 		= valuation
	# 		last_price  	= current_price
			
	# 		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
	# 		init_buy = True


	print("#"*50)
	print("STATUS: GOOD")
	print("#"*50)
	print(current_price)
	print(last_trade_date)
	print(dataset_date)
	print("#"*50)
	print()
	print("#"*50)
	print("#"*50)
	print("STATS")
	print("----------------------------------------------")
	print("INIT BUY:    	" + str(init_buy))
	print("INIT SELL:   	" + str(init_sell))
	print("SMA APPEND:  	" + str(sma_appended))
	print("SMA TYPE:    	" + str(sma_type))
	print("VAL PRICE:   	" + str(last_val*1.002))
	print("TEST DIFF:   	" + str(test_diff))
	print("ONE UP:   		" + str(one_up))
	print("ONE DOWN:    	" + str(one_down))
	print("BUY THRESH:  	" + str(buy_thresh))
	print("SELL THRESH: 	" + str(sell_thresh))
	print("-------------------------------")
	print("SIGNAL:      	" + str(buy))
	print("START BAL:   	" + str(start_balance))
	print("PRICE:       	" + str(current_price))
	print("BALANCE:     	" + str(balance))
	print("VALUATION:   	" + str(current_price*quantity))
	print("LAST VAL:    	" + str(last_val))
	print("LAST PRICE:  	" + str(last_price))
	print("QUANTITY:    	" + str(quantity))
	print("DATE:        	" + str(dataset[len(dataset)-1]["date"]))
	print("OPEN:        	" + str(dataset[len(dataset)-1]["open"]))
	print("HIGH:        	" + str(dataset[len(dataset)-1]["high"]))
	print("LOW:         	" + str(dataset[len(dataset)-1]["low"]))
	print("CLOSE:       	" + str(dataset[len(dataset)-1]["close"]))
	print("VOLUME:      	" + str(dataset[len(dataset)-1]["volume"]))
	print("SMA 1:       	" + str(dataset[len(dataset)-1]["sma_1"]))
	print("SMA 6:       	" + str(dataset[len(dataset)-1]["sma_6"]))
	print("SMA 20:      	" + str(dataset[len(dataset)-1]["sma_20"]))
	print("RSI:         	" + str(iter_rsi))
	print("CURRENT STOCH K: " + str(dataset[len(dataset)-1]["so_k"]))
	print("CURRENT STOCH D: " + str(dataset[len(dataset)-1]["so_d"]))
	print("LAST QUANTITY:   " + str(last_quantity))
	print("LAST QUANTITY+1%:" + str(last_quantity*1.01))
	print("EMERGENCY:   	" + str(emergency_stop))
	print("#"*50)
	print("#"*50)
	print()
	print("#"*50)
	last_stoch_k 	=  dataset[len(dataset)-1]["so_k"]
	last_stoch_d 	=  dataset[len(dataset)-1]["so_d"]
	# time.sleep(1)
	time.sleep(sleep_wait)

##################################################################
##################################################################
##################################################################

def feedback(order_date, signal, price_per, balance, valuation, quantity, iter_rsi, current_price):
	send_test("order_date: "+ str(order_date) + " | signal: "+ str(signal) + " | price_per: "+ str(price_per) + " | balance: "+ str(balance) + " | valuation: "+ str(valuation) + " | quantity: "+ str(quantity) + " | iter_rsi: "+ str(iter_rsi) + " | current_price: " + str(current_price))
	print("-----------------")
	print("SIGNAL:    " + str(signal))
	print("DATE:      " + str(order_date))
	print("CURR PRICE:" + str(current_price))
	print("RSI:       " + str(iter_rsi))
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

def process_datset(product_sym, rsi_period):
	# a 			= auth().get_historical_klines("ETCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
	a 			= auth().get_historical_klines(product_sym, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
	convert_json(a, "binance_test")
	b 			= trade_file_or_array("file", "binance_test")
	dataset 	= moving_average_alt(b, 1)
	dataset 	= moving_average_alt(dataset, 6)
	dataset 	= moving_average_alt(dataset, 20)
	dataset 	= relative_strength_index(dataset, rsi_period)
	dataset 	= money_flow_index(dataset, 14)
	dataset 	= stochastic_oscillator_k(dataset)
	dataset 	= stochastic_oscillator_d(dataset, 14)
	# dataset 	= money_flow_index(dataset, 14)
	# dataset 	= macd(dataset, 12, 26)
	# dataset 	= standard_deviation(dataset, 21)
	dataset 	= dataset.to_json(orient='records')
	dataset 	= json.loads(dataset)
	return dataset

##################################################################
##################################################################

init_dataset 	= process_datset(product_sym, 7)
# # balance 		= float(auth().get_asset_balance(asset="USDT")["free"])
# # quantity 		= float(auth().get_asset_balance(asset="ETC")["free"])
# balance 		= float(auth().get_asset_balance(asset=pegged_currency)["free"])
# quantity 		= float(auth().get_asset_balance(asset=crypto_currency)["free"])
# current_price 	= product_ticker(product_sym)
# current_price 	= float(current_price["lastPrice"])
# valuation		= float(quantity)*current_price

if started == False:
	last_val = valuation

if sma_appended == False:
		for e in init_dataset[200]:
			if "sma_" in str(e):
				sma_counter+=1
				sma_type.append(int(e.replace("sma_", "")))
		sma_type.sort()
		sma_appended = True

quantity = split_quantity(quantity)

while True:
	try:
		backtest(process_datset(product_sym, 7))
	except:
		pass

##################################################################
##################################################################
##################################################################

# ORDER RESPONSES

# {'symbol': 'BTTUSDT', 'orderId': 3246745, 'clientOrderId': 'eYMPQsbfqnmLZnHdukLkE4', 'transactTime': 1549474385021, 

# 'price': '0.00000000', 'origQty': '202740.00000000', 'executedQty': '202740.00000000', 'cummulativeQuoteQty': '191.79520660', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'SELL', 'fills': [{

# 'price': '0.00094640', 'qty': '23248.00000000'


# 'price': '0.00094630', 'qty': '10674.00000000'


# 'price': '0.00094630', 'qty': '21347.00000000'


# 'price': '0.00094630', 'qty': '10674.00000000'


# 'price': '0.00094610', 'qty': '82429.00000000'


# 'price': '0.00094550', 'qty': '46731.00000000'


# 'price': '0.00094550', 'qty': '7637.00000000'






# {'symbol': 'BTTUSDT', 'orderId': 3247078, 'clientOrderId': 'jDHyRH3EkLqkARbi09LX49', 'transactTime': 1549474411714, 

# 'price': '0.00000000', 'origQty': '203571.00000000', 'executedQty': '203571.00000000', 'cummulativeQuoteQty': '191.18809190', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{

# 'price': '0.00093910', 'qty': '130742.00000000'

