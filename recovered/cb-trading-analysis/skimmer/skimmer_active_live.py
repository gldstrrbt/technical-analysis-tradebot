import os, csv, time, requests

import numpy as np
import pandas as pd
# import matplotlib.mlab as mlab
# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker
# import matplotlib.colors as colors
# import matplotlib.font_manager as font_manager
# from mpl_finance import candlestick2_ohlc
# from mpl_finance import index_bar
# from mpl_finance import plot_day_summary_oclh

import robin_stocks as r
import robin_stocks.helper as helper
import robin_stocks.crypto as crypto

login = r.login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))

# print(crypto.get_crypto_currency_pairs())
# print(crypto.get_crypto_info("BTC"))
print(crypto.get_crypto_quote("BTC"))


# balance 		= 500.0
# signal 			= False
# amount 			= 0
data_collect 	= []


def moving_average_alt(df, n):
	# compiled_sma 	= pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	compiled_sma 	= pd.Series(df["mark_price"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df


def trade_file_or_array(file_or_array, datas):
	a = []
	convert_csv(datas)
	datas 		= str(datas) + "_header"
	a 			= pd.read_csv(datas + ".csv", parse_dates=True, infer_datetime_format=True)
	# a.columns 	= ['date','open','high','low','close','volume']
	a.columns 	= ['mark_price','high','low']
	return a


def convert_csv(filename):
	a = open(str(filename)+".csv", "r+")
	b = csv.reader(a)
	c = open(str(filename)+"_header.csv", "w+")
	d = csv.writer(c)
	d.writerow(["mark_price", "high", "low"])
	for e in b:
		d.writerow(e)


def open_csv(filename):
	a = open(filename, "r+")
	b = csv.reader(a)
	c = [d for d in b]
	a.close()
	return c 


def write_csv(filename, dataset):
	a = open(filename, "a+")
	b = csv.writer(a)
	# print([dataset["mark_price"],dataset["high_price"],dataset["low_price"]])
	b.writerow([dataset["mark_price"],dataset["high_price"],dataset["low_price"]])
	return a 


def start_var():
	a = 200
	b = False
	return [a,b]


def place_buy(balance, val):
	a = balance/val
	return a


def place_sell(amount, val):
	a = amount*val
	return a


def append_data(dataset):
	global data_collect
	b = []
	# a = [a for a in dataset]
	for c in dataset:
		b.append(c)
	return b


def init():
	amount 	= 0
	start_balance = 500
	balance = start_balance
	signal 	= False
	purchase_price = 0
	purchase_value = 0
	skim = 0
	csv_filename = "test"
	y = 0

	while True:
		try:	
			k = write_csv(csv_filename+".csv", crypto.get_crypto_quote("BTC"))
			a = open_csv(csv_filename+".csv") 
			b = trade_file_or_array("file", csv_filename)
			b = moving_average_alt(b, 3)
			b = moving_average_alt(b, 5)
			z = b.iterrows()
			v = []
			for d, c in z:
				t = []
				for s, r in enumerate(c):
					if s == 0 or s == 3 or s == 4:
						t.append(float(r))
				v.append(t)
			bb = balance

			if signal == True:
				y+=1

			if signal == False and y == 0 and (v[len(v)-1][1] > v[len(v)-1][2] and v[len(v)-2][1] >= v[len(v)-2][2] and v[len(v)-3][1] < v[len(v)-3][2]):
				amount 	= place_buy(bb, float(v[len(v)-1][0]))
				purchase_value = float(balance)
				balance = 0 
				signal 	= True 
				purchase_price = float(v[len(v)-1][0])

			elif signal == True and (y >= 9 or v[len(v)-1][0] > purchase_price*1.01):
				if v[len(v)-1][0]*amount > start_balance:
					balance = start_balance
					skim += (v[len(v)-1][0]*amount)-start_balance 
					print(v[len(v)-1][0]*amount)
				else:
					balance = place_sell(amount, float(v[len(v)-1][0]))
				amount 	= 0
				signal 	= False
				y=0

			# if :
			print("*"*100)
			print("*"*100)
			print(v[len(v)-1])
			print(v[len(v)-1])
			print(v[len(v)-1])
			print(v[len(v)-1])
			print("*"*50)
			print("Y:   	"+str(y))
			print("curr:   	"+str(v[len(v)-1][0]))
			print("balance: "+str(balance))
			print("amount:  "+str(amount))
			print("signal:  "+str(signal))
			print("value:   "+str(amount*v[len(v)-1][0]))
			print("skim:  	"+str(skim))
			print("*"*50)
			# time.sleep(60)
			# time.sleep(60)
			# time.sleep(10)
			time.sleep(5)
			# time.sleep(1)
			# time.sleep(3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725)
			# except:
			# 	pass
		except:
			pass

init()

# for hh in crypto.get_crypto_quote("BTC"):
# 	print(hh)