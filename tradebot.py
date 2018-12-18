import os, json, csv, requests, cbpro, matplotlib, mpl_finance
from bs4 import BeautifulSoup as soup
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.colors as colors 	
import matplotlib.font_manager as font_manager
from mpl_finance import candlestick2_ohlc
import datetime as datetime




  

# public_client = cbpro.PublicClient()
# LTC HISTORICAL DATA:
# https://www.cryptodatasets.com/platforms/Bitfinex/LTC/
# test = public_client.get_products()
# print(test)
# # Get the order book at the default level.
# order_book = public_client.get_product_order_book('LTC-USD')
# # Get the order book at a specific level.
# # order_book_lvl = public_client.get_product_order_book('LTC-USD', level=2)
# # print(order_book_lvl)
# print()
# # get_ticker = public_client.get_product_ticker(product_id='LTC-USD')
# # print(get_ticker)
# print()
# # get_trades = public_client.get_product_trades(product_id='LTC-USD')
# # print(get_trades)
# print()
# # get_stats = public_client.get_product_24hr_stats('LTC-USD')
# # print(get_stats)
# print()
# get_historic = public_client.get_product_historic_rates('LTC-USD')
# # print(get_historic)
# print()
# get_hist_gran = public_client.get_product_historic_rates('LTC-USD', granularity=86400)
# print(get_hist_gran)
# print()

def dd():
	print("*"*50)

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

# ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
def get_csv():
	csv_doc = open("./ltc_hour.csv")
	csv_read = csv.reader(csv_doc)
	csv_data = []
	for b, a in enumerate(csv_read):
		if b != 0:	
			csv_data.append(a)
	return csv_data

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def csv_reverse(csv_data):
	reversed_arr = []
	for a in reversed(csv_data):
		reversed_arr.append(a)
	return reversed_arr

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def check_closing_difference(dataset):
	new_arr = []
	x = 0
	while x < len(dataset):
		try:
			diff_val = float(dataset[x][4])-float(dataset[x-1][4])
			diff_percent = diff_val/float(dataset[x-1][4])
			volume_change_val = float(dataset[x][6])-float(dataset[x][5])
			new_arr.append({"date": dataset[x][0], "prev_date": dataset[x-1][0], "diff_val": diff_val, "diff_percent": diff_percent, "current_price": dataset[x][4], "volume_start": dataset[x][5], "volume_end": dataset[x][6], "volume_change_val":volume_change_val, "open_price": dataset[x][1],  "close_price": dataset[x][4], "high_price": dataset[x][2], "low_price": dataset[x][3], "marketcap": dataset[x][6]})
		except:
			pass
		x+=1
	return new_arr

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def get_gain_loss_rsi(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	rsi_array = []
	while counter < arr_len:
		all_rsi = []
		gains = [] # STORES VALUES FOR OPENING PRICE FOR SET TIME RANGE INDEXES
		losses = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			get_val_diff = float(dataset[sub_counter]["diff_val"])
			try:
				if get_val_diff > 0:
					gains.append(get_val_diff)
				else:
					losses.append(get_val_diff)
			except:
				pass
			sub_counter-=1
		dataset[counter]["rsi"] = process_rsi(gains, losses, time_range)
		dataset[counter]["gains"] = gains
		dataset[counter]["losses"] = losses
		counter += 1
	return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def process_rsi(gains, losses, time_range):
	gains = sum(gains)/time_range
	losses = (sum(losses)/time_range)*-1
	first_rsi = gains/losses
	rsi_period_end = 100-(100/(1+first_rsi))
	return rsi_period_end

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def max_min_avg(dataset, parameter):
	arr = []
	max_val = 0
	min_val = 0
	avg = 0
	for a in dataset:
		arr.append(float(a[parameter]))
	max_val = max(arr)
	min_val = min(arr)
	avg = sum(arr)/len(arr)
	dd()

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def stochastic_rsi(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	while counter < arr_len:
		rsi_array = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		ma_counter = 0
		ma_rsi = []
		while sub_counter > end_count:
			get_rsi = float(dataset[sub_counter]["rsi"])
			rsi_array.append(get_rsi)
			sub_counter-=1
			if sub_counter > 3:
				get_prev_rsi = float(dataset[sub_counter]["rsi"])
				ma_rsi.append(get_prev_rsi)
		stoch_a = ((float(dataset[counter]["rsi"])-float(min(rsi_array)))/(float(max(rsi_array))-float(min(rsi_array))))
		stoch_ma = ma_rsi
		dataset[counter]["stochastic"] = stoch_a
		try:
			dataset[counter]["stochastic_ma"] = sum(stoch_ma)/len(stoch_ma)
		except:
			pass
		counter+=1
	return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def smoothed_rsi(dataset, time_range):
	for b, a in enumerate(dataset):
		gains = float(sum(a["gains"]))/float(time_range)
		losses = float(sum(a["losses"]))/float(time_range)
		if a["diff_val"] > 0.0:
			rsi_sm = (((gains*(float(time_range)-1.0))+float(a["diff_val"]))/float(time_range))/((((losses*(float(time_range)-1.0))+0.0)/float(time_range))+1)
		elif a["diff_val"] < 0.0:
			rsi_sm = (((gains*(float(time_range)-1.0))+0.0)/float(time_range))/((((losses*(float(time_range)-1.0))+float(a["diff_val"]))/float(time_range))+1)
		dataset[b]["rsi_sm"] = float(rsi_sm)
	return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def get_sma(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	while counter < arr_len:
		price_arr = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			get_price = float(dataset[sub_counter]["current_price"])
			price_arr.append(get_price)
			sub_counter-=1

		sma_val = np.mean(price_arr)
		dataset[counter]["sma_" + str(time_range)] = sma_val
		counter+=1
	return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def get_vol_sma(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	while counter < arr_len:
		price_arr = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			get_price = float(dataset[sub_counter]["volume_end"])
			price_arr.append(get_price)
			sub_counter-=1

		sma_val = float(sum(price_arr))/int(len(price_arr))
		dataset[counter]["vol_sma_" + str(time_range)] = sma_val
		counter+=1
	return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def candle_type(dataset):
	counter = 0
	while counter < len(dataset):
		date = dataset[counter]["date"]
		open_val = float(dataset[counter]["open_price"])
		close_val = float(dataset[counter]["close_price"])
		open_close_avg = (open_val+close_val)/2
		high_val = float(dataset[counter]["high_price"])
		low_val = float(dataset[counter]["low_price"])
		high_low_avg = (high_val+low_val)/2

		with open("candle_test.csv", "a") as z:
			csv_out = csv.writer(z)
			csv_out.writerow([date, open_val, close_val, open_close_avg, high_val, low_val, high_low_avg])
		counter +=1

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def close_to_open(dataset):
	counter = 0
	while counter < len(dataset):
		close_val = float(dataset[counter-1]["close_price"])
		open_val = float(dataset[counter]["close_price"])
		counter +=1

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

# def stoch_d(dataset, time_range):
# 	counter = 0
# 	arr_len = len(dataset)
# 	rsi_array = []
# 	while counter < arr_len:
# 		start_count = counter 
# 		end_count = counter - time_range
# 		sub_counter = start_count
# 		while sub_counter > end_count:

	# 		try:
	# 		get_smoothed = float(dataset[sub_counter]["smoothed_rsi"])
	# 		rsi_array.append(get_smoothed)
	# 		# print(get_rsi)
	# 		sub_counter-=1
	# 		# print("-"*5)
	# 	# print("*"*50)
	# 	stoch = float(sum(rsi_array))/time_range
	# 	print(stoch)
	# 	dataset[counter]["stoch_d"] = stoch
	# 	counter+=1
	# return dataset

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################


# RSI Oversold in Uptrend
# [type = stock] AND [country = US] 
# AND [Daily SMA(20,Daily Volume) > 40000] 
# AND [Daily SMA(60,Daily Close) > 20] 

# AND [Daily Close > Daily SMA(200,Daily Close)] 
# AND [Daily RSI(5,Daily Close) <= 30]


# RSI Overbought in Downtrend
# [type = stock] AND [country = US] 
# AND [Daily SMA(20,Daily Volume) > 40000] 
# AND [Daily SMA(60,Daily Close) > 20] 

# AND [Daily Close < Daily SMA(200,Daily Close)] 
# AND [Daily RSI(5,Daily Close) >= 70]


def sim_trade(dataset):
	startup = False
	traded_low = False
	traded_high = False
	start_money = 1000
	start_quantity = 0
	min_amount = start_money
	end_money = 0
	end_quantity = 0
	for b, a in enumerate(dataset):
		twenty_fifty_sma_diff = float(a["sma_50"])-float(a["sma_20"])
		fifty_twohundred_sma_diff = float(a["sma_200"])-float(a["sma_50"])
		# if traded_low == False and float(a["vol_sma_20"]) < float(a["volume_end"]) and float(a["sma_20"]) > float(a["current_price"]) and float(a["rsi"]) <= 30 and float(a["sma_200"]) > float(a["current_price"]):
		# if traded_low == False and float(a["sma_50"]) >= float(a["sma_20"]) and twenty_fifty_sma_diff >= 0.000000001 and twenty_fifty_sma_diff <= 0.10000000 and fifty_twohundred_sma_diff <= 0.2000000 and fifty_twohundred_sma_diff >= 0.00000001:
		# if traded_low == False and float(a["sma_50"]) >= float(a["sma_20"]) and twenty_fifty_sma_diff >= 0.000000001 and twenty_fifty_sma_diff <= 0.100000000:
		if traded_low == False and fifty_twohundred_sma_diff >= 0.500000001 and fifty_twohundred_sma_diff <= 0.900000000 and float(a["rsi"]) <= 30:
		#	print("WOAH")
			#print(end_money)
		# try:
			# if(end_money != 0.0):
		# end_money = end_quantity*float(a["current_price"])
	# if float(a["smoothed_rsi"]) <= 30 and traded_low == False and ((start_money/float(a["current_price"]))*float(a["current_price"])) > start_money:
	# if float(a["rsi"]) <= 30 and traded_low == False and ((start_money/float(a["current_price"]))*float(a["current_price"])) > end_money*0.9:
		
		# if float(a["smoothed_rsi"]) <= 30 and traded_low == False and ((start_money/float(a["current_price"]))*float(a["current_price"])) > end_money*0.9 and float(a["diff_val"]) < 0.0:
	#	if float(a["rsi"]) <= 25 and traded_low == False and float(a["vol_sma_20"]) < float(a["volume_end"]):
		#if float(a["rsi"]) <= 30 and traded_low == False and float(a["diff_val"]) < 0.0:
	#	if startup == True and float(a["rsi"]) >= 91 and traded_high == False  and float(a["diff_val"]) > 0.0:
			print("stochastic")
			print(a["stochastic"])
			print(a["stochastic_ma"])
			print("-"*50)
			print("")
			print(end_money)
			print("")
			print(a)
			print(a["current_price"])
			if startup == False:
				start_quantity = start_money/float(a["current_price"]) 
				end_quantity = start_quantity
				end_money = start_quantity*float(a["current_price"])
				startup = True
			elif startup == True:
				end_quantity = float(end_money/float(a["current_price"]))
				end_money = end_quantity*float(a["current_price"])
				print(end_money)
			traded_low = True
			traded_high = False

			print("BOUGHT")
			print(a["date"])
			print("VOLUME END: " + str(a["volume_end"]))
			print("VOLUME SMA: " + str(a["vol_sma_20"]))
			print("QUANTITY: " + str(end_quantity))
			print("TOTAL: " + str(end_money))
			print("---")
		# ((start_money/float(a["current_price"]))*float(a["current_price"])):
		# elif startup == True and float(a["rsi"]) >= 90 and traded_high == False:
		# elif startup == True and float(a["rsi"]) >= 90 and traded_high == False  and ((start_money/float(a["current_price"]))*float(a["current_price"])) > start_money:
		# elif startup == True and float(a["rsi"]) >= 90 and traded_high == False  and ((start_money/float(a["current_price"]))*float(a["current_price"])) > end_money*0.9:
		# elif startup == True and float(a["rsi"]) >= 80 and traded_high == False  and ((start_money/float(a["current_price"]))*float(a["current_price"])) > end_money*0.9 and float(a["diff_val"]) > 0.0:
	
	#	elif float(a["vol_sma_20"]) < float(a["volume_end"]) and float(a["sma_20"]) > float(a["current_price"]) and float(a["rsi"]) <= 30 and float(a["sma_200"]) > float(a["current_price"]):
		# elif startup == True and traded_high == False and float(a["rsi"]) >= 80 and float(a["vol_sma_20"]) < float(a["volume_end"]):
		# elif startup == True and traded_high == False and float(a["sma_50"]) <= float(a["sma_20"]) and twenty_fifty_sma_diff >= -0.200000001 and twenty_fifty_sma_diff <= 0.000000001 and fifty_twohundred_sma_diff >= -0.100000001 and fifty_twohundred_sma_diff <= 0.000000001:
		# elif startup == True and traded_high == False and float(a["sma_50"]) <= float(a["sma_20"]) and twenty_fifty_sma_diff >= -0.100000001 and twenty_fifty_sma_diff <= 0.000000001:
		elif startup == True and traded_high == False and fifty_twohundred_sma_diff >= -0.100000001 and fifty_twohundred_sma_diff <= 0.000000001 and float(a["rsi"]) >= 80:
			print("stochastic")
			print(a["stochastic"])
			print(a["stochastic_ma"])
			print("-"*50)

	#	elif startup == True and float(a["rsi"]) >= 91 and traded_high == False  and float(a["diff_val"]) > 0.0:
			print("")
			print(end_money)
			print("")
			print(a)
			end_money = end_quantity*float(a["current_price"])
			end_quantity = 0
			traded_low = False
			traded_high = True
			print("SOLD")
			print(a["date"])
			print("VOLUME END: " + str(a["volume_end"]))
			print("VOLUME SMA: " + str(a["vol_sma_20"]))
			print("QUANTITY: " + str(end_quantity))
			print("TOTAL: " + str(end_money))
			print("---")
		# except:
		# 	pass

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def plotem(dataset):
	counter = 0
	dates = [] 
	open_val = [] 
	close_val = [] 
	high_val = [] 
	low_val = [] 
	high_low_avg = []
	open_close_avg = []
	sma_twenty = []
	sma_fifty = []
	sma_two_hund = []
	# aapl = data.DataReader('AAPL', 'google', '2017-06-01')
	while counter < len(dataset):
		dates.append(dataset[counter]["date"])
		sma_twenty.append(float(dataset[counter]["sma_20"]))
		sma_fifty.append(float(dataset[counter]["sma_50"]))
		sma_two_hund.append(float(dataset[counter]["sma_200"]))
		open_val.append(float(dataset[counter]["open_price"]))
		close_val.append(float(dataset[counter]["close_price"]))
		high_val.append(float(dataset[counter]["high_price"]))
		low_val.append(float(dataset[counter]["low_price"]))
		hi_lo_avg = (float(dataset[counter]["low_price"])+float(dataset[counter]["high_price"]))/2.0
		open_close = (float(dataset[counter]["open_price"])+float(dataset[counter]["close_price"]))/2.0
		high_low_avg.append(float(hi_lo_avg))
		open_close_avg.append(float(open_close))
		counter+=1

	plt.ion()
	fig, ax = plt.subplots()
	candlestick2_ohlc(ax,open_val,high_val,low_val,close_val, colorup="#FFFFFF", colordown="#FF0000", width=2.0)
	xdate = dates
	# xdate = [datetime.datetime.fromtimestamp(i) for i in quotes['time']]

	ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

	def mydate(x,pos):
	    try:
	        return xdate[int(x)]
	    except IndexError:
	        return ''

	ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	ax.set_facecolor((0.0, 0.0, 0.0))
	fig.autofmt_xdate()
	# fig.tight_layout()

	# PLOT CANDLE AVERAGES
	# plt.plot(dates, open_close_avg, color="b", linewidth=1.5)
	# plt.plot(dates, high_low_avg, color="m", linewidth=1.5)
	
	# PLOT SMAs
	plt.plot(dates, sma_twenty, color="g", linewidth=1.5)
	plt.plot(dates, sma_fifty, color="y", linewidth=1.5)
	plt.plot(dates, sma_two_hund, color="b", linewidth=1.5)


	plt.draw()
	plt.grid(True)
	# plt.draw()
	# plt.pause(50)
	plt.show(block=True)

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

def init():
	time_range = 14
	dataset = csv_reverse(get_csv())
	dataset = check_closing_difference(dataset)
	dataset = get_gain_loss_rsi(dataset, time_range)
	# dataset = get_gain_loss_rsi(dataset, time_range)
	# print(dataset)
	# dataset = stochastic_rsi(dataset, time_range)
	# print(dataset)
	# for a in dataset:
	# 	print(a["volume_change_val"])
	dataset = get_sma(dataset, 20)
	dataset = get_sma(dataset, 50)
	dataset = get_sma(dataset, 100)
	dataset = get_sma(dataset, 200)

	dataset = get_vol_sma(dataset, 20)
	dataset = get_vol_sma(dataset, 50)
	dataset = get_vol_sma(dataset, 100)
	dataset = get_vol_sma(dataset, 200)
	dataset = stochastic_rsi(dataset, 14)


	
	plotem(dataset)
	# candle_type(dataset)
	# for a in dataset:
	# 	print("sma_20: " + str(a["sma_20"]))
	# 	print("sma_50: " + str(a["sma_50"]))
	# 	print("sma_100: " + str(a["sma_100"]))
	# 	print("sma_200: " + str(a["sma_200"]))
	# 	print()
	# 	print("vol_sma_20: " + str(a["vol_sma_20"]))
	# 	print("vol_sma_50: " + str(a["vol_sma_50"]))
	# 	print("vol_sma_100: " + str(a["vol_sma_100"]))
	# 	print("vol_sma_200: " + str(a["vol_sma_200"]))
	# 	print()
	# 	dd()
		# for b in a:
			# if "sma_" in str(b):
			# 	print(b)
			# 	print(a[b])
			# 	print()
	# print(sma_twenty)
	# for a in sma_twenty:
	# 	print(a["date"])
	# 	print(a["sma_20"])
	# 	dd()

	# dataset = smoothed_rsi(dataset, time_range)
	# dataset = stoch_d(dataset, 3)

	# print(dataset)
	# print()
	# max_min_avg(dataset, "current_price")
	# max_min_avg(dataset, "rsi")
	sim_trade(dataset)
	# return dataset

init()



###########################################################################
###########################################################################
###########################################################################
# STRATEGIES!
###########################################################################
###########################################################################
###########################################################################


# RSI Oversold in Uptrend
# [type = stock] AND [country = US] 
# AND [Daily SMA(20,Daily Volume) > 40000] 
# AND [Daily SMA(60,Daily Close) > 20] 

# AND [Daily Close > Daily SMA(200,Daily Close)] 
# AND [Daily RSI(5,Daily Close) <= 30]




# RSI Overbought in Downtrend
# [type = stock] AND [country = US] 
# AND [Daily SMA(20,Daily Volume) > 40000] 
# AND [Daily SMA(60,Daily Close) > 20] 

# AND [Daily Close < Daily SMA(200,Daily Close)] 
# AND [Daily RSI(5,Daily Close) >= 70]
