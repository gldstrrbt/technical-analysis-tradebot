import os
import time
import numpy as np
import pandas as pd
import robin_stocks as r
import robin_stocks.crypto as crypto
import robin_stocks.orders as orders
import robin_stocks.helper as helper
from Robinhood import Robinhood
from robinhood_crypto_api import RobinhoodCrypto

order_id 		= ""
shit = RobinhoodCrypto("<REDACTED_EMAIL>", "!Bling4jlo3")
print(shit)

login 		= r.login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))
my_trader 	= Robinhood()
my_trader.login(username=os.getenv("ROBINHOOD_USERNAME", "").encode(), password=os.getenv("ROBINHOOD_PASSWORD", "").encode())

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

def place_buy(amount, val):
	global order_id
	order_id = orders.order_buy_crypto_by_price("BTC",amount)
	order_id = order_id["id"]
	# buy_market_order_info = shit.trade(
	#     'BTCUSD',
	#     # price=val,
	#     price=round(float(amount) * 1.005, 2),
	#     quantity=round(float((amount-0.000001)/val), 6),
	#     side="buy",
	#     time_in_force="gtc",
	#     type="limit"
	# )
	# order_id = buy_market_order_info["id"]
	# print(buy_market_order_info)

def append_data(dataset):
	b = []
	for c in dataset:
		b.append(c)
	return b

def get_crypto_amount():
	a = my_trader.crypto_holdings()
	return float(a["results"][0]["quantity"])

def get_fiat_amount():
	return float(my_trader.get_account()["crypto_buying_power"])

def init():
	global order_id
	amount 			= 0
	start_balance 	= get_fiat_amount() 
	balance 		= start_balance 
	
	signal 			= ""
	purchase_price 	= 0
	skim 			= 0
	y 				= 0
	data_array 		= [5,3,4,5,12]
	time_int 		= 0.5
	crypto_name 	= "BTC"

	crypto_balance 	= get_crypto_amount()

	while True:
		# try:	
		fuck = crypto.get_crypto_quote(crypto_name)
		data_array.append(float(fuck["mark_price"]))
		if len(data_array) > 20:
			data_array.pop(0)
		# print("*"*50)
		a = data_to_df(data_array)
		a = moving_average_alt(a, 3)
		a = moving_average_alt(a, 5)
		b = a.iterrows()
		c = []
		for d, e in b:
			t = []
			for s, r in enumerate(e):
				t.append(float(r))
			c.append(t)
		# bb = balance
		time.sleep(time_int)
		# balance 		= get_fiat_amount()
		# crypto_balance 	= get_crypto_amount()
		time.sleep(time_int)
		if signal == True:
			y+=1

		# if signal == False and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
		if signal != True and signal != False and balance > 10 and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
			
			if get_fiat_amount() > start_balance:	
				place_buy(start_balance, c[len(c)-1][0])
				purchase_price 	= float(c[len(c)-1][0])
				# signal 			= True 
			else:
				place_buy(balance, c[len(c)-1][0])
				# signal 			= True 
			# balance 		= get_fiat_amount()


		# elif signal == True and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		elif signal != True and signal != False and crypto_balance*round(float(fuck["mark_price"]), 4) > 10 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
			order_id = orders.order_sell_crypto_by_price("BTC", round(crypto_balance*float(fuck["mark_price"])*0.99999, 6))
			order_id = order_id["id"]
			# orders.order_sell_crypto_by_price("BTC", str(crypto_balance*c[len(c)-1][0]))
			# print(round(float(c[len(c)-1][0])*0.99999, 2))
			# print(float(c[len(c)-1][0])*0.99999)
			# print(float(c[len(c)-1][0]))
			# print(c[len(c)-1][0])
			# print(crypto_balance)
			# print(crypto_balance*0.99999)
			# print("*"*50)
			signal = True
			crypto_balance 	= get_crypto_amount()
			# sell_market_order_info = shit.trade(
			#     'BTCUSD',
			#     price=round(float(c[len(c)-1][0])*0.9, 2),
			#     quantity=crypto_balance*0.99999,
			#     side="sell",
			#     time_in_force="gtc",
			#     type="limit"
			# )

		skim = balance-start_balance
		print("*"*100)
		print("*"*100)
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print("BUY TRIGGER: " + str(balance > 10))
		print("SELL TRIGGER: " + str(crypto_balance*float(fuck["mark_price"]) > 10))
		print("*"*50)
		print("Y:   	"+str(y))
		print("curr:   	"+str(c[len(c)-1][0]))
		print("balance: "+str(balance))
		print("amount:  "+str(crypto_balance))
		# print("signal:  "+str(signal))
		print("value:   "+str((crypto_balance*c[len(c)-1][0])+balance))
		print("skim:  	"+str(skim))
		print("*"*50)
		# g = open("log_" +  str(time_int) + "_" + str(crypto_name) + "_live_first_run.txt", "w+")
		# g.write(str(balance) + " " + str(skim))
		time.sleep(time_int)
		if y == 9:
			balance 		= get_fiat_amount()
			crypto_balance 	= get_crypto_amount()
			signal 			= ""
			y = 0
			my_trader.cancel_crypto(order_id)

		# time.sleep(3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725)
		# except:
		# 	pass


# print(get_crypto_amount())
# for zzz in get_crypto_amount():
# 	print(zzz)

# init()
my_trader.cancel_crypto(order_id)

# print(orders.get_all_open_orders())


import random

def GenerateDeviceToken():
    rands = []
    for i in range(0,16):
        r = random.random()
        rand = 4294967296.0 * r
        rands.append((int(rand) >> ((3 & i) << 3)) & 255)

    hexa = []
    for i in range(0,256):
        hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

    id = ""
    for i in range(0,16):
        id += hexa[rands[i]]

        if (i == 3) or (i == 5) or (i == 7) or (i == 9):
            id += "-"

    # self.device_token = id
    print(id) #can get rid of this in API code

# GenerateDeviceToken()