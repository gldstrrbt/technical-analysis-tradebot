import os
import time
import numpy as np
import pandas as pd
import robin_stocks as r
import robin_stocks.urls as urls
import robin_stocks.account as account
import robin_stocks.crypto as crypto
import robin_stocks.orders as orders
import robin_stocks.helper as helper
import robin_stocks.helper as profiles
from uuid import uuid4


# {'ask_price': '10149.610000', 'bid_price': '10123.981983', 'mark_price': '10136.795991', 'high_price': '10422.790000', 'low_price': '10095.090000', 'open_price': '10301.970000', 'symbol': 'BTCUSD', 'id': '3d961844-d360-45fc-989b-f6fca761d511', 'volume': '204169.156178'}

###################################################################################

def open_doc():
	a = open("creds.txt","r+")
	b = [c for c in a]
	return b 

###################################################################################

btc_id 		= "3d961844-d360-45fc-989b-f6fca761d511"
username 	= str(open_doc()[0])
password 	= str(open_doc()[1])
login 		= r.login(username,password)

###################################################################################

def get_quote():
	return r.get_crypto_quote_from_id(btc_id)

###################################################################################

def get_mark_price(quote_info):
	return round(float(quote_info["mark_price"]),2)
	
###################################################################################

def place_buy(amountInDollars, price):
	print(price)
	try:
		shares = round(amountInDollars/float(price),6)
	except:
		shares = 0

	print(shares)
	print("-"*50)
	print("-"*50)
	print("-"*50)
	print("-"*50)
	print("-"*50)
	print("-"*50)
	payload = {
	'mimeType': 'application/json',
	'account_id': os.getenv("ROBINHOOD_ACCOUNT_ID", ""),
	# 'account_id': crypto.load_crypto_profile(info="id"),
	# 'currency_pair_id': crypto_info['id'],
	'currency_pair_id': btc_id,
	'price': price,
	'quantity': shares,
	'ref_id': str(uuid4()),
	'side': 'buy',
	'time_in_force': 'gtc',
	'type': 'limit'
	# 'type': 'market'
	}
	url = urls.order_crypto()
	data = helper.request_post(url,payload,json=True)
	return(data)
	# return orders.order_buy_crypto_by_price("BTC",amount)

###################################################################################

def place_sell(amountInBtc, price):
	payload = {
	'account_id': os.getenv("ROBINHOOD_ACCOUNT_ID", ""),
	'currency_pair_id': btc_id,
	'price': price,
	'quantity': amountInBtc,
	'ref_id': str(uuid4()),
	'side': 'buy',
	'time_in_force': 'gtc',
	'type': 'limit'
	}

	url = urls.order_crypto()
	data = helper.request_post(url,payload,json=True)

	return(data)

###################################################################################

def get_usd_balance():
	return r.load_portfolio_profile()["excess_maintenance"]
	# return r.load_portfolio_profile()
	# return r.load_portfolio_profile()["equity"]
	# return r.get_all_positions()

###################################################################################

def get_crypto_balance_sheet():
	return r.get_crypto_positions()
	# return r.get_crypto_positions()[0]["cost_bases"][0]["direct_cost_basis"]

###################################################################################

def get_crypto_balance():
	return get_crypto_balance_sheet()[0]["quantity_available"]

###################################################################################

def get_crypto_cost_basis():
	return get_crypto_balance_sheet()[0]["cost_bases"][0]["direct_cost_basis"]

###################################################################################

def check_orders():
	url = urls.order_crypto()
	items = helper.request_get(url)
	items = [item for item in items['results'] if item['cancel_url'] is not None]
	return items

###################################################################################

def cancel_placed_orders(items_in_orders):
    items = items_in_orders
    for item in items:
        cancel_url = urls.cancel_crypto_orders(item["cancel_url"])
        print(cancel_url)
        data = helper.request_post(cancel_url)

    print('All Crypto Orders Cancelled')
    return(items)

###################################################################################

def countdown_to_cancel():
	a = 0
	b = 9
	while a < b:
		if a == b:
			cancel_placed_orders()
			break
		a = a+1
		time.sleep(0.5)

###################################################################################

def moving_average_alt(df, n):
	compiled_sma 	= pd.Series(df["mark_price"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df

###################################################################################

def data_to_df(datas):
	a = pd.DataFrame(datas, columns={"mark_price"})
	return a

###################################################################################

def mod_data_array(data_array):
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
	return c

###################################################################################

def init():
	amount 			= 0
	start_balance 	= float(get_usd_balance() )
	balance 		= float(start_balance) 
	signal 			= True
	purchase_price 	= 0
	skim 			= 0
	y 				= 0
	data_array 		= [5,3,4,5,12]
	time_int 		= 0.5
	crypto_name 	= "BTC"
	crypto_balance 	= float(get_crypto_balance())

	while True:
		signal_current  = signal
		orders_in_place = check_orders()
		orders_num 		= len(orders_in_place)
		btc_quote 		= get_quote()
		btc_mark_price 	= get_mark_price(btc_quote)
		data_array.append(btc_mark_price)
		
		if orders_num > 0:
			y+=1
		else:
			y=0
	
		if len(data_array) > 20:
			data_array.pop(0)

		c = mod_data_array(data_array)
		# a = data_to_df(data_array)
		# a = moving_average_alt(a, 3)
		# a = moving_average_alt(a, 5)
		# b = a.iterrows()
		# c = []

		# for d, e in b:
		# 	t = []
		# 	for s, r in enumerate(e):
		# 		t.append(float(r))
		# 	c.append(t)

		balance 		= float(get_usd_balance())
		crypto_balance 	= float(get_crypto_balance())
		
		if signal == True and orders_num == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
		# if signal != True and signal != False and balance > 10 and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
			if balance > start_balance:	
				place_buy(balance, str(btc_mark_price))
				signal = False 
			else:
				place_buy(balance, str(btc_mark_price))
				signal = False 
			
			purchase_price = float(btc_mark_price)

		# elif signal == True and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		# elif signal == False and crypto_balance > 1 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		# elif signal != True and signal != False and crypto_balance > 1 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		elif signal == False and orders_num == 0 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
			place_sell(crypto_balance, str(btc_mark_price))
			signal = True
		
		if y == 9:
			cancel_placed_orders()
			y=0
			if signal != signal_current:
				signal = signal_current
		
		print("-"*50)
		skim = balance-start_balance
		print("*"*100)
		print("*"*100)
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print("BUY TRIGGER: " + str(balance > 10))
		print("SELL TRIGGER: " + str(crypto_balance > 1))
		print("*"*50)
		print("Y:   	"+str(y))
		print("curr:   	"+str(c[len(c)-1][0]))
		print("balance: "+str(balance))
		print("amount:  "+str(crypto_balance))
		print("signal:  "+str(signal))
		print("value:   "+str(balance+crypto_balance))
		print("skim:  	"+str(skim))
		print("*"*50)
		time.sleep(0.5)


###################################################################################

# init()

###################################################################################

def test():
	a = float(get_crypto_balance())
	b = float(get_mark_price(get_quote()))
	# c = float(get_usd_balance())
	c = get_usd_balance()
	d = float(get_crypto_cost_basis())
	# e = get_quote()
	f = float(e["bid_price"])
	g = float(e["ask_price"])
	# h = place_buy(1.0, str(b))
	# i = place_sell(amountInBtc, str(b))
	print(a)
	# print(c)
	# print(f)
	# print(g)
	# print((g+f)/2)
	# print(b)
	# print()
	# print(d)
	# print(a*b)
	# print(c+d)
	# print(get_usd_balance())
	# print(h)
	print("--------------")
	print("--------------")
	print("--------------")
	print(get_usd_balance())
	print("-"*50)
	# cancel_placed_orders()
	# print(b["quantity_available"])
	# for c in b:
	# 	print(c)

test()