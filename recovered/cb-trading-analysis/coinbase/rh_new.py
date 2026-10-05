import os, json, requests, time, csv, matplotlib, mpl_finance
from Robinhood import Robinhood
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.colors as colors
import matplotlib.font_manager as font_manager
from mpl_finance import candlestick2_ohlc
from mpl_finance import index_bar
from mpl_finance import plot_day_summary_oclh
import datetime as datetime
# import robin_stocks as r
# shit = r.get_historicals("TSLA")
# print(shit)

####################################################################################################
####################################################################################################
####################################################################################################

# test 							= Robinhood()

####################################################################################################
####################################################################################################
####################################################################################################

def create_category_csv():
	for b, a in enumerate(ticker_collection):
		c = open("./ticker_categories/" + str(category_names[b]) + ".csv", "w+")
		d = csv.writer(c)
		for e in a:
			d.writerow([e])

####################################################################################################
####################################################################################################
####################################################################################################

#  URL FOR ACCESSING HISTORICALS: https://api.robinhood.com/quotes/historicals/?symbols=AMD,CRSP&interval=day&span=week
def get_ticker_dataset(tickers, interval, span):
	tickers = strip_tag_array(tickers)
	a 		= requests.get("https://api.robinhood.com/quotes/historicals/?symbols=" + str(tickers) + "&interval=" + str(interval) + "&span=" + str(span) + "")
	b 		= a.text
	b 		= json.loads(b)
	return b

####################################################################################################
####################################################################################################
####################################################################################################

def get_news(tick):
	ticker_news = test.get_news(tick)
	return ticker_news

####################################################################################################
####################################################################################################
####################################################################################################

def get_tagged_tickers(tagnames):
	tickers = []
	for a in tagnames:
		b = requests.get("https://api.robinhood.com/midlands/tags/tag/"+a+"/")
		c = json.loads(b.text)
		# print(c)
		if "{'detail': 'Not found.'}" not in str(c):
			for d in c["instruments"]:
				e = requests.get(d)
				f = json.loads(e.text)
				tickers.append(f["symbol"])
	return tickers

####################################################################################################
####################################################################################################
####################################################################################################

def log_tag_changes(tagname):
	a 			= "./_tagname_historical_data"
	b 			= a + "/" + str(datetime.datetime.now()).split(" ")[0].replace("-", "")
	c 			= b + "/" + tagname + ".csv"
	if not os.path.exists(a):
		os.makedirs(a, exist_ok=True)
	if not os.path.exists(b):
		os.makedirs(b, exist_ok=True)
	if not os.path.exists(c):
		tickers = get_tagged_tickers([str(tagname)])
		d = open(c, "w+")
		e = csv.writer(d)
		for f in tickers:
			e.writerow([f])

####################################################################################################
####################################################################################################
####################################################################################################

def init_tag_logging():
	for z in tags:	
		print()
		print("-"*50)
		print(z)
		print("-"*50)
		print()
		log_tag_changes(str(z))
		print()
		print("-"*50)
		print(z)
		print("-"*50)
		print()

####################################################################################################
####################################################################################################
####################################################################################################

def get_instrument(tick):
	# stock_instrument = test.instruments(tick)[0]
	stock_instrument = test.instruments(tick)
	# for a in stock_instrument:
		# print(a)
		# try:
		# 	print(stock_instrument[a])
		# except:
		# 	pass
		# print(stock_instrument[a])
		# print("*"*50)
	return stock_instrument

####################################################################################################
####################################################################################################
####################################################################################################

# buy_order = test.place_buy_order(stock_instrument, 1)
# sell_order = test.place_sell_order(stock_instrument, 1)

# process_tickers(rh_list)

# results
# # interval
# # quote
# # instrument
# # span
# # symbol
# # bounds
# # historicals
# # # open_price 
# # # close_price 
# # # begins_at 
# # # interpolated 
# # # session 
# # # high_price 
# # # low_price 
# # # volume

####################################################################################################
####################################################################################################
####################################################################################################

def strip_tag_array(tickers):
	tickers = str(tickers).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
	return tickers

####################################################################################################
####################################################################################################
####################################################################################################

def get_hist_values(historical_data):
	historical_data = historical_data["historicals"]
	entries 		= []
	for a in historical_data:
		for b in a:
			# print(a)
			# print(b)
			# for c in a[b]:
			if "close_price" in str(b):	
				entries.append(a[b])
					# try:
					# except:
					# 	pass
	return entries
		# print(historical_data[a])

####################################################################################################
####################################################################################################
####################################################################################################

def get_close_avg(close_price):
	prices 				= []
	closing_averages 	= {}
	for a in close_price:
		try:
			prices.append(float(a["close_price"]))
		except:
			pass
	closing_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	closing_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	closing_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	closing_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	closing_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	closing_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	closing_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	return closing_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_open_avg(open_price):
	prices 				= []
	opening_averages 	= {}
	for a in open_price:
		try:
			prices.append(float(a["open_price"]))
		except:
			pass
	opening_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	opening_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	opening_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	opening_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	opening_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	opening_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	opening_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	return opening_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_averages(dataset, price_type):
	prices 				= []
	opening_averages 	= {}
	for a in dataset:
		try:
			prices.append(float(a["open_price"]))
		except:
			pass
	opening_averages["span_total_avg"] 	= float(sum(prices)/len(prices))
	opening_averages["1_day_avg"] 		= float(sum(prices[-1:])/len(prices[-1:]))
	opening_averages["10_day_avg"] 		= float(sum(prices[-10:])/len(prices[-10:]))
	opening_averages["20_day_avg"] 		= float(sum(prices[-20:])/len(prices[-20:]))
	opening_averages["50_day_avg"] 		= float(sum(prices[-50:])/len(prices[-35:]))
	opening_averages["100_day_avg"] 	= float(sum(prices[-100:])/len(prices[-100:]))
	opening_averages["200_day_avg"] 	= float(sum(prices[-200:])/len(prices[-120:]))
	# print(opening_averages)
	return opening_averages

####################################################################################################
####################################################################################################
####################################################################################################

def get_open_close_avg(open_avg, close_avg):
	# prices 			= []
	open_close_averages = {}
	for a in open_avg:
		try:
			prices 						= [float(open_avg[a]), float(close_avg[a])]
			price_sum 					= sum(prices)
			price_len 					= len(prices)
			open_close_averages[str(a)] = price_sum/price_len
		except:
			pass
	# open_close_averages["span_total_open_avg"] = float(sum(prices)/len(prices))
	# open_close_averages["20_day_open_avg"] = float(sum(prices[-20:])/len(prices[-20:]))
	# open_close_averages["50_day_open_avg"] = float(sum(prices[-50:])/len(prices[-35:]))
	# open_close_averages["100_day_open_avg"] = float(sum(prices[-100:])/len(prices[-100:]))
	# open_close_averages["200_day_open_avg"] = float(sum(prices[-200:])/len(prices[-120:]))
	return open_close_averages

# def get_value_gap(value_set_a, value_set_b):

####################################################################################################
####################################################################################################
####################################################################################################

def process_percent_change_daily(price_data):
	for a in price_data:
		change = float(a["open_price"])/float(a["close_price"])
		print("PERCENT CHANGE DAILY: " + str(change))

####################################################################################################
####################################################################################################
####################################################################################################

def get_percent_change(value_set_a, value_set_b):
	# percent_change 	= (value_set_a - value_set_b)/(value_set_a + value_set_b)
	percent_change 		= float(value_set_a)/float(value_set_b)
	return float(percent_change)

####################################################################################################
####################################################################################################
####################################################################################################

def plotem(industry, dataset):
	counter 		= 0
	dates 			= [] 
	open_val 		= [] 
	close_val 		= [] 
	high_val 		= [] 
	low_val 		= [] 
	high_low_avg 	= []
	open_close_avg 	= []
	sma_twenty 		= []
	sma_fifty 		= []
	sma_two_hund 	= []
	if industry == False:
		# aapl = data.DataReader('AAPL', 'google', '2017-06-01')
		while counter < len(dataset):
			dates.append(dataset[counter]["begins_at"])
			sma_twenty.append(float(dataset[counter]["sma_20"]))
			sma_fifty.append(float(dataset[counter]["sma_50"]))
			sma_two_hund.append(float(dataset[counter]["sma_200"]))
			open_val.append(float(dataset[counter]["open_price"]))
			close_val.append(float(dataset[counter]["close_price"]))
			high_val.append(float(dataset[counter]["high_price"]))
			low_val.append(float(dataset[counter]["low_price"]))
			hi_lo_avg 	= (float(dataset[counter]["low_price"])+float(dataset[counter]["high_price"]))/2.0
			open_close 	= (float(dataset[counter]["open_price"])+float(dataset[counter]["close_price"]))/2.0
			high_low_avg.append(float(hi_lo_avg))
			open_close_avg.append(float(open_close))
			counter+=1
	elif industry == True:
		for a in dataset:
			print(dataset[a])
			print()
			print()
			dates.append(a)
			open_val.append(dataset[a]["price_open_avg"])
			close_val.append(dataset[a]["price_close_avg"])
			low_val.append(dataset[a]["price_low_avg"])
			high_val.append(dataset[a]["price_high_avg"])


	plt.ion()
	fig, ax = plt.subplots()
	candlestick2_ohlc(ax,open_val,high_val,low_val,close_val, colorup="#FFFFFF", colordown="#FF0000", width=2.0)
	# index_bar(ax, close_val, facecolor='b', edgecolor='r', width=1, alpha=1.0)
	# plot_day_summary_oclh(ax, close_val, ticksize=3, colorup='k', colordown='r')

	xdate 	= dates
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
	plt.plot(dates, close_val, color="#664444", linewidth=1.5)
	plt.plot(dates, sma_twenty, color="g", linewidth=1.5)
	plt.plot(dates, sma_fifty, color="y", linewidth=1.5)
	plt.plot(dates, sma_two_hund, color="m", linewidth=1.5)


	plt.draw()
	plt.grid(True)
	# plt.draw()
	# plt.pause(50)
	plt.show(block=True)


####################################################################################################
####################################################################################################
####################################################################################################

def get_sma(dataset, time_range):
	counter = 0
	arr_len = len(dataset)
	while counter < arr_len:
		price_arr = []
		start_count = counter 
		end_count = counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			# print("-"*50)
			# print(dataset[sub_counter])
			# print("-"*50)
			# get_price = float(dataset[sub_counter])
			try:
				get_price = float(dataset[sub_counter]["close_price"])
				price_arr.append(get_price)
				sub_counter-=1
			except:
				pass

		sma_val = np.mean(price_arr)
		dataset[counter]["sma_" + str(time_range)] = sma_val
		counter+=1
	return dataset

####################################################################################################
####################################################################################################
####################################################################################################

def convert_to_date_index(dataset):
	new_dataset = {}
	for a in dataset:
		new_dataset[str(a["begins_at"])] = a
	return new_dataset

####################################################################################################
####################################################################################################
####################################################################################################

def gather_industries(tickers, intervals, time_range):
	tag_set = {}
	for a in tickers:
		test_hist_data = get_hist_values(test.get_ticker_dataset_quotes(str(a), intervals, time_range))
		dataset = get_sma(test_hist_data, 20)
		dataset = get_sma(dataset, 50)
		dataset = get_sma(dataset, 200)
		dataset = convert_to_date_index(dataset)
		for b in dataset:
			if b not in tag_set:
				tag_set[b] = {}
				tag_set[b][a] = dataset[b]
			else:	
				tag_set[b][a] = dataset[b]
	return tag_set

####################################################################################################
####################################################################################################
####################################################################################################

def get_industries_sma(dataset):
	industry_values = {}
	for a in dataset:
		# print(a)
		closing_prices = []
		opening_prices = []
		high_prices = []
		low_prices = []
		# opening_prices = []
		for b in dataset[a]:
			opening_prices.append(float(dataset[a][b]["open_price"]))
			closing_prices.append(float(dataset[a][b]["close_price"]))
			high_prices.append(float(dataset[a][b]["high_price"]))
			low_prices.append(float(dataset[a][b]["low_price"]))
		industry_values[a] = {"price_open_avg":np.mean(opening_prices), "price_close_avg":np.mean(closing_prices), "price_high_avg":np.mean(high_prices), "price_low_avg":np.mean(low_prices)}
	# print(industry_values)
	return industry_values

####################################################################################################
####################################################################################################
####################################################################################################

def get_markets():
	a = requests.get("https://api.robinhood.com/markets/")
	b = a.text
	c = json.loads(b)
	return c

####################################################################################################
####################################################################################################
####################################################################################################

def market_direction(indexname, direction):
	a = requests.get("https://api.robinhood.com/midlands/movers/"+indexname+"/?direction="+direction+"")
	b = a.text
	c = json.loads(b)
	return c

####################################################################################################
####################################################################################################
####################################################################################################

def test_moving_averages(tag, time_interval, time_span):
	test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "week", "5year"))
	# test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "day", "year"))
	# test_hist_data = get_hist_values(test.get_ticker_dataset_quotes("CRSP", "5minute", "week"))
	# get_averages(test_hist_data, "close_price")
	
	dataset = get_sma(test_hist_data, 20)
	dataset = get_sma(dataset, 50)
	dataset = get_sma(dataset, 200)

	##############################
	### INDUSTRIES TEST
	##############################

	# dataset 		= convert_to_date_index(dataset)
	# INTERVALS 	= ['15second', '5minute', '10minute', 'hour', 'day', 'week']
	# SPANS 		= ['day', 'hour', 'week', 'year', '5year', 'all']

	# dataset = gather_industries(global_stocks, "week", "5year")
	# dataset = gather_industries(tag, time_interval, time_span)
	# dataset = gather_industries(beer, "week", "5year")
	# dataset = gather_industries(asia, "week", "5year")
	# dataset = gather_industries(r_and_d, "week", "5year")
	# dataset = gather_industries(electric_utilities, "week", "5year")
	# dataset = gather_industries(renewables, "day", "year")
	# dataset = gather_industries(renewables, "week", "5year")
	# dataset = gather_industries(female_ceo, "week", "5year")
	# dataset = gather_industries(loan, "week", "5year")
	# dataset = gather_industries(real_estate, "week", "5year")
	# dataset = gather_industries(kids, "week", "5year")
	# dataset = gather_industries(entertainment, "week", "5year")
	# dataset = gather_industries(manufacturing, "week", "5year")
	# dataset = gather_industries(e_commerce, "week", "5year")
	# dataset = gather_industries(retail, "week", "5year")
	# dataset = gather_industries(broadcasting, "week", "5year")
	# dataset = gather_industries(digital_television, "week", "5year")
	# dataset = gather_industries(television, "week", "5year")
	# dataset = gather_industries(electronics, "week", "5year")
	# dataset = gather_industries(radio, "week", "5year")
	# dataset = gather_industries(automotive, "week", "5year")
	# dataset = gather_industries(transportation, "week", "5year")
	# dataset = gather_industries(telecommunications, "week", "5year")
	# dataset = gather_industries(upcoming_earnings, "week", "5year")
	# dataset = gather_industries(computer_hardware, "week", "5year")
	# dataset = gather_industries(material, "week", "5year")
	# dataset = gather_industries(packaging, "week", "5year")
	# dataset = gather_industries(business_service, "week", "5year")
	# dataset = gather_industries(etf, "week", "5year")
	# dataset = gather_industries(aerospace, "week", "5year")
	# dataset = gather_industries(air_transportation, "week", "5year")
	# dataset = gather_industries(professional_service, "week", "5year")
	# dataset = gather_industries(investment_service, "week", "5year")
	# dataset = gather_industries(cancer_prevention, "week", "5year")
	# dataset = gather_industries(outsourcing, "week", "5year")
	# dataset = gather_industries(logistics, "week", "5year")
	# dataset = gather_industries(most_popular_under_twenty_five, "week", "5year")
	# dataset = gather_industries(sports, "week", "5year")
	# dataset = gather_industries(consumer_product, "week", "5year")
	
	# for a inphotovoltaic:
	# 	print(dataset[a])
	dataset = get_industries_sma(dataset)
	# print(dataset)
	plotem(True, dataset)

	##############################
	##############################
	##############################
	

	# print(dataset)
	# plotem(tag_or_ticker, dataset)

	# print("OPENING AVERAGES: " +  str(get_open_avg(test_hist_data)))
	# print("CLOSING AVERAGES: " + str(get_close_avg(test_hist_data)))
	# print("OPENING + CLOSING AVERAGES: " + str(get_open_close_avg(get_open_avg(test_hist_data), get_close_avg(test_hist_data))))

	# value_set_a = get_close_avg(test_hist_data)
	# value_set_a = value_set_a["10_day_avg"]

	# value_set_b = get_open_avg(test_hist_data)
	# value_set_b = value_set_b["10_day_avg"]
	# print(value_set_a)
	# print(value_set_b)
	# print("DAILY PERCENT CHANGE: " + str(get_percent_change(float(value_set_a), float(value_set_a))))
	# process_percent_change_daily(test_hist_data)
	# print(test_hist_data)
	# counter = 0
	# arr_len = len(test_data)
	# print(arr_len)
	# while counter < arr_len:
	# 	try:
	# 		print(test_data[counter:counter+14])
	# 	except:
	# 		pass
	# 	# print(counter)
	# 	counter += 1
	# for a in test_hist_data:
	# 	print(len(test_hist_data))
	# 	print(a["close_price"])
	# print("OPENING + CLOSING AVERAGES: " + str(get_open_close_avg(get_open_avg(test_hist_data), get_close_avg(test_hist_data))))
	# print(test.get_ticker_dataset_quotes("FB", "day", "year"))
	# print(test.get_ticker_dataset_quotes("FB", "week", "5year"))


####################################################################################################
####################################################################################################
####################################################################################################

# dataset 		= convert_to_date_index(dataset)
# tickers 		= [] # Enter array of tickers
# time_interval = ['15second', '5minute', '10minute', 'hour', 'day', 'week']
# time_span 	= ['day', 'hour', 'week', 'year', '5year', 'all']
def plot_tickers(tickers, time_interval, time_span):
	dataset = gather_industries(tickers, time_interval, time_span)
	dataset = get_industries_sma(dataset)
	# print(dataset)
	plotem(True, dataset)

####################################################################################################
####################################################################################################
####################################################################################################

def get_price_data(historical_dataset):
	# for b, a in enumerate(historical_dataset["results"]):
		# print()
		# print("-"*50)
		# print()
		# print(a["symbol"])
		# print()
		# print("-"*50)
		# print()
		# for c in historical_dataset["results"][b]["historicals"]:
		# 	print(c)
	return historical_dataset["results"]
	# return historical_dataset["results"][b]["historicals"]

####################################################################################################
####################################################################################################
####################################################################################################


####################################################################################################
########################################## INITIAL STEPS ###########################################
####################################################################################################

# 1. INIT TAG COLLECTION AND SAVE LOCALLY
## Create a local copy of ticker groupings to avoid making a ton of requests/slowing down the process
# init_tag_logging()

# 2. COLLECT HISTORICAL QUOTES AND SAVE LOCALLY

# 3. UPDATE 

####################################################################################################
########################################### BACKTESTING ############################################
####################################################################################################

# 1. UPDATE DATA COLLECTIONS. TAGS AND QUOTES

# 2. CHECK FOR INCOMPLETE TAG LISTINGS/CSV FILES

# 3. RUN DIFFS ON TAG SETS. COMPARE CHANGES IN GROUPINGS. SIMPLY CHECK LEN AND MEMBERSHIP COUNTS

# 4. PROCESS SMAs AND ANY OTHER INDICATOR

# 5. PLOT EM

# 6. CREATE BRIEF REPORTS ON TAG COLLECTIONS. SIMPLE CHANGE DETECTION IF IMPATIENT 

# plot_tickers(alcohol, "week", "5year")
# print(test.get_news("FB"))
# plot_tickers(["AMD"], "week", "5year")
# plot_tickers(television, "week", "5year")
# process_tickers(loan)
# test_moving_averages(television, "week", "5year")
# print(test.instruments("BTC"))
# print(test.news("FB"))
# print(test.get_popularity("FB"))
# print(test.get_tickers_by_tag("technology"))
# print(test.get_fundamentals("FB"))
# get_ticker_dataset("FB", "day", "year")
# testing = get_ticker_dataset("FB", "day", "year")
# print(get_ticker_dataset("FB", "day", "year"))



# print(get_markets())
# print(market_direction("sp500", "up"))



# def get_sma_diff_range(dataset, sma_type):
# 	diffs = []
# 	for a in dataset:
# 		# test_fract 	= float(a["sma_" + str(sma_type[0])])/float(a["sma_" + str(sma_type[1])])
# 		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
# 		diffs.append(float(test_diff))
# 	diffs.sort()
	
# 	front 	= []
# 	back  	= []
# 	counter = 0
# 	ends 	= int(len(diffs)*.2)
# 	backend = len(diffs)-ends

# 	while counter < ends:
# 		# print(diffs[counter])
# 		# print(ends)
# 		# print(backend)
# 		# print(counter)
# 		front.append(diffs[counter])
# 		counter+=1
	
# 	counter = 1
# 	# print(ends)
# 	# print()
# 	while (ends-counter)+backend > backend:
# 		# print(diffs[(ends-counter)+backend])
# 		back.append(diffs[(ends-counter)+backend])
# 		# print((ends-counter)+backend)
# 		counter+=1

# 	# print("*"*50)
# 	# print(np.mean(front))
# 	# print(np.mean(back))
# 	# print("*"*50)
# 	return [np.mean(front), np.mean(back)]
def moving_average_alt(df, n):
	"""Calculate the moving average for the given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	compiled_sma 	= pd.Series(df["close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df



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




def get_sma_diff_range_from_center(dataset, sma_type):
	diffs = []
	for a in dataset:
		test_fract 	= float(a["sma_" + str(sma_type[1])])/float(a["sma_" + str(sma_type[2])])
		test_diff 	= float(a["sma_" + str(sma_type[1])])-float(a["sma_" + str(sma_type[2])])
		diffs.append(float(test_diff))
	diffs.sort()
	
	front 	= []
	back  	= []
	counter = 0
	center 	= int(len(diffs)/2)
	# ends 	= int(center*.009)
	ends 	= int(30)
	
	frontend = center-ends
	backend = center-ends
	# print(frontend)
	# print(backend)

	while (center-counter) > center-frontend:
		# print(diffs[center-counter])
		# print(ends)
		# print(backend)
		# print(center-counter)
		front.append(diffs[center-counter])
		counter+=1
	
	counter = 0
	# print(ends)
	# print(center+backend)
	
	while (center+counter) < center+backend:
		try:	
			# print(diffs[center+counter])
			back.append(diffs[center+counter])
			# print(center+counter)
			counter+=1
		except:
			break

	# print("*"*50)
	# print(np.mean(front))
	# print(np.mean(back))
	# print("*"*50)
	return [np.mean(front), np.mean(back)]

###########################################################################
###########################################################################
###########################################################################
	
def get_gain_loss_rsi(dataset, time_range):
	counter 	= 0
	arr_len 	= len(dataset)
	rsi_array 	= []
	while counter < arr_len:
		all_rsi 	= []
		gains 		= [] # STORES VALUES FOR OPENING PRICE FOR SET TIME RANGE INDEXES
		losses 		= []
		start_count = counter 
		end_count 	= counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			get_val_diff = float(dataset[sub_counter]["close_price"])-float(dataset[sub_counter-1]["close_price"])
			try:
				if get_val_diff > 0:
					gains.append(get_val_diff)
				else:
					losses.append(get_val_diff)
			except:
				pass
			sub_counter-=1
		dataset[counter]["rsi"] 	= process_rsi(gains, losses, time_range)
		dataset[counter]["gains"] 	= gains
		dataset[counter]["losses"] 	= losses
		counter += 1
	return dataset

###########################################################################
###########################################################################
###########################################################################
	
def get_gain_loss_mfi(dataset, time_range):
	counter 	= 0

	while counter < len(dataset):
		pos_flow 		= [] # STORES VALUES FOR OPENING PRICE FOR SET TIME RANGE INDEXES
		neg_flow 		= []
		start_count = counter 
		end_count 	= counter - time_range
		sub_counter = start_count
		while sub_counter > end_count:
			get_val_diff = float(dataset[sub_counter]["typical_price"])-float(dataset[sub_counter-1]["typical_price"])
			try:
				if get_val_diff > 0:
					pos_flow.append(float(dataset[sub_counter]["money_flow"]))
				else:
					neg_flow.append(float(dataset[sub_counter]["money_flow"]))
			except:
				pass
			sub_counter-=1
		
		# pos_flow 									= 0
		# neg_flow 									= 0
		# money_rat 									= 0
		# dataset[counter]["pos_flow"] 				= 0
		# dataset[counter]["neg_flow"] 				= 0
		# dataset[counter]["money_ratio"] 			= 0
		# dataset[counter]["money_flow_index"] 		= 0
		# dataset[counter]["money_flow_index_alt"] 	= 0
		# try:
		pos_f 										= sum(pos_flow)
		# print(pos_f)
		neg_f 										= sum(neg_flow)
		if neg_f == 0:
			money_rat 									= pos_f/1
		else:
			money_rat 									= pos_f/neg_f
		dataset[counter]["pos_flow"] 				= pos_f
		dataset[counter]["neg_flow"] 				= neg_f
		dataset[counter]["money_ratio"] 			= money_rat
		dataset[counter]["money_flow_index"] 		= 100-(100/(1+money_rat))
		dataset[counter]["money_flow_index_alt"] 	= 100*(pos_f/(pos_f+neg_f))
		# except:
		# 	pass

		counter += 1
		
		# try:
		# 	neg_flow 									= float(sum(neg_flow))
		# except:
		# 	print()
		
		# try:
		# 	money_rat 									= pos_flow/neg_flow
		# except:
		# 	print()
		
		# try:
		# 	dataset[counter]["pos_flow"] 				= pos_flow
		# except:
		# 	print()
		
		# try:
		# 	dataset[counter]["neg_flow"] 				= neg_flow
		# except:
		# 	print()		
		
		# try:
		# 	dataset[counter]["money_ratio"] 			= money_rat
		# except:
		# 	print()
		
		# try:
		# 	dataset[counter]["money_flow_index"] 		= 100-(100/(1+money_rat))
		# except:
		# 	print()
		
		# try:
		# 	dataset[counter]["money_flow_index_alt"] 	= 100*(pos_flow/(pos_flow+neg_flow))
		# except:
		# 	print()
		
	return dataset

###########################################################################
###########################################################################
###########################################################################

def check_closing_difference(dataset):
	x = 0
	while x < len(dataset):
		try:
			diff_val 					= float(dataset[x]["close_price"])-float(dataset[x-1]["close_price"])
			diff_percent 				= diff_val/float(dataset[x-1]["close_price"])
			dataset[x]["diff_val"] 		= diff_val
			dataset[x]["diff_percent"] 	= diff_percent
		except:
			pass
		x+=1
	return dataset

###########################################################################
###########################################################################
###########################################################################

def process_rsi(gains, losses, time_range):
	try:	
		gains = sum(gains)/time_range
		losses = (sum(losses)/time_range)*-1
		first_rsi = gains/losses
		rsi_period_end = 100-(100/(1+first_rsi))
		return rsi_period_end
	except:
		pass

###########################################################################
###########################################################################
###########################################################################

def get_mf(dataset):
	a = 0
	while a < len(dataset):
		b = dataset[a]["high_price"]
		c = dataset[a]["low_price"]
		d = dataset[a]["close_price"]
		e = (a+b+c)/3
		f = e*dataset[a]["volume"]

		dataset[a]["typical_price"] = e
		dataset[a]["money_flow"] 	= f
		a+=1
	return dataset
		
	

###########################################################################
###########################################################################
###########################################################################





# get_tagged_tickers(["photovoltaic"])
# testing = get_ticker_dataset(photovoltaic, "day", "year")
# testing = get_ticker_dataset(["AMD"], "5minute", "week")
# testing = get_ticker_dataset(["AMD"], "week", "5year")
# testing = get_price_data(testing) 
# testing = r.get_historicals("CRON", "week")
# x = open("ltc_cb.json", "r+")
# x = open("gemini_BTCUSD_2018_1min.csv", "r+")
# w = []
# v = csv.reader(x)
# t = 0
# for u in v:
# 	print(u)
# 	try:
# 		w.append({"begins_at": u[1], "close_price": float(u[6])})
# 	except:
# 		pass
# 	# t +=1
# print(w)

# testing = w
# dataset = get_sma(testing, 1)
# # dataset = get_sma(testing[0]["historicals"], 2)