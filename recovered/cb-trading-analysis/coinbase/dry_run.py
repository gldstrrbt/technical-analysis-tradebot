import os, csv, ast, json, time, datetime
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import cbpro
import pytz
from datetime import datetime, timedelta

public_client = cbpro.PublicClient()
# import get_history
# import __orig_get_history
# get_history.history_data.get_history_data()

# import technical_indicators

##########################################################################################
##########################################################################################

# def rewrite_csv():
# 	# get_history.history_data.get_history_data()
# 	__orig_get_history.history_data.get_history_data()

# def correct_header():
# 	__orig_get_history.history_data.csv_header()
	# get_history.history_data.csv_header()

##########################################################################################
##########################################################################################

# def auth():
# 	key 		= os.getenv("COINBASE_API_KEY", "")
# 	b64secret 	= os.getenv("COINBASE_API_SECRET", "")
# 	passphrase 	= os.getenv("COINBASE_API_PASSPHRASE", "")
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

# import get_history
# import __orig_get_history
# get_history.history_data.get_history_data()

# import technical_indicators

##########################################################################################
##########################################################################################

# def rewrite_csv():
# 	# get_history.history_data.get_history_data()
# 	__orig_get_history.history_data.get_history_data()

# def correct_header():
# 	__orig_get_history.history_data.csv_header()
	# get_history.history_data.csv_header()

##########################################################################################
##########################################################################################

def check_ticker():
	a = auth().get_product_ticker(product_id='ETH-USD')
	return a

##########################################################################################
##########################################################################################

def moving_average(df, n):
	"""Calculate the moving average for the given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	MA = pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df = df.join(MA)
	return df

##########################################################################################
##########################################################################################

def macd(df, n_fast, n_slow):
	"""Calculate MACD, MACD Signal and MACD difference
	
	:param df: pandas.DataFrame
	:param n_fast: 
	:param n_slow: 
	:return: pandas.DataFrame
	"""
	EMAfast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
	EMAslow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
	MACD = pd.Series(EMAfast - EMAslow, name='macd')
	MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='macd_sign_' + str(n_fast) + '_' + str(n_slow))
	MACDdiff = pd.Series(MACD - MACDsign, name='macd_diff_' + str(n_fast) + '_' + str(n_slow))
	df = df.join(MACD)
	df = df.join(MACDsign)
	df = df.join(MACDdiff)
	return df

##########################################################################################
##########################################################################################

def rate_of_change(df, n):
	"""
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	M = df['close'].diff(n - 1)
	N = df['close'].shift(n - 1)
	ROC = pd.Series(M / N, name='roc')
	df = df.join(ROC)
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

##########################################################################################
##########################################################################################

def check_rsi(rsi):
	for a in rsi:
		print(a)


##########################################################################################
##########################################################################################

def stochastic_oscillator_k(df):
	"""Calculate stochastic oscillator %K for given data.
	
	:param df: pandas.DataFrame
	:return: pandas.DataFrame
	"""
	SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='sto_k')
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
	SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='sto_k')
	SOd = pd.Series(SOk.ewm(span=n, min_periods=n).mean(), name='sto_d')
	df = df.join(SOd)
	return df

##########################################################################################
##########################################################################################

def relative_strength_index(df, n):
	"""Calculate Relative Strength Index(RSI) for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	i = 0
	UpI = [0]
	DoI = [0]
	while i + 1 <= df.index[-1]:
		try:
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
		except:
			i = i + 1
			pass
	UpI = pd.Series(UpI)
	DoI = pd.Series(DoI)
	PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
	NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
	RSI = pd.Series(PosDI / (PosDI + NegDI), name='rsi')
	df = df.join(RSI)
	return df

##########################################################################################
##########################################################################################

def money_flow_index(df, n):
	"""Calculate Money Flow Index and Ratio for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	# PP = (df['high'].atype(float) + df['low'].atype(float) + df['close'].atype(float)) / 3
	PP = (df['high'] + df['low'] + df['close']) / 3
	print()
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
	MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name='mfi')
	df = df.join(MFI)
	return df

##########################################################################################
##########################################################################################

def standard_deviation(df, n):
	"""Calculate Standard Deviation for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	df = df.join(pd.Series(df['close'].rolling(n, min_periods=n).std(), name='std'))
	return df


##########################################################################################
##########################################################################################

# convert_csv("20190123_203432___data")

def testing():
	# a 		= "20190122_145449___data"
	# a 		= "20190122_142459___data"
	# a 		= "20190122_194125___data"
	# a 		= "20190122_185923___data"
	a 		= "buffer_data"
	# a 		= "sec_wtf"
	# a 		= open("buffer___data.csv", "r+")
	# d 		= csv.reader(a)
	# e 		= [f for f in d]
	# b 		= pd.DataFrame(e, columns=['date','low', 'high', 'open', 'close', 'volume'])
	# b 		= pd.read_csv(a + ".csv", index_col=0, parse_dates=True, infer_datetime_format=True, columns=['low', 'high', 'open', 'close', 'volume'])
	b 		= pd.read_csv(a + ".csv", parse_dates=True, infer_datetime_format=True)
	b.columns = ['date','low','high','open','close','volume']
	# b 		= pd.read_csv(a + ".csv", parse_dates=True, infer_datetime_format=True)
	# print(b)

	dataset = moving_average(b, 1)
	dataset = moving_average(dataset, 6)
	dataset = moving_average(dataset, 20)
	# print(dataset["date"])
	# print(dataset["high"])
	# print(dataset["close"])
	# print(dataset["open"])
	# print(dataset["low"])
	dataset = relative_strength_index(dataset, 14)
	dataset = money_flow_index(dataset, 14)
	dataset = macd(dataset, 12, 26)
	dataset = standard_deviation(dataset, 21)
	dataset = stochastic_oscillator_k(dataset)
	dataset = stochastic_oscillator_d(dataset, 3)

	# print(dataset)

	# for y, z in enumerate(dataset):
		# print(dataset[])
		# print("CLOSE PRICE : " + str(dataset[y]))
		# print("-"*5)
		# print("SMA 20      : " + str(dataset[y]))
	c = 0
	start_balance = 1000
	balance = start_balance
	quantity = 0
	valuation = 0
	last_val = 0
	buy = False
	cut_off = False

	while c < len(dataset):
		# current_price = check_ticker()
		# current_price = current_price["price"]
		# print(current_price)
		# print((balance/dataset["close"][c])*dataset["close"][c])
		# print(dataset["close"][c])
		# print(len(dataset))
		if dataset["rsi"][c] != None:
			# print(dataset["close"][c] - dataset["open"][c])
			# if dataset["rsi"][c] < dataset["mfi"][c] and buy == True and last_val*.5 < valuation:
			# if buy == True and (dataset["rsi"][c] < dataset["mfi"][c] or dataset["rsi"][c] > 0.9):
			# print(last_val)
			# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6):
			# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["close"][c] - dataset["open"][c] > 0.4):
			# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["close"][c] - dataset["open"][c] > 0.4 and dataset["macd"][c] > 0.4):
			if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["macd"][c] > 0.005 and dataset["sma_1"][c] > dataset["sma_6"][c] or dataset["std"][c] > 0.75):
			# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["sma_1"][c] > dataset["sma_6"][c] or dataset["std"][c] > 0.75):
			# if buy == True:
				last_val = valuation
				balance   = quantity*dataset["close"][c] 
				quantity  = 0
				valuation = 0
				print("-"*50)
				print("SOLD")
				print("PRICE:       " + str(dataset["close"][c]))
				print("QUANTITY:    " + str(quantity))
				print("VALUATION:   " + str(valuation))
				print("BALANCE:     " + str(balance))
				print("DATE:        " + str(dataset["date"][c]))
				print("OPEN:        " + str(dataset["open"][c]))
				print("HIGH:        " + str(dataset["high"][c]))
				print("LOW:         " + str(dataset["low"][c]))
				print("CLOSE:       " + str(dataset["close"][c]))
				print("VOLUME:      " + str(dataset["volume"][c]))
				print("SMA 1:       " + str(dataset["sma_1"][c]))
				print("SMA 6:       " + str(dataset["sma_6"][c]))
				print("SMA 20:      " + str(dataset["sma_20"][c]))
				print("RSI:         " + str(dataset["rsi"][c]))
				print("STOCH K:    	" + str(dataset["sto_k"][c]))
				print("STOCH D:     " + str(dataset["sto_d"][c]))
				print("MFI:         " + str(dataset["mfi"][c]))
				print("STD:         " + str(dataset["std"][c]))
				print("MACD:        " + str(dataset["macd"][c]))
				print("-"*50)
				buy = False
			# elif buy == False and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] < 0.5):
			# elif buy == False and quantity*dataset["close"][c] > start_balance:
			elif buy == False and ((balance/dataset["close"][c])*dataset["close"][c]) >= start_balance and (dataset["rsi"][c] < 0.08 and dataset["mfi"][c] < 0.3 and dataset["macd"][c] < -0.005 and dataset["sma_1"][c] < dataset["sma_6"][c] or dataset["std"][c] > 0.95):
			# elif buy == False and ((balance/dataset["close"][c])*dataset["close"][c]) > start_balance and (dataset["rsi"][c] < 0.08 and dataset["mfi"][c] < 0.3 and dataset["sma_1"][c] < dataset["sma_6"][c]):
			# elif buy == False:
			# elif buy == False and ((balance/dataset["close"][c])*dataset["close"][c]) > start_balance and (dataset["rsi"][c] < 0.08 and dataset["mfi"][c] < 0.3 and dataset["close"][c] - dataset["open"][c] > 0.0 and dataset["macd"][c] < -0.3):
			# elif buy == False and ((balance/dataset["close"][c])*dataset["close"][c]) > start_balance and (dataset["rsi"][c] < 0.08 and dataset["mfi"][c] < 0.3 and dataset["close"][c] - dataset["open"][c] > 0.0):
				quantity  = balance/dataset["close"][c] 
				valuation = quantity*dataset["close"][c] 
				# last_val = valuation
				balance   = 0
				print("-"*50)
				print("BOUGHT")
				print("PRICE:       " + str(dataset["close"][c]))
				print("BALANCE:     " + str(balance))
				print("VALUATION:   " + str(valuation))
				print("QUANTITY:    " + str(quantity))
				print("DATE:        " + str(dataset["date"][c]))
				print("OPEN:        " + str(dataset["open"][c]))
				print("HIGH:        " + str(dataset["high"][c]))
				print("LOW:         " + str(dataset["low"][c]))
				print("CLOSE:       " + str(dataset["close"][c]))
				print("VOLUME:      " + str(dataset["volume"][c]))
				print("SMA 1:       " + str(dataset["sma_1"][c]))
				print("SMA 6:       " + str(dataset["sma_6"][c]))
				print("SMA 20:      " + str(dataset["sma_20"][c]))
				print("RSI:         " + str(dataset["rsi"][c]))
				print("STOCH K:    	" + str(dataset["sto_k"][c]))
				print("STOCH D:     " + str(dataset["sto_d"][c]))
				print("MFI:         " + str(dataset["mfi"][c]))
				print("STD:         " + str(dataset["std"][c]))
				print("MACD:        " + str(dataset["macd"][c]))
				print("-"*50)
				buy = True
		c+=1



# def compare_time(date_a, date_b):
# 	for date_a in my_orders():
# 		if "ltc" in str(date_a).lower():
# 			print(date_a["created_at"])
# 			print(date_a["created_at"])
# 			print(date_a["created_at"])
# 			# date_b = str(date_a["created_at"]).replace("T", " ")
# 			# date_b = str(date_a["created_at"]).split("T")
# 			date_b = str(date_a["created_at"]).split(".")
# 			date_b = date_b[0]
# 			print(date_b)
# 			print(date_b)
# 			print(date_b)
# 			print(date_b)
# 			print(date_b)
# 			print(datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S"))
# 			print(datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S"))
# 			print(datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S"))
# 			print(datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S"))
# 			z = datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S")
# 			if z < datetime.now():
# 				print()
# 				print(z)
# 				print(datetime.now())
# 				print(datetime.now()-z)



























































	# if z < datetime.now():
	# 	print()
	# 	print(z)
	# 	print(datetime.now())
	# 	print(datetime.now()-z)







iter_count 		= 0
start_balance 	= 100
balance 		= start_balance
quantity 		= 0
valuation 		= 0
last_val 		= 0
buy 			= False
current_price   = 0

set_trade_date 	= False
last_trade_date = 0
dataset_date 	= 0

def compare_time(date_a, date_b):
	global last_trade_date 
	print(date_a)
	print(date_a)
	print(date_a)
	# date_b = str(date_a["created_at"]).replace("T", " ")
	# date_b = str(date_a["created_at"]).split("T")
	print()
	print(date_b)
	print(date_b)
	print(date_b)
	date_a = str(date_a).split("+")[0]
	date_b = str(date_b).split("+")[0]
	print()
	print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	print(datetime.strptime(date_a, "%Y-%m-%d %H:%M:%S"))
	print()
	print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	print(datetime.strptime(date_b, "%Y-%m-%d %H:%M:%S"))
	print("#"*50)
	# z = datetime.strptime(date_b, "%Y-%m-%dT%H:%M:%S")
	if date_b < date_a:
		time.sleep(3)
		return True
	elif date_b >= date_a:
		last_trade_date = date_b
		return False




def dry_run():
	global balance
	global valuation
	global quantity
	global last_val
	global buy
	global iter_count
	global set_trade_date
	global last_trade_date
	global dataset_date

	a 				= "buffer_data"
	b 				= pd.read_csv(a + ".csv", parse_dates=True, infer_datetime_format=True)
	b.columns 		= ['date','low','high','open','close','volume']
	# a 		= open("buffer___data.csv", "r+")
	# d 		= csv.reader(a)
	# e 		= [f for f in d]
	# b 		= pd.DataFrame(e, columns=['date','low', 'high', 'open', 'close', 'volume'])
	# b 		= pd.read_csv(a + ".csv", index_col=0, parse_dates=True, infer_datetime_format=True, columns=['low', 'high', 'open', 'close', 'volume'])
	# b 		= pd.read_csv(a + ".csv", parse_dates=True, infer_datetime_format=True)
	# print(b)

	current_price = check_ticker()
	current_price = current_price["price"]
	print(current_price)

	dataset = moving_average(b, 1)
	dataset = moving_average(dataset, 6)
	dataset = moving_average(dataset, 20)
	# print(dataset["date"])
	# print(dataset["high"])
	# print(dataset["close"])
	# print(dataset["open"])
	# print(dataset["low"])
	dataset = relative_strength_index(dataset, 14)
	dataset = money_flow_index(dataset, 14)
	dataset = macd(dataset, 12, 26)
	dataset = standard_deviation(dataset, 21)
	# print(dataset)




	lagged_update 	= False

	if set_trade_date == False:
		last_trade_date = dataset["date"][len(dataset)-1]
		set_trade_date 	= True
		print(last_trade_date)
		print(dataset_date)
	else:
		dataset_date 	= dataset["date"][len(dataset)-1]
		lagged_update  	= compare_time(last_trade_date, dataset_date)






	# for y, z in enumerate(dataset):
		# print(dataset[])
		# print("CLOSE PRICE : " + str(dataset[y]))
		# print("-"*5)
		# print("SMA 20      : " + str(dataset[y]))
	
	# while c < len(dataset):
		# print((balance/dataset["close"][c])*dataset["close"][c])
		# print(dataset["close"][c])
		# print(len(dataset))
	if dataset["rsi"][len(dataset)-1] != None and lagged_update == False:
		print()
		print("#"*50)
		print("#"*50)
		print("STATUS")
		print("PRICE:       " + str(dataset["close"][len(dataset)-1]))
		print("BALANCE:     " + str(balance))
		print("VALUATION:   " + str(dataset["close"][len(dataset)-1]*quantity))
		print("QUANTITY:    " + str(quantity))
		print("DATE:        " + str(dataset["date"][len(dataset)-1]))
		print("OPEN:        " + str(dataset["open"][len(dataset)-1]))
		print("HIGH:        " + str(dataset["high"][len(dataset)-1]))
		print("LOW:         " + str(dataset["low"][len(dataset)-1]))
		print("CLOSE:       " + str(dataset["close"][len(dataset)-1]))
		print("VOLUME:      " + str(dataset["volume"][len(dataset)-1]))
		print("SMA 1:       " + str(dataset["sma_1"][len(dataset)-1]))
		print("SMA 6:       " + str(dataset["sma_6"][len(dataset)-1]))
		print("SMA 20:      " + str(dataset["sma_20"][len(dataset)-1]))
		print("RSI:         " + str(dataset["rsi"][len(dataset)-1]))
		print("MFI:         " + str(dataset["mfi"][len(dataset)-1]))
		print("STD:         " + str(dataset["std"][len(dataset)-1]))
		print("MACD:        " + str(dataset["macd"][len(dataset)-1]))
		print("#"*50)
		print("#"*50)
		print()

		
		# print(dataset["close"][c] - dataset["open"][c])
		# if dataset["rsi"][c] < dataset["mfi"][c] and buy == True and last_val*.5 < valuation:
		# if buy == True and (dataset["rsi"][c] < dataset["mfi"][c] or dataset["rsi"][c] > 0.9):
		# print(last_val)
		# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6):
		# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["close"][c] - dataset["open"][c] > 0.4):
		# if buy == True and last_val < quantity*dataset["close"][c] and quantity*dataset["close"][c] > start_balance and (dataset["rsi"][c] > 0.85 and dataset["mfi"][c] > 0.6 and dataset["close"][c] - dataset["open"][c] > 0.4 and dataset["macd"][c] > 0.4):
		if buy == True and last_val < quantity*dataset["close"][len(dataset)-1] and quantity*dataset["close"][len(dataset)-1] > start_balance and (dataset["rsi"][len(dataset)-1] > 0.85 and dataset["mfi"][len(dataset)-1] > 0.6 and dataset["macd"][len(dataset)-1] > 0.005 and dataset["sma_1"][len(dataset)-1] > dataset["sma_6"][len(dataset)-1] or dataset["std"][len(dataset)-1] > 0.75):
		# if buy == True and last_val < quantity*dataset["close"][len(dataset)-1] and quantity*dataset["close"][len(dataset)-1] > start_balance and (dataset["rsi"][len(dataset)-1] > 0.85 and dataset["mfi"][len(dataset)-1] > 0.6 and dataset["sma_1"][len(dataset)-1] > dataset["sma_6"][len(dataset)-1] or dataset["std"][len(dataset)-1] > 0.75):
		# if buy == True:
			last_val = valuation
			balance   = quantity*dataset["close"][len(dataset)-1] 
			quantity  = 0
			valuation = 0
			print("-"*50)
			print("SOLD")
			print("PRICE:       " + str(dataset["close"][len(dataset)-1]))
			print("QUANTITY:    " + str(quantity))
			print("VALUATION:   " + str(valuation))
			print("BALANCE:     " + str(balance))
			print("DATE:        " + str(dataset["date"][len(dataset)-1]))
			print("OPEN:        " + str(dataset["open"][len(dataset)-1]))
			print("HIGH:        " + str(dataset["high"][len(dataset)-1]))
			print("LOW:         " + str(dataset["low"][len(dataset)-1]))
			print("CLOSE:       " + str(dataset["close"][len(dataset)-1]))
			print("VOLUME:      " + str(dataset["volume"][len(dataset)-1]))
			print("SMA 1:       " + str(dataset["sma_1"][len(dataset)-1]))
			print("SMA 6:       " + str(dataset["sma_6"][len(dataset)-1]))
			print("SMA 20:      " + str(dataset["sma_20"][len(dataset)-1]))
			print("RSI:         " + str(dataset["rsi"][len(dataset)-1]))
			print("MFI:         " + str(dataset["mfi"][len(dataset)-1]))
			print("STD:         " + str(dataset["std"][len(dataset)-1]))
			print("MACD:        " + str(dataset["macd"][len(dataset)-1]))
			print("-"*50)
			buy = False
		# elif buy == False and quantity*dataset["close"][len(dataset)-1] > start_balance and (dataset["rsi"][len(dataset)-1] < 0.5):
		# elif buy == False and quantity*dataset["close"][len(dataset)-1] > start_balance:
		elif buy == False and ((balance/dataset["close"][len(dataset)-1])*dataset["close"][len(dataset)-1]) >= start_balance and (dataset["rsi"][len(dataset)-1] < 0.08 and dataset["mfi"][len(dataset)-1] < 0.3 and dataset["macd"][len(dataset)-1] < -0.005 and dataset["sma_1"][len(dataset)-1] < dataset["sma_6"][len(dataset)-1] or dataset["std"][len(dataset)-1] > 0.95):
		# elif buy == False and ((balance/dataset["close"][len(dataset)-1])*dataset["close"][len(dataset)-1]) > start_balance and (dataset["rsi"][len(dataset)-1] < 0.08 and dataset["mfi"][len(dataset)-1] < 0.3 and dataset["sma_1"][len(dataset)-1] < dataset["sma_6"][len(dataset)-1]):
		# elif buy == False:
		# elif buy == False and ((balance/dataset["close"][len(dataset)-1])*dataset["close"][len(dataset)-1]) > start_balance and (dataset["rsi"][len(dataset)-1] < 0.08 and dataset["mfi"][len(dataset)-1] < 0.3 and dataset["close"][len(dataset)-1] - dataset["open"][len(dataset)-1] > 0.0 and dataset["macd"][len(dataset)-1] < -0.3):
		# elif buy == False and ((balance/dataset["close"][len(dataset)-1])*dataset["close"][len(dataset)-1]) > start_balance and (dataset["rsi"][len(dataset)-1] < 0.08 and dataset["mfi"][len(dataset)-1] < 0.3 and dataset["close"][len(dataset)-1] - dataset["open"][len(dataset)-1] > 0.0):
			quantity  = balance/dataset["close"][len(dataset)-1] 
			valuation = quantity*dataset["close"][len(dataset)-1] 
			# last_val = valuation
			balance   = 0
			print("-"*50)
			print("BOUGHT")
			print("PRICE:       " + str(dataset["close"][len(dataset)-1]))
			print("BALANCE:     " + str(balance))
			print("VALUATION:   " + str(valuation))
			print("QUANTITY:    " + str(quantity))
			print("DATE:        " + str(dataset["date"][len(dataset)-1]))
			print("OPEN:        " + str(dataset["open"][len(dataset)-1]))
			print("HIGH:        " + str(dataset["high"][len(dataset)-1]))
			print("LOW:         " + str(dataset["low"][len(dataset)-1]))
			print("CLOSE:       " + str(dataset["close"][len(dataset)-1]))
			print("VOLUME:      " + str(dataset["volume"][len(dataset)-1]))
			print("SMA 1:       " + str(dataset["sma_1"][len(dataset)-1]))
			print("SMA 6:       " + str(dataset["sma_6"][len(dataset)-1]))
			print("SMA 20:      " + str(dataset["sma_20"][len(dataset)-1]))
			print("RSI:         " + str(dataset["rsi"][len(dataset)-1]))
			print("MFI:         " + str(dataset["mfi"][len(dataset)-1]))
			print("STD:         " + str(dataset["std"][len(dataset)-1]))
			print("MACD:        " + str(dataset["macd"][len(dataset)-1]))
			print("-"*50)
			buy = True
		time.sleep(60)
		iter_count+=1
		print(current_price)
	elif lagged_update == True:
		time.sleep(1)
		iter_count+=1
		print(current_price)

##########################################################################################
##########################################################################################

# def init():
	# convert_csv("data/20190128_185225___data")
	# rewrite_csv()
	# correct_header()
	# testing()

######################################################################################
##########################################################################################

# while True:
# 	try:
# 		dry_run()
# 	except:
# 		pass


testing()
# z = open("20190120_192023___data.json", "r+")
# x = json.load(z)
# rings = ast.literal_eval(x)
# numpy_2d_arrays = [np.array(ring) for ring in rings]
# print(numpy_2d_arrays)

##########################################################################################
##########################################################################################










