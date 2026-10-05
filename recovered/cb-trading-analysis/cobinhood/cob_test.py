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
from cobinhood_api import cobinhood
from decimal import Decimal, ROUND_DOWN
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
	a = json.loads(a.content)
	return a
######################################################################################################################################################
######################################################################################################################################################
def auth():
	a = os.getenv("API_TOKEN", "")
	b = cobinhood.Cobinhood_API(a)
	return b
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
def get_product_ticker(product_sym):
	a = auth().get_ticker(product_sym)
	return a["ticker"]
######################################################################################################################################################
######################################################################################################################################################
def get_ticker_price(ticker_array):
	a = ticker_array["last_trade_price"]
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
	ema_slow.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
	macd = pd.Series(ema_fast - ema_slow, name='macd')
	macd_sign = pd.Series(macd.ewm(span=9, min_periods=9).mean(), name='macd_sign_' + str(n_fast) + '_' + str(n_slow))
	macd_diff = pd.Series(macd - macd_sign, name='macd_diff_' + str(n_fast) + '_' + str(n_slow))
	df = df.join(macd)
	df = df.join(macd_sign)
	df = df.join(macd_diff)
	return df
######################################################################################################################################################
######################################################################################################################################################
##########################################################################################
##########################################################################################
def stochastic_oscillator_k(h, l, c, fastk_period, slowk_period, slowd_period, df):
    hh = pd.Series.rolling(h, fastk_period, min_periods=fastk_period).max()
    ll = pd.Series.rolling(l, fastk_period, min_periods=fastk_period).min()
    # fast_k = 100 * (c - ll) / (hh - ll)
    fast_k = (c - ll) / (hh - ll)
    # print(ll)
    so_k = pd.Series(fast_k, name="fast_k")
    df = df.join(so_k)
    
    slow_k = pd.Series.ewm(fast_k, span=slowk_period, min_periods=slowk_period).mean()
    slow_kk = pd.Series(slow_k, name="so_k")
    df = df.join(slow_kk)

    slow_d = pd.Series.ewm(slow_k, span=slowd_period, min_periods=slowd_period).mean()
    slow_dd = pd.Series(slow_d, name="so_d")
    df = df.join(slow_dd)

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
		b.writerow([c["timestamp"], c["open"], c["high"], c["low"], c["close"], c["volume"]])
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
######################################################################################################################################################
######################################################################################################################################################	

def conditional_feedback_emergency_sell(buy, quantity, current_price, balance, low_balance):
	print("-"*50)
	print("CONDITIONS: EMERGENCY SELL")
	print("-"*50)
	print("(quantity*current_price)+balance <= low_balance")
	print((quantity*current_price)+balance <= low_balance)
	print("buy == True")
	print(buy == True)

def conditional_feedback_sell(buy, curr_stoch_k, quantity, current_price, low_balance):
	print("-"*50)
	print("CONDITIONS: SELL")
	print("-"*50)
	print("curr_stoch_k >= 1.0")
	print(curr_stoch_k >= 1.0)
	print("buy == True")
	print(buy == True)
	print("quantity > 0.0")
	print(quantity > 0.0)
	print("(quantity*current_price) >= low_balance")
	print((quantity*current_price) >= low_balance)

def conditional_feedback_buy(buy, balance, current_price, low_quantity, curr_stoch_k,  curr_stoch_d):
	print("-"*50)
	print("CONDITIONS: BUY")
	print("-"*50)
	print("buy == False")
	print(buy == False)
	print("(balance/current_price) >= low_quantity")
	print((balance/current_price) >= low_quantity)
	print("((curr_stoch_k <= 0.0 or curr_stoch_k == None)")
	print(curr_stoch_k <= 0.0 or curr_stoch_k == None)
	print("curr_stoch_d >= curr_stoch_k)")
	print(curr_stoch_d >= curr_stoch_k)
	print("-"*50)
	print("-"*50)

######################################################################################################################################################
######################################################################################################################################################	
def get_queued_orders():
	a = auth().get_all_orders()
	a = a["orders"]
	return a
######################################################################################################################################################
######################################################################################################################################################
def orders_wait_time(sleep_wait_primary, sleep_wait_psecondary):
	a = get_queued_orders()
	b = len_of_orders(a)
	sleep_wait = 0
	if b > 0:
		sleep_wait = sleep_wait_secondary
	elif b <= 0:  
		sleep_wait = sleep_wait_primary
	return sleep_wait
######################################################################################################################################################
######################################################################################################################################################	
def len_of_orders(order_queue):
	a = len(order_queue)
	return a

# def toggle_buy(quantity):
# 	global buy
# 	if quantity > 0.1:
# 		buy = True
# 	else:
# 		buy = False
# 	print(buy)
# 	return buy
################
def toggle_buy(quantity, balance):
	global buy
	if quantity > 0.1:
		buy = True
	elif quantity > 0.1 and balance < 0.2:
		buy = False
	else:
		buy = False
	print(buy)
	return buy
######################################################################################################################################################
######################################################################################################################################################	
def update_orders():
	global buy
	a = get_queued_orders()
	b = len_of_orders(a)
	if b > 0:
		for c in a:
			if c["side"] == "ask":
				buy = True
				d = auth().cancel_order(c["id"])
				print("v"*50)
				print(c)					 
				print(d)
				print(buy)
				print("^"*50)
			elif c["side"] == "bid":
				buy = False
				d = auth().cancel_order(c["id"])
				print("v"*50)
				print(c)					 
				print(d)
				print(buy)
				print("^"*50)
	print(buy)
	return buy
######################################################################################################################################################
######################################################################################################################################################	
def order_state(order_array):
	try:	
		a = auth().get_order(order_array["order"]["id"])
		try:
			if a["order"]["state"] == "rejected":
				return False
			elif a["order"]["state"] == "filled":
				return True
		except:
			pass
	except:
		a = order_array["success"]
		if a == "False":
			return False
		elif a == "True":
			return True

######################################################################################################################################################
######################################################################################################################################################
def place_sell(current_price, product_sym, quantity, buy, last_val):
	# quantity = float(str().split(".")[0])
	quant_array = [".00000001", ".0000001", ".000001", ".00001", ".0001", ".001", ".01", ".1"]
	went_through = False
	buy = buy
	for aa in quant_array:
		sell_quant = quantity
		sell_quant = Decimal(str(sell_quant)).quantize(Decimal(aa), rounding=ROUND_DOWN)
		print("------------------------------------------------------")
		print("SELL")
		print("SYMBOL:   " + str(product_sym))
		print("PRICE: 	 " + str(current_price))
		print("QUANTITY: " + str(sell_quant))
		print("BALANCE:  " + str(balance))
		print("------------------------------------------------------")
		print(sell_quant)
		# p = auth().order_market_sell(symbol=product_sym, quantity=quantity)
		# p = auth().place_order(product_sym, 'ask', 'limit', quantity)
		# order_data = {
		#     "trading_pair_id": "BTC-USDT",
		#     "side": "bid",
		#     "type": "market",
		#     "size": str(quantity)
		# }
		# p = auth().place_order(product_sym, 'ask', 'market', str(sell_quant))
		p = auth().place_order(product_sym, 'ask', 'limit', str(sell_quant), price=float(current_price))
		print(p)
		if order_state(p) == True:
			went_through = True

	if went_through == True:
		buy = False
	else:
		buy = True
	return [buy]
		
######################################################################################################################################################
######################################################################################################################################################
def place_buy(current_price, product_sym, balance, buy, last_val):
	quant_array = [".00000001", ".0000001", ".000001", ".00001", ".0001", ".001", ".01", ".1"]
	went_through = False
	buy = buy
	for aa in quant_array:	
		# buy_quant = float(balance-0.5)/float(current_price)
		buy_quant = Decimal(str(float(balance)/float(current_price))).quantize(Decimal(aa), rounding=ROUND_DOWN)
		# buy_quant = float(balance)/float(current_price)
		if buy_quant < 0:
			buy_quant = -1*buy_quant
			print("---")
			print("INVERTED")
			print("---")
			print(buy_quant)
			print("---")
			print("INVERTED")
			print("---")
		# buy_quant = split_quantity(buy_quant)
		# buy_quant = float(str(buy_quant).split(".")[0])
		print("------------------------------------------------------")
		print("ORDER:    BUY")
		print("SYMBOL:   " + str(product_sym))
		print("PRICE: 	 " + str(current_price))
		print("QUANTITY: " + str(buy_quant))
		print("BALANCE:  " + str(balance))
		print("------------------------------------------------------")
		# p = auth().order_market_buy(symbol=product_sym, quantity=buy_quant)
		# p 	= auth().place_order(product_sym, 'bid', 'limit', buy_quant)
		# p 	= auth().place_order(product_sym, 'bid', 'market', str(buy_quant))
		p 	= auth().place_order(product_sym, 'bid', 'limit', str(buy_quant), price=float(current_price))
		print(p)
		if order_state(p) == True:
			went_through = False

	if went_through == True:
		buy = True
	else:
		buy = False
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
def get_quantity(crypto_currency):
	a = float(auth().get_asset_balance(asset=crypto_currency)["free"])
	return a
#################################################
#################################################
def get_balance():
	# a = float(auth().get_asset_balance(asset=pegged_currency)["free"])
	a = auth().get_wallet_balances()
	return a["balances"]
#################################################
#################################################
def get_currency_balance(all_balances,currency_type):
	a = all_balances
	b = 0.0
	d = 0.0
	for c in a:
		if c["currency"] == currency_type:
			b = float(c["total"])
			d = float(c["usd_value"])
			break
	return [b, d]
#################################################
#################################################

init_balances 	= get_balance()

# crypto_currency = "BTC"
crypto_currency = "ETH"
pegged_currency = "USDT"
product_sym 	= crypto_currency+ "-" + pegged_currency

# start_balance 	= float(auth().get_asset_balance(asset=pegged_currency)["free"])

start_balance 	= float(get_currency_balance(init_balances, pegged_currency)[0])
# start_balance 	= 50.0
balance 		= start_balance
quantity 		= float(get_currency_balance(init_balances, crypto_currency)[0])
# quantity 		= float(auth().get_asset_balance(asset=crypto_currency)["free"])
# quantity 		= 0.0
# current_price 	= get_ticker_price(product_sym)
# current_price 	= float(current_price["lastPrice"])


# quantity 		= float(auth().get_asset_balance(asset="ETC")["free"])

# if product_sym == "LTC":
# 	quantity 		= auth().get_accoun)["available"]
# 	

# elif product_sym == "ETH":
# 	quantity 		= auth().get_accoun)["	

config_override = open_config()
######################################################################################################################################################################################
trigger_threshold_buy_var = config_override[0]["trigger_threshold_buy_var"]

started 		= False
last_val 		= 0.0
prev_val 		= 0.0
buy 			= True
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
rsi_period 				= 7
# sleep_wait 			= 5
sleep_wait 				= 3
sleep_wait_primary		= 3
sleep_wait_secondary	= 15
############################################
last_stoch_k 		= 0.0
last_stoch_d 		= 0.0
############################################
low_balance 		= start_balance
reset_low_balance 	= False
low_quantity 		= quantity
last_quantity 		= quantity
############################################
fuck_you 			= False
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
	global trigger_threshold_buy_var
	
	global last_stoch_k
	global last_stoch_d

	global low_balance
	global reset_low_balance
	global low_quantity
	global last_quantity
	global fuck_you
	
	global sleep_wait
	global sleep_wait_primary
	global sleep_wait_secondary

	ticker_array 	= get_product_ticker(product_sym)
	print("*"*20)
	print("*"*20)
	print(ticker_array)

	curr_stoch_k 	= dataset[len(dataset)-1]["fast_k"]
	curr_stoch_d 	= dataset[len(dataset)-1]["so_d"]

	print("K " + str(curr_stoch_k))
	print("D " + str(curr_stoch_d))
	# if curr_stoch_k != None:
	balance  		= balance
	low_balance 	= low_balance
	init_balances   = get_balance()
	quantity 		= get_currency_balance(init_balances, crypto_currency)[0]
	low_quantity 	= low_quantity
	# quantity 		= split_quantity(quantity)
	valuation		= float(quantity*current_price)
	current_price 	= float(get_ticker_price(ticker_array))
	order_date 		= datetime.fromtimestamp(float(dataset[len(dataset)-1]["date"])/1000)
	print(buy)
	buy 			= toggle_buy(quantity, balance)
	print(buy)

	print(buy)
######################################################################################################################################################
######################################################################################################################################################
	print(current_price)

	# print(Decimal(str(current_price)).quantize(Decimal('.0000001'), rounding=ROUND_DOWN))
	# print(reset_low_balance, (valuation), start_balance)

	if reset_low_balance == False and valuation >= start_balance:
		low_balance 	  = start_balance
		reset_low_balance = True

	######################################################################################################################################################################################
	if started == False:
		buy 	= check_balance(balance, trigger_threshold_buy_var, quantity, current_price)
		# if balance > 4.0:
		# 	low_quantity 	= balance/current_price 
		# 	last_quantity 	= low_quantity 
		# else:
		# 	low_quantity = quantity 
		# 	last_quantity 	= low_quantity
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
	#####################################################################################################################################################################################
	trigger_threshold_buy_var 	= config_override[0]["trigger_threshold_buy_var"]
	sleep_wait 					= config_override[0]["sleep_wait"]
	#####################################################################################################################################################################################
	#####################################################################################################################################################################################
	if config_override[0]["start_balance_override"] == True:
		start_balance 	= config_override[0]["start_balance"]
	#####################################################################################################################################################################################
	#####################################################################################################################################################################################
	# if config_override[0]["sleep_override"] == True:
	# 	sleep_wait_primary 		= config_override[0]["sleep_wait_primary"]
	# 	sleep_wait_secondary	= config_override[0]["sleep_wait_secondary"]
	# 	sleep_wait				= config_override[0]["sleep_wait"]
	######################################################################################################################################################################################
	######################################################################################################################################################################################
	if config_override[0]["last_val_override"] == True:
		last_val 		= config_override[0]["last_val"]
	#####################################################################################################################################################################################
	#####################################################################################################################################################################################
	if config_override[0]["buy_override"] == True:
		buy 			= config_override[0]["buy"]
	####################################################################################################################################################################################
	####################################################################################################################################################################################
	if config_override[0]["conditional_override"] == True:
		buy_rsi 			= config_override[0]["buy_rsi"]
		sell_rsi 			= config_override[0]["sell_rsi"]
		last_val_increase 	= config_override[0]["last_val_increase"]
		mod_buy_last_price 	= config_override[0]["mod_buy_last_price"]
		mod_sell_last_price = config_override[0]["mod_sell_last_price"]
		mod_buy_thresh 		= config_override[0]["mod_buy_thresh"]
		mod_sell_thresh 	= config_override[0]["mod_sell_thresh"]
	#####################################################################################################################################################################################
	#####################################################################################################################################################################################
	if config_override[0]["emergency_override"] == True:
		emergency_cutoff 	= config_override[0]["emergency_cutoff"]
		emergency_period 	= config_override[0]["emergency_period"]
	
	if config_override[0]["force_emergency_stop"] == True:
		emergency_stop 	= config_override[0]["emergency_stop"]
	######################################################################################################################################################################################
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
	# print(auth().get_order('d1a4cb51-6891-4be7-8250-6c20fec1db2e'))
	toggle_buy(quantity, balance)
	buy = update_orders()
	# toggle_buy(quantity, balance)
	# place_buy(current_price, product_sym, balance, buy, last_val)
	# init_balances 	= get_balance()
	# quantity 		= get_currency_balance(init_balances, crypto_currency)[0]
	# place_sell(current_price, product_sym, quantity, buy, last_val)
	# print(auth().get_all_orders())

######################################################################################################################################################################################
######################################################################################################################################################################################
######################################################################################################################################################################################
	# if curr_stoch_k != None:
	# if (quantity*current_price)+balance <= low_balance and buy == True:
	# 	signal 		= "BELOW START BALANCE"
	# 	signal 		= "SOLD"
	# 	# quantity 			= get_quantity(crypto_currency)
	# 	init_balances 	= get_balance()
	# 	quantity 		= get_currency_balance(init_balances, crypto_currency)[0]
	# 	low_quantity 		= quantity
	# 	ticker_array 	= get_product_ticker(product_sym)
	# 	order_return 	= place_sell(ticker_array["last_trade_price"], product_sym, quantity, buy, last_val)
	# 	# order_return 	= place_sell(ticker_array["lowest_ask"], product_sym, quantity, buy, last_val)
	# 	# order_return 	= place_sell(current_price, product_sym, quantity, buy, last_val)
		
	# 	buy 				= order_return[0]

	# 	init_balances 		= get_balance()
	# 	balance 			= get_currency_balance(init_balances, pegged_currency)[0]
	# 	quantity 			= get_currency_balance(init_balances, crypto_currency)[0]

	# 	last_price  		= current_price
	# 	low_balance 		= balance
	# 	reset_low_balance 	= False

	# 	feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)

######################################################################################################################################################################################
	# elif curr_stoch_k != None and curr_stoch_k >= 1.0 and buy == True and quantity > 0.0 and (quantity*current_price) >= low_balance:
	# if (float(quantity) > 0.0 and buy == True and float(quantity)*float(dataset[len(dataset)-1]["close"]) > float(start_balance) and float(last_val)*1.002 < float(quantity)*float(dataset[len(dataset)-1][close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) > 0.90))) or (buy == True and float(dataset[len(dataset)-1][close_var]) > float(last_price)*1.02):
	# elif curr_stoch_k != None and curr_stoch_k >= 1.0 and buy == True and quantity > 0.0 and ((quantity + (balance/current_price))*current_price) >= low_balance:
	if (float(quantity) > 0.0 and buy == True and float(quantity)*float(dataset[len(dataset)-1][close_var]) > float(start_balance) and float(last_val) < float(quantity)*float(dataset[len(dataset)-1][close_var]) and ((test_diff > sell_thresh and one_up < test_diff) or (float(iter_rsi) >= 0.85))) or (buy == True and float(dataset[len(dataset)-1][close_var]) > float(last_price)*1.02):
######################################################################################################################################################################################
		signal 				= "SOLD"
		init_balances 		= get_balance()
		ticker_array 		= get_product_ticker(product_sym)
		quantity 			= get_currency_balance(init_balances, crypto_currency)[0]
		# order_return 		= place_sell(current_price, product_sym, quantity, buy, last_val)
		# order_return 		= place_sell(ticker_array["last_trade_price"], product_sym, quantity, buy, last_val)
		# order_return 		= place_sell(ticker_array["lowest_ask"], product_sym, quantity, buy, last_val)
		# buy 				= order_return[0]
		last_price  		= current_price

		init_balances 		= get_balance()
		balance 			= get_currency_balance(init_balances, pegged_currency)[0]
		quantity 			= get_currency_balance(init_balances, crypto_currency)[0]

		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)

######################################################################################################################################################################################
	# elif buy == False and balance >= start_balance and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	# elif buy == False and balance/current_price >= low_quantity and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	# elif buy == False and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	# elif (buy == False and float(balance) >= float(start_balance) and ((test_diff < buy_thresh and (one_down > test_diff or one_down < test_diff)) or (float(iter_rsi) < 0.12) or (float(dataset[len(dataset)-1][close_var]) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.2):
	# elif buy == False and ((curr_stoch_k <= 0.0 or curr_stoch_k == None) and curr_stoch_d >= curr_stoch_k):
	elif (buy == False and float(balance) >= float(start_balance) and ((test_diff < buy_thresh and one_down > test_diff) or (float(iter_rsi) < 0.2) or (float(dataset[len(dataset)-1][close_var]) < float(last_price)-(float(last_price)*0.1)))) or (buy == False and float(iter_rsi) < 0.4):
######################################################################################################################################################################################
		signal 			= "BOUGHT"
		ticker_array 	= get_product_ticker(product_sym)
		order_return 	= place_buy(ticker_array["highest_bid"], product_sym, balance, buy, last_val)
		init_balances  	= get_balance()

		buy 			= order_return[0]
		valuation 		= get_currency_balance(init_balances, crypto_currency)[1]
		
		last_price  	= current_price
		balance 		= get_currency_balance(init_balances, pegged_currency)[0]
		quantity 		= get_currency_balance(init_balances, crypto_currency)[0]
		last_val 		= valuation
		
		feedback(order_date, signal, current_price, balance, valuation, quantity, iter_rsi, current_price)
######################################################################################################################################################################################
######################################################################################################################################################################################
	print("----------------------------------------------")
	print("----------------------------------------------")
	conditional_feedback_emergency_sell(buy, quantity, current_price, balance, low_balance)
	conditional_feedback_sell(buy, curr_stoch_k, quantity, current_price, low_balance)
	conditional_feedback_buy(buy, balance, current_price, low_quantity, curr_stoch_k,  curr_stoch_d)
	print("----------------------------------------------")
	print("DATE:        	" + str(dataset[len(dataset)-1]["date"]))
	print("OPEN:        	" + str(dataset[len(dataset)-1]["open"]))
	print("HIGH:        	" + str(dataset[len(dataset)-1]["high"]))
	print("LOW:         	" + str(dataset[len(dataset)-1]["low"]))
	print("CLOSE:       	" + str(dataset[len(dataset)-1]["close"]))
	print("VOLUME:      	" + str(dataset[len(dataset)-1]["volume"]))
	print("-------------------------------")
	print("SMA TYPE:    	" + str(sma_type))
	print("RESET BALANCE:   " + str(reset_low_balance))
	print("-------------------------------")
	print("TEST DIFF:   	" + str(test_diff))
	print("ONE UP:   		" + str(one_up))
	print("ONE DOWN:    	" + str(one_down))
	print("BUY THRESH:  	" + str(buy_thresh))
	print("SELL THRESH: 	" + str(sell_thresh))
	print("-------------------------------")
	print("LAST VAL:    	" + str(last_val))
	print("LAST PRICE:  	" + str(last_price))
	print("LAST VAL THRESH: " + str(last_val))
	print("LOW QUANT THRESH:" + str(low_quantity+500.0))
	print("-------------------------------")
	print("SIGNAL:      	" + str(buy))
	print("START BAL:   	" + str(start_balance))
	print("PRICE:       	" + str(current_price))
	print("QUANTITY:    	" + str(quantity))
	print("BALANCE:     	" + str(balance))
	print("VALUATION:   	" + str(current_price*quantity))
	print("PROJECTED QUANTITY: " + str(balance/current_price))
	print("-------------------------------")
	print("VAL BAL COMBINE: " + str(valuation+balance))
	print("EST. QTY+PRC+BAL:" + str((quantity*current_price)+balance))
	print("BAL/PRICE:    	" + str(balance/current_price))
	print("-------------------------------")
	print("LOWEST BALANCE:     " + str(low_balance))
	print("LOWEST QUANTITY:    " + str(low_quantity))
	print("-------------------------------")
	print("SMA 1:       	" + str(dataset[len(dataset)-1]["sma_1"]))
	print("SMA 6:       	" + str(dataset[len(dataset)-1]["sma_6"]))
	print("SMA 20:      	" + str(dataset[len(dataset)-1]["sma_20"]))
	print("-------------------------------")
	print("RSI:         	" + str(iter_rsi))
	print("STOCH FAST 0:    " + str(dataset[0]["fast_k"]))
	print("STOCH FAST K:    " + str(dataset[len(dataset)-1]["fast_k"]))
	print("STOCH SLOW K:    " + str(dataset[len(dataset)-1]["so_k"]))
	print("STOCH SLOW D:    " + str(dataset[len(dataset)-1]["so_d"]))
	print("-------------------------------")
	print("SLEEP WAIT:      " + str(sleep_wait))
	print("-------------------------------")
	print("#"*50)
	print("#"*50)
	print()
	print("#"*50)
	# last_stoch_k 	=  dataset[len(dataset)-1]["so_k"]
	# last_stoch_d 	=  dataset[len(dataset)-1]["so_d"]
	# time.sleep(sleep_wait)
	sleep_wait = orders_wait_time(sleep_wait_primary, sleep_wait_secondary)
	print(sleep_wait)
	time.sleep(sleep_wait)
	# else:
	# 	print(curr_stoch_k)
		

##################################################################
##################################################################
##################################################################

def feedback(order_date, signal, price_per, balance, valuation, quantity, iter_rsi, current_price):
	# send_test("order_date: "+ str(order_date) + " | signal: "+ str(signal) + " | price_per: "+ str(price_per) + " | balance: "+ str(balance) + " | valuation: "+ str(valuation) + " | quantity: "+ str(quantity) + " | iter_rsi: "+ str(iter_rsi) + " | current_price: " + str(current_price))