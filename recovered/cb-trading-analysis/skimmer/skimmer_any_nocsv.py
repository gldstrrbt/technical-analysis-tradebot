import os
import time
import numpy as np
import pandas as pd
import robin_stocks as r
import robin_stocks.crypto as crypto
import robin_stocks.helper as helper


# window.oauthClientId = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS";

# clientId: "910fb9f4-f10a-4247-bbb7-e119669b049d"


login = r.login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))

def moving_average_alt(df, n):
	# compiled_sma 	= pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	compiled_sma 	= pd.Series(df["mark_price"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df

def data_to_df(datas):
	a = pd.DataFrame(datas, columns={"mark_price"})
	return a

def start_var():
	a = 200
	b = False
	return [a,b]

def place_buy(balance, val):
	a = ((balance*.999)/val)
	# r.order_buy_crypto_by_price("BTC",balance)
	return a

def place_sell(amount, val):
	a = amount*val
	return a

def append_data(dataset):
	b = []
	for c in dataset:
		b.append(c)
	return b

def init():
	amount 			= 0
	start_balance 	= 100
	balance 		= start_balance
	signal 			= False
	purchase_price 	= 0
	purchase_value 	= 0
	skim 			= 0
	y 				= 0
	data_array 		= [5,3,4,5,12]
	time_int 		= 0.5
	crypto_name 	= "BTC"

	sma_a = 20
	sma_b = 50
	arr_len = sma_b*3

	while True:
		try:	
			data_array.append(float(crypto.get_crypto_quote(crypto_name)["mark_price"]))
			if len(data_array) > arr_len:
				data_array.pop(0)
			print("*"*50)
			a = data_to_df(data_array)
			# a = moving_average_alt(a, 3)
			# a = moving_average_alt(a, 5)
			a = moving_average_alt(a, sma_a)
			a = moving_average_alt(a, sma_b)
			b = a.iterrows()
			c = []
			for d, e in b:
				t = []
				for s, r in enumerate(e):
					t.append(float(r))
				c.append(t)
			bb = balance
			print(c)
			if signal == True:
				y+=1

			# if signal == False and y == 0 and (c[len(c)-1][0] > c[len(c)-1][1] and c[len(c)-1][1] > c[len(c)-1][2] and c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
			if signal == False and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
				amount 			= place_buy(bb, float(c[len(c)-1][0]))
				purchase_value 	= float(balance)
				balance 		= 0 
				signal 			= True 
				purchase_price 	= float(c[len(c)-1][0])

			# elif signal == True and (y >= 9 or (c[len(c)-1][0]*amount)>start_balance):
			# elif signal == True and (y >= 9 or (c[len(c)-1][0]*amount)>start_balance+0.005):
			# elif signal == True and (y >= 9 or (c[len(c)-1][0]*amount)>start_balance+0.005):
			# elif signal == True and (y >= 9 or (c[len(c)-1][0]*amount)>start_balance):
			# elif signal == True and (y >= 9 or c[len(c)-1][0] > purchase_price):
			# elif signal == True and (c[len(c)-1][0] < c[len(c)-1][1] or c[len(c)-1][0] < c[len(c)-1][2] or y >= 9 or (c[len(c)-1][0]*amount)>start_balance):
			# elif signal == True and (y >= 9 or c[len(c)-1][0]>purchase_price*1.001):
			elif signal == True and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]) and c[len(c)-2][1] > purchase_price*1.002:

				if c[len(c)-1][0]*amount > start_balance:
					balance = start_balance
					skim += ((c[len(c)-1][0]*amount)*.999)-start_balance 
					print(c[len(c)-1][0]*amount)
				else:
					balance = place_sell(amount, float(c[len(c)-1][0]))
					balance = balance*.999
				amount 	= 0
				signal 	= False
				y=0

			if y > 9:
				print("OVER 9000")

			print("*"*100)
			print("*"*100)
			print(c[len(c)-1])
			print(c[len(c)-1])
			print(c[len(c)-1])
			print(c[len(c)-1])
			print("*"*50)
			print("Y:   	"+str(y))
			print("curr:   	"+str(c[len(c)-1][0]))
			print("balance: "+str(balance))
			print("amount:  "+str(amount))
			print("signal:  "+str(signal))
			print("value:   "+str(amount*c[len(c)-1][0]))
			print("skim:  	"+str(skim))
			print("*"*50)
			g = open("log_" +  str(time_int) + "_" + str(crypto_name) + "_001_buy_sell_cross_sma.txt", "w+")
			g.write(str(balance) + " " + str(skim))
			time.sleep(time_int)
			# time.sleep(3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725)
		except:
			pass




# from Robinhood import Robinhood

#Setup
# my_trader = Robinhood()
#login
# my_trader.login(username=os.getenv("ROBINHOOD_USERNAME", "").encode(), password=os.getenv("ROBINHOOD_PASSWORD", "").encode())

# 3d961844-d360-45fc-989b-f6fca761d511
# print(my_trader.get_news("GEVO"))
# print(my_trader.last_updated_at("GEVO")[0])
# print(my_trader.get_account())
# print(my_trader.portfolios())
# print(my_trader.crypto_holdings())

# r.helper.get_device_token()

# print(r.get_all_watchlists())
# print(r.build_holdings())
# print(r.get_market_options())
# r.order_buy_crypto_by_price("BTC", 1.23, priceType="mark_price")
# r.order_buy_crypto_by_price("BTC",1.19)
# print(r.load_crypto_profile())
# print(r.load_account_profile())
# print(r.find_orders()[0])
# print(r.get_all_open_orders())
# print(r.get_all_option_positions())
# print(r.get_aggregate_positions())
# print(r.build_user_profile())
# print(r.load_crypto_profile())
# print(r.get_crypto_info("BTC"))
# print(r.get_crypto_quote("BTC"))
# print(r.get_crypto_quote_from_id("3d961844-d360-45fc-989b-f6fca761d511"))
# print(r.get_all_positions())
print("---------------------------")
print("---------------------------")
# r.request_get("https://api.robinhood.com/accounts/5QT20706/positions/)
# for asdf in r.load_crypto_profile():
# 	print(asdf)
# print("---------------------------")
# print("---------------------------")
# print("---------------------------")
# print(r.get_crypto_info("BTC"))
# print("---------------------------")
# print(r.get_crypto_quote("BTC"))
# https://api.robinhood.com/accounts/5QT20706/positions/43d961844-d360-45fc-989b-f6fca761d511/
# # init()https://api.robinhood.com/accounts/5QT20706/positions/4580fee1-f557-42f2-a8f0-330a276e8f88/
# 3d961844-d360-45fc-989b-f6fca761d511

init()