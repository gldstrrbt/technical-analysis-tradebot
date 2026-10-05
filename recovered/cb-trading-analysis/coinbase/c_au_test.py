import cbpro, os, time, csv, json, websocket
import datetime as datetime
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
import numpy as np

# os.system("mongod")

public_client = cbpro.PublicClient()

# a = public_client.get_product_ticker(product_id='ETH-USD')
# print(a)
# # for b in a:
# # 	print(b)
# b = public_client.get_product_historic_rates('ETH-USD')
# print(b)

# c = public_client.get_product_24hr_stats('ETH-USD')
# print(c)

# d = public_client.get_product_24hr_stats('ETH-USD')
# print(d)

# e = public_client.get_currencies()
# print(e)

# f = public_client.get_time()
# print(f)

#################################################
#################################################

def get_hist():
		# DATA STARTS AT 2016-05-18
		# {60, 300, 900, 3600, 21600, 86400}
		# one minute, five minutes, fifteen minutes, one hour, six hours, and one day

		a = public_client.get_product_historic_rates("ETH-USD", "2016-05-18T00:00", "2016-05-18T00:59", 300)
		print(a)
		# yy = 2016
		# mm = 01
		# dd = 01
		# hh = 00
		# mm = 00

#################################################
#################################################

def auth():
	key = os.getenv("COINBASE_API_KEY", "")
	b64secret = os.getenv("COINBASE_API_SECRET", "")
	passphrase = os.getenv("COINBASE_API_PASSPHRASE", "")
	auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
	# Use the sandbox API (requires a different set of API access credentials)
	# auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, api_url="https://api-public.sandbox.pro.coinbase.com")
	return auth_client

#################################################
#################################################

def my_fills():
	g = auth()
	h = g.get_fills("ETH-USD")
	for i in h:
		print(i)
	print(h)
	# i = 

#################################################
#################################################

def my_account():
	a = auth()
	b = a.get_account()
	print(b)

#################################################
#################################################

def my_orders():
	a = auth()
	b = a.get_orders()
	return b

#################################################
#################################################

def get_stats():
	a = public_client.get_product_24hr_stats('ETH-USD')
	return a

#################################################
#################################################

# def check_ticker():
# 	a = public_client.get_product_ticker(product_id='ETH-USD')
# 	return a

#################################################
#################################################

def convert_time(timeset):
	a = str(timeset).split(".")
	a = a[0]
	b = datetime.strptime(a, "%Y-%m-%dT%H:%M:%S")
	print(b)

#################################################
#################################################

def check_time():
	a = public_client.get_time()
	return a
	# y = str(x["created_at"]).split(".")
	# y = y[0]
	# z = datetime.strptime(y, "%Y-%m-%dT%H:%M:%S")

#################################################
#################################################

def compare_time():
	for x in my_orders():
		if "ltc" in str(x).lower():
			print("shit")
			print(x["created_at"])
			print(x["created_at"])
			print(x["created_at"])
			# y = str(x["created_at"]).replace("T", " ")
			# y = str(x["created_at"]).split("T")
			y = str(x["created_at"]).split(".")
			y = y[0]
			print(y)
			print(y)
			print(y)
			print(y)
			print(y)
			print(datetime.strptime(y, "%Y-%m-%dT%H:%M:%S"))
			print(datetime.strptime(y, "%Y-%m-%dT%H:%M:%S"))
			print(datetime.strptime(y, "%Y-%m-%dT%H:%M:%S"))
			print(datetime.strptime(y, "%Y-%m-%dT%H:%M:%S"))
			z = datetime.strptime(y, "%Y-%m-%dT%H:%M:%S")
			if z < datetime.now():
				print()
				print(z)
				print(datetime.now())
				print(datetime.now()-z)

#################################################
#################################################

def test_ws():
	a = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD", should_print=True)
	# Do other stuff...
	b = a.start()
	print("--------------------")
	print(b)
	print("--------------------")
	print("--------------------")

	# print(a)
	# a.close()
	# for b in a:
	# 	print(b)

# class myWebsocketClient(cbpro.WebsocketClient):
# 	def on_open(self):
# 		self.url = "wss://ws-feed.pro.coinbase.com/"
# 		self.products = ["LTC-USD"]
# 		self.message_count = 0
# 		print("Lets count the messages!")
# 	def on_message(self, msg):
# 		self.message_count += 1
# 		try:
# 			print(msg["reason"])
# 		except:
# 			pass
# 		# if 'price' in msg and 'type' in msg:
# 		#     print ("Message type:", msg["type"],
# 		#            "\t@ {:.3f}".format(float(msg["price"])))
# 	def on_close(self):
# 		print("-- Goodbye! --")

def wtf():
	wsClient = myWebsocketClient()
	wsClient.start()
	print(wsClient)
	for a in wsClient:
		print(b)
	# print(wsClient.url, wsClient.products)
	# while (wsClient.message_count < 500):
	#     print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
	#     time.sleep(1)
	wsClient.close()

def log_eth():
	mongo_client = MongoClient('mongodb://localhost:27017/')

	# specify the database and collection
	db = mongo_client.cryptocurrency_database
	eth_collection = db.eth_collection

	# instantiate a WebsocketClient instance, with a Mongo collection as a parameter
	wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="ETH-USD",
	    mongo_collection=eth_collection, should_print=True)
	wsClient.start()

#################################################
#################################################

def test_mongo():
	a = MongoClient('localhost',27017)
	# b = a.get_database("cryptocurrency_database")
	b = a["cryptocurrency_database"]
	print(b)
	print(b.eth_collection)
	print(b.eth_collection.find({}))
	c = b.eth_collection.find({})
	f = [] 
	for d in c:
		# print(d)
		if "filled" in str(d) and "price" in str(d):
			# print(d)
			# try:
			# print(d["reason"])
			# except:
			# 	pass
			# try:
			print(d["time"])
			print(d["price"])
			# except:
			# 	pass
			f.append({"begins_at": d["time"], "close_price":d["price"]})
			print("------------------")
			print("------------------")
	
	e = open("test_mongo.json", "w+")
	e.write(json.dumps(f))
	# c = b.collection.find().count()
	# c = b.list_collection_names()
	# b = a.database_names()
	# c = b[2].find()
	# print(c)

#################################################
#################################################

def get_sma(dataset, time_range):
	# counter = 0
	# arr_len = len(dataset)
	# while counter < arr_len:
	price_arr = []
	start_count = len(dataset)-1
	end_count = start_count - time_range
	sub_counter = start_count
	while sub_counter > end_count:
		try:
			get_price = float(dataset[sub_counter]["close_price"])
			price_arr.append(get_price)
			sub_counter-=1
		except:
			pass

	sma_val = np.mean(price_arr)
	dataset[start_count]["sma_" + str(time_range)] = sma_val
	return dataset

#################################################
#################################################

def get_diffs(dataset, sma_type):
	diffs 	= []
	for a in dataset:
		test_diff 	= float(a["sma_" + str(sma_type[0])])-float(a["sma_" + str(sma_type[1])])
		diffs.append(float(test_diff))

	diffs.sort()

#################################################
#################################################

def feedback(order_date, signal, price_per, balance, valuation, quantity):
	# print("-"*50)
	# print(test_fract)
	# print(test_diff)
	# print("-"*50)
	print("-----------------")
	print("DATE:      " + str(order_date))
	print("SIGNAL:    " + str(signal))
	print("PRICE PER: " + str(price_per))
	print("BALANCE:   " + str(balance))
	print("VALUATION: " + str(valuation))
	print("QUANTITY:  " + str(quantity))
	print("-----------------")

#################################################
#################################################

def get_sma_diff_range(dataset, sma_type):
	diffs 	= []

	dataset_end = len(dataset)
	dataset_start = dataset_end-100
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
	ends 	= int(len(diffs)*.2)
	backend = len(diffs)-ends

	while counter < ends:
		front.append(diffs[counter])
		counter+=1
	
	counter = 1

	while (ends-counter)+backend > backend:
		back.append(diffs[(ends-counter)+backend])
		counter+=1
	return [np.mean(front), np.mean(back)]

#################################################
#################################################

start_balance 	= 1000
balance 		= start_balance
quantity 		= 0.0
last_val 		= 0.0
buy 			= False
valuation 		= 0.0
signal 			= "BOUGHT"
diff 			= 100.0*(float(start_balance)/float(balance))
test_diff 		= 0
sell_thresh 	= 0
buy_thresh 		= 0



def backtest(dataset):
	
	# try:
	buy_thresh = get_sma_diff_range(dataset, sma_type)[0]
	sell_thresh = get_sma_diff_range(dataset, sma_type)[1]
	# print(sma_type)
	# except:
		# pass

	# for d in dataset:
	d = dataset[len(dataset)-1]
	# test_fract 	= float(d["sma_" + str(sma_type[0])])/float(d["sma_" + str(sma_type[1])])
	test_diff 	= float(d["sma_" + str(sma_type[0])])-float(d["sma_" + str(sma_type[1])])
	order_date 	= d["begins_at"]
	print("-------")
	print("-------")
	print(d)
	print("-------")
	print(buy_thresh)
	print(sell_thresh)
	print("-------")
	print(test_diff)
	print("-------")
	print("-------")
	# if test_fract > 1.007 and buy == True and float(start_balance) > 0.0:
	if test_diff > sell_thresh and buy == True and quantity*float(d["close_price"]) > float(start_balance) and last_val < quantity*float(d["close_price"]):
	# if test_diff > sell_thresh and buy == True and quantity*float(d["close_price"]) > float(start_balance):
		balance 	= quantity*float(d["close_price"])
		# balance 	= balance - (float(balance)*0.003)
		valuation	= 0.0
		quantity 	= 0.0
		buy 		= False
		signal 		= "SOLD"
		last_val 	= balance
		# try:
		# 	diff 	= 100.0-(float(start_balance)/float(valuation))
		# except:
		# 	pass
		feedback(order_date, signal, d["close_price"], balance, valuation, quantity)
	# elif test_fract < 0.990 and buy == False and float(d["close_price"]) > 0.0:
	elif test_diff < buy_thresh and buy == False and float(d["close_price"]) > 0.0 and balance >= 1000:
	# elif test_diff < buy_thresh and buy == False and float(d["close_price"]) > 0.0:
		quantity 	= balance/float(d["close_price"])
		balance 	= 0.0
		valuation	= quantity*float(d["close_price"])
		# valuation 	= valuation - (float(valuation)*0.003)
		last_val 	= valuation
		buy 		= True
		signal 		= "BOUGHT"
		# try:
		# 	diff 	= 100.0-(float(start_balance)/float(valuation))
		# except:
		# 	pass
		feedback(order_date, signal, d["close_price"], balance, valuation, quantity)
	print("")
	print("-------"*10)
	print("-------"*10)



# backtest(dataset)

#################################################
#################################################

def testing():
	a 			= []
	start_log 	= False
	sma_a 		= 1
	sma_b 		= 3
	ff = [{"begins_at": "2019-01-22T05:21:24.441Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:23:16.573Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:23:18.926Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:23:40.803Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:23:45.437Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:06.253Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:06.814Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:09.650Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:41.855Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:48.274Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:25:56.526Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:26:34.420Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:27:18.468Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:27:19.426Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:27:23.294Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:27:41.746Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:27:51.750Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:27:53.269Z", "close_price": "116.26000000"}, {"begins_at": "2019-01-22T05:28:22.310Z", "close_price": "116.26000000"}, {"begins_at": "2019-01-22T05:28:57.793Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:29:03.170Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:29:05.281Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:29:47.368Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:29:54.529Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:30:09.628Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:30:12.990Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:30:20.140Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:31:24.432Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:31:54.893Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:32:59.617Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:33:09.374Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:33:39.796Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:33:59.437Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:34:39.283Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T05:35:09.997Z", "close_price": "116.34000000"}, {"begins_at": "2019-01-22T05:35:15.631Z", "close_price": "116.42000000"}, {"begins_at": "2019-01-22T05:35:43.842Z", "close_price": "116.42000000"}, {"begins_at": "2019-01-22T05:35:47.182Z", "close_price": "116.42000000"}, {"begins_at": "2019-01-22T05:35:49.498Z", "close_price": "116.42000000"}, {"begins_at": "2019-01-22T05:36:06.413Z", "close_price": "116.42000000"}, {"begins_at": "2019-01-22T05:36:33.140Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:36:34.155Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:36:45.685Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:37:02.267Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:37:13.542Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:37:41.469Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:37:44.881Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:37:49.802Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:38:33.334Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:39:35.492Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:39:38.353Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:39:40.375Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:40:07.493Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:40:09.912Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:41:11.204Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T05:41:22.892Z", "close_price": "116.35000000"}, {"begins_at": "2019-01-22T05:41:30.544Z", "close_price": "116.33000000"}, {"begins_at": "2019-01-22T05:41:50.130Z", "close_price": "116.33000000"}, {"begins_at": "2019-01-22T05:41:58.741Z", "close_price": "116.34000000"}, {"begins_at": "2019-01-22T05:42:01.363Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T05:42:41.946Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T05:42:49.410Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:43:54.748Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:44:30.586Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:44:46.251Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:45:02.900Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:45:11.124Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:45:14.686Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:45:31.780Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:45:45.190Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:45:47.186Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:45:48.904Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:46:22.197Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:46:41.162Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:47:14.510Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:47:17.871Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:47:27.850Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:47:45.232Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:47:52.540Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:48:03.954Z", "close_price": "116.40000000"}, {"begins_at": "2019-01-22T05:49:42.613Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:50:09.270Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T05:50:18.275Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:51:03.848Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:51:12.548Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:51:22.303Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:51:55.558Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T05:51:57.730Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:52:04.400Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:52:15.529Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:52:24.273Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:52:40.649Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:52:51.451Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:53:02.485Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:53:22.598Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T05:54:16.501Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:54:33.807Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T05:54:38.292Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:54:59.108Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T05:55:46.370Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T05:56:02.600Z", "close_price": "116.46000000"}, {"begins_at": "2019-01-22T05:56:04.240Z", "close_price": "116.53000000"}, {"begins_at": "2019-01-22T05:56:06.243Z", "close_price": "116.55000000"}, {"begins_at": "2019-01-22T05:56:06.753Z", "close_price": "116.57000000"}, {"begins_at": "2019-01-22T05:56:11.794Z", "close_price": "116.52000000"}, {"begins_at": "2019-01-22T05:56:13.789Z", "close_price": "116.50000000"}, {"begins_at": "2019-01-22T05:56:15.477Z", "close_price": "116.43000000"}, {"begins_at": "2019-01-22T05:56:22.284Z", "close_price": "116.52000000"}, {"begins_at": "2019-01-22T05:56:54.505Z", "close_price": "116.47000000"}, {"begins_at": "2019-01-22T05:57:05.722Z", "close_price": "116.47000000"}, {"begins_at": "2019-01-22T05:57:44.470Z", "close_price": "116.47000000"}, {"begins_at": "2019-01-22T05:57:49.508Z", "close_price": "116.46000000"}, {"begins_at": "2019-01-22T05:57:56.795Z", "close_price": "116.49000000"}, {"begins_at": "2019-01-22T05:58:45.939Z", "close_price": "116.46000000"}, {"begins_at": "2019-01-22T05:59:05.783Z", "close_price": "116.41000000"}, {"begins_at": "2019-01-22T05:59:09.718Z", "close_price": "116.33000000"}, {"begins_at": "2019-01-22T05:59:48.423Z", "close_price": "116.33000000"}, {"begins_at": "2019-01-22T05:59:54.750Z", "close_price": "116.34000000"}, {"begins_at": "2019-01-22T05:59:58.909Z", "close_price": "116.36000000"}, {"begins_at": "2019-01-22T06:00:10.840Z", "close_price": "116.35000000"}, {"begins_at": "2019-01-22T06:00:35.983Z", "close_price": "116.28000000"}, {"begins_at": "2019-01-22T06:00:48.454Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T06:01:03.247Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T06:01:16.860Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T06:01:20.335Z", "close_price": "116.27000000"}, {"begins_at": "2019-01-22T06:01:21.592Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T06:01:30.180Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T06:01:37.634Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T06:02:44.643Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T06:03:18.889Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T06:03:21.323Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T06:05:12.195Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T06:05:19.903Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T06:05:43.985Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T06:06:16.703Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T06:06:21.609Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T06:06:24.235Z", "close_price": "116.13000000"}, {"begins_at": "2019-01-22T06:06:24.966Z", "close_price": "116.11000000"}, {"begins_at": "2019-01-22T06:06:29.600Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T06:06:31.808Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T06:06:36.201Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T06:06:38.770Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T06:06:41.358Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:06:56.128Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:07:00.626Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:07:05.782Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:07:15.841Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T06:07:27.448Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T06:07:28.966Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T06:08:07.159Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T06:08:11.306Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:08:16.820Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T06:08:27.100Z", "close_price": "115.83000000"}, {"begins_at": "2019-01-22T06:08:45.713Z", "close_price": "115.83000000"}, {"begins_at": "2019-01-22T06:08:55.897Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T06:09:08.963Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:09:16.243Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:09:46.231Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T06:09:50.362Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:09:54.387Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:09:54.885Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:09:56.361Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:10:18.632Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:11:24.280Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:11:36.801Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:11:44.448Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:11:54.546Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T06:12:23.908Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T06:12:49.290Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T06:14:17.359Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:14:25.174Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:14:34.880Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T06:14:45.141Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:14:57.659Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T06:15:06.419Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T06:15:07.640Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T06:15:09.807Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T06:15:16.215Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T06:15:17.343Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:15:20.760Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:15:53.671Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T06:16:09.804Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:16:15.638Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T06:16:17.397Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T06:16:23.417Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:16:40.892Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:16:59.238Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:17:15.639Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T06:17:31.321Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T06:17:49.130Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T06:18:21.921Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:18:41.300Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:18:52.198Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T06:18:59.690Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:19:13.675Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:19:40.150Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:20:15.963Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:20:16.528Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:20:24.485Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:20:46.210Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:21:16.585Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:21:31.971Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:21:52.586Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:22:08.980Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:22:09.119Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:22:56.623Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:23:06.110Z", "close_price": "115.65000000"}, {"begins_at": "2019-01-22T06:23:19.178Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T06:23:21.695Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T06:23:36.637Z", "close_price": "115.65000000"}, {"begins_at": "2019-01-22T06:24:02.621Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:24:21.180Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:25:12.252Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:25:14.620Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:25:17.959Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:25:23.660Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:25:25.658Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:25:35.518Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T06:25:38.168Z", "close_price": "115.28000000"}, {"begins_at": "2019-01-22T06:25:45.888Z", "close_price": "115.28000000"}, {"begins_at": "2019-01-22T06:25:48.828Z", "close_price": "115.28000000"}, {"begins_at": "2019-01-22T06:25:59.181Z", "close_price": "115.31000000"}, {"begins_at": "2019-01-22T06:26:01.174Z", "close_price": "115.31000000"}, {"begins_at": "2019-01-22T06:26:15.775Z", "close_price": "115.16000000"}, {"begins_at": "2019-01-22T06:26:19.730Z", "close_price": "115.34000000"}, {"begins_at": "2019-01-22T06:26:21.938Z", "close_price": "115.34000000"}, {"begins_at": "2019-01-22T06:26:30.858Z", "close_price": "115.46000000"}, {"begins_at": "2019-01-22T06:26:45.750Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T06:27:17.522Z", "close_price": "115.41000000"}, {"begins_at": "2019-01-22T06:27:37.821Z", "close_price": "115.41000000"}, {"begins_at": "2019-01-22T06:27:48.242Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T06:27:51.339Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:27:59.769Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:28:04.528Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T06:28:20.665Z", "close_price": "115.44000000"}, {"begins_at": "2019-01-22T06:28:22.800Z", "close_price": "115.43000000"}, {"begins_at": "2019-01-22T06:28:25.120Z", "close_price": "115.44000000"}, {"begins_at": "2019-01-22T06:28:42.341Z", "close_price": "115.44000000"}, {"begins_at": "2019-01-22T06:28:49.386Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:29:04.100Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:29:24.300Z", "close_price": "115.48000000"}, {"begins_at": "2019-01-22T06:29:25.441Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:29:40.454Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:30:04.106Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:30:05.440Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:30:29.257Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:30:47.978Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:30:52.257Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:31:24.242Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:31:37.688Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:31:46.180Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:32:08.740Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:32:27.344Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T06:32:48.928Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T06:32:57.287Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T06:32:58.940Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T06:33:08.576Z", "close_price": "115.65000000"}, {"begins_at": "2019-01-22T06:33:14.474Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T06:33:20.585Z", "close_price": "115.67000000"}, {"begins_at": "2019-01-22T06:33:30.282Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T06:33:31.418Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T06:34:42.412Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:34:48.116Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T06:34:50.460Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:35:10.121Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:35:10.332Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:35:13.705Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T06:35:14.696Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:35:23.778Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T06:35:28.216Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T06:35:32.136Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T06:35:32.687Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T06:36:08.695Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T06:36:12.180Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T06:36:20.385Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T06:36:28.119Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T06:36:58.746Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T06:38:05.890Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T06:38:11.572Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T06:38:37.652Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T06:39:07.416Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:39:21.897Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:39:57.580Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:40:07.260Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:40:32.122Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:41:01.200Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:41:09.393Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:41:17.631Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:41:21.177Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:41:33.866Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:41:34.430Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:41:45.340Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:41:48.400Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:42:59.919Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:43:18.215Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:43:26.288Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:44:35.224Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:44:41.706Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:44:46.510Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:44:57.376Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:46:48.181Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:47:11.394Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:48:00.390Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:48:21.780Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:48:49.765Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T06:49:00.390Z", "close_price": "115.95000000"}, {"begins_at": "2019-01-22T06:50:33.249Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T06:50:40.470Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T06:50:51.900Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T06:51:07.960Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T06:52:00.120Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T06:52:10.563Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T06:52:26.950Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T06:52:26.943Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T06:52:40.550Z", "close_price": "115.84000000"}, {"begins_at": "2019-01-22T06:52:54.869Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:53:09.908Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T06:53:40.934Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T06:53:48.111Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T06:54:27.228Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T06:54:59.672Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:55:04.497Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:55:05.938Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T06:55:17.651Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:55:38.708Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:55:51.931Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:56:13.770Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T06:56:45.621Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T06:57:00.318Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T06:57:34.432Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:57:42.479Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:57:53.283Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:58:06.522Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:58:38.660Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T06:59:24.970Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T06:59:38.761Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:59:50.274Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T06:59:59.998Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T07:00:02.868Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T07:00:08.248Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T07:00:25.319Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T07:00:41.569Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T07:00:43.913Z", "close_price": "115.67000000"}, {"begins_at": "2019-01-22T07:00:46.106Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T07:01:06.491Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T07:01:12.202Z", "close_price": "115.67000000"}, {"begins_at": "2019-01-22T07:01:17.201Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:01:26.135Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:01:35.740Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:01:42.823Z", "close_price": "115.53000000"}, {"begins_at": "2019-01-22T07:01:44.969Z", "close_price": "115.51000000"}, {"begins_at": "2019-01-22T07:01:55.139Z", "close_price": "115.43000000"}, {"begins_at": "2019-01-22T07:01:57.549Z", "close_price": "115.41000000"}, {"begins_at": "2019-01-22T07:02:04.929Z", "close_price": "115.37000000"}, {"begins_at": "2019-01-22T07:02:09.132Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T07:02:12.773Z", "close_price": "115.36000000"}, {"begins_at": "2019-01-22T07:02:23.923Z", "close_price": "115.36000000"}, {"begins_at": "2019-01-22T07:02:26.830Z", "close_price": "115.33000000"}, {"begins_at": "2019-01-22T07:02:28.965Z", "close_price": "115.40000000"}, {"begins_at": "2019-01-22T07:02:34.455Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T07:03:10.684Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T07:03:18.756Z", "close_price": "115.46000000"}, {"begins_at": "2019-01-22T07:03:50.520Z", "close_price": "115.52000000"}, {"begins_at": "2019-01-22T07:04:27.142Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:04:45.199Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:04:52.960Z", "close_price": "115.56000000"}, {"begins_at": "2019-01-22T07:05:00.611Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T07:05:03.665Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T07:05:32.110Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T07:05:42.634Z", "close_price": "115.32000000"}, {"begins_at": "2019-01-22T07:05:52.565Z", "close_price": "115.30000000"}, {"begins_at": "2019-01-22T07:05:57.253Z", "close_price": "115.31000000"}, {"begins_at": "2019-01-22T07:06:00.535Z", "close_price": "115.39000000"}, {"begins_at": "2019-01-22T07:06:28.610Z", "close_price": "115.46000000"}, {"begins_at": "2019-01-22T07:06:39.870Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T07:06:44.874Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T07:06:54.139Z", "close_price": "115.52000000"}, {"begins_at": "2019-01-22T07:07:24.615Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:07:35.596Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:08:23.383Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:08:25.870Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T07:08:28.842Z", "close_price": "115.60000000"}, {"begins_at": "2019-01-22T07:08:56.945Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T07:09:02.168Z", "close_price": "115.58000000"}, {"begins_at": "2019-01-22T07:09:46.311Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:10:14.937Z", "close_price": "115.47000000"}, {"begins_at": "2019-01-22T07:11:26.500Z", "close_price": "115.51000000"}, {"begins_at": "2019-01-22T07:11:29.303Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T07:11:46.745Z", "close_price": "115.51000000"}, {"begins_at": "2019-01-22T07:11:50.804Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T07:11:55.170Z", "close_price": "115.43000000"}, {"begins_at": "2019-01-22T07:12:04.573Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T07:12:15.302Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T07:13:48.937Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T07:13:50.361Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T07:14:26.526Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T07:14:40.595Z", "close_price": "115.50000000"}, {"begins_at": "2019-01-22T07:15:51.775Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T07:16:05.529Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:16:14.584Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:16:42.185Z", "close_price": "115.58000000"}, {"begins_at": "2019-01-22T07:17:00.900Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:17:46.261Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:18:37.209Z", "close_price": "115.58000000"}, {"begins_at": "2019-01-22T07:18:37.344Z", "close_price": "115.58000000"}, {"begins_at": "2019-01-22T07:19:53.863Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:20:20.102Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:20:44.811Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T07:21:34.957Z", "close_price": "115.60000000"}, {"begins_at": "2019-01-22T07:21:37.591Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:21:46.304Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:21:58.687Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:22:38.795Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:22:39.990Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:22:53.500Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:23:35.218Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:23:40.471Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:24:11.218Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:24:20.644Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:24:52.261Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:24:55.958Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:25:04.348Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:26:27.437Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:26:45.571Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:27:39.639Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:27:48.920Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:28:41.321Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:28:54.699Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:28:56.633Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:29:05.829Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:29:17.119Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:29:25.642Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:29:32.494Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:29:44.135Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:30:39.728Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:31:28.520Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T07:31:34.113Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T07:31:53.660Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T07:32:01.660Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T07:32:14.840Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:32:25.738Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:32:48.513Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T07:32:54.826Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T07:33:00.378Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T07:34:04.544Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T07:34:23.183Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:34:55.666Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T07:36:30.584Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:37:30.734Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T07:38:36.791Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:38:50.590Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T07:39:01.310Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T07:39:51.333Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T07:41:01.410Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:41:05.889Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:41:12.190Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:41:28.635Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:41:35.864Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:43:13.478Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:43:22.453Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:43:25.325Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:43:56.690Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:45:10.577Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:45:29.577Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:45:59.680Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:46:00.112Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T07:46:10.437Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:46:22.410Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T07:47:51.186Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T07:49:14.252Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:49:19.324Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T07:49:24.467Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:49:29.606Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:49:52.550Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:50:06.523Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:50:22.519Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T07:51:14.628Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:51:21.819Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:51:29.447Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:51:42.606Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:52:18.445Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:52:32.590Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:53:01.116Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T07:53:09.234Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:53:17.443Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:53:58.913Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:54:17.714Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:54:31.538Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T07:54:33.194Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:55:57.846Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:56:18.100Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:58:13.684Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T07:58:50.250Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T07:58:53.597Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T07:58:57.957Z", "close_price": "115.67000000"}, {"begins_at": "2019-01-22T07:59:37.532Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T08:00:10.629Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T08:00:28.259Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T08:01:17.735Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T08:01:54.641Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T08:03:26.632Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T08:03:49.547Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T08:04:40.139Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T08:04:57.528Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T08:05:22.753Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:06:50.812Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:06:55.505Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T08:08:18.638Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:24.331Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:29.704Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:39.242Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:40.873Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:47.545Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:09:50.546Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:10:01.375Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:10:07.267Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T08:10:12.886Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T08:10:57.465Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T08:11:01.790Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:11:03.340Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:11:05.712Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:11:27.212Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:11:47.390Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:12:10.680Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T08:12:46.646Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T08:14:48.192Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:14:52.649Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T08:14:57.193Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T08:15:07.676Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T08:16:00.170Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T08:16:03.494Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T08:16:03.614Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T08:16:25.250Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T08:16:32.407Z", "close_price": "115.95000000"}, {"begins_at": "2019-01-22T08:16:45.410Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:16:52.941Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T08:17:18.415Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T08:17:21.950Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T08:18:15.862Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:19:35.775Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:19:44.726Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T08:20:02.317Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:20:20.585Z", "close_price": "116.07000000"}, {"begins_at": "2019-01-22T08:20:26.589Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:20:37.693Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:21:08.222Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T08:21:11.350Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T08:21:27.360Z", "close_price": "116.11000000"}, {"begins_at": "2019-01-22T08:21:59.226Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T08:22:03.957Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T08:22:04.281Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:22:09.540Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T08:23:03.847Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T08:23:15.950Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T08:23:52.861Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T08:24:05.690Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:24:20.586Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T08:24:23.402Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:25:04.850Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:25:53.196Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:25:56.149Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T08:25:57.646Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T08:26:46.217Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:26:51.880Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:27:21.721Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:27:42.490Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:28:28.379Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:28:38.831Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:28:48.317Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:28:51.716Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:29:15.139Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T08:29:21.368Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:29:23.156Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T08:29:52.717Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T08:30:24.851Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:30:32.842Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:31:06.706Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:31:10.602Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:31:17.678Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T08:31:59.990Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T08:32:27.987Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T08:32:37.630Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T08:32:45.491Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T08:33:06.206Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:33:13.286Z", "close_price": "116.07000000"}, {"begins_at": "2019-01-22T08:33:25.798Z", "close_price": "116.07000000"}, {"begins_at": "2019-01-22T08:33:36.150Z", "close_price": "116.13000000"}, {"begins_at": "2019-01-22T08:33:44.710Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T08:34:19.796Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T08:34:28.211Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T08:35:16.662Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T08:37:02.281Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T08:38:03.508Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:38:23.340Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:39:06.722Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:39:25.460Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:40:11.560Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T08:40:24.947Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T08:40:35.958Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:40:38.123Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T08:41:09.335Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:42:17.370Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:42:17.761Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:42:31.518Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:42:49.274Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:43:20.480Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:43:49.829Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:43:59.785Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:44:39.383Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:44:53.228Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:44:54.783Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:02.775Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:09.531Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:10.329Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:23.875Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:24.525Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:45:39.586Z", "close_price": "116.20000000"}, {"begins_at": "2019-01-22T08:45:49.796Z", "close_price": "116.29000000"}, {"begins_at": "2019-01-22T08:46:00.508Z", "close_price": "116.39000000"}, {"begins_at": "2019-01-22T08:46:06.500Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T08:46:11.975Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T08:46:18.954Z", "close_price": "116.37000000"}, {"begins_at": "2019-01-22T08:46:31.156Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T08:46:59.503Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T08:47:21.987Z", "close_price": "116.38000000"}, {"begins_at": "2019-01-22T08:47:42.282Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T08:48:15.439Z", "close_price": "116.29000000"}, {"begins_at": "2019-01-22T08:48:46.439Z", "close_price": "116.29000000"}, {"begins_at": "2019-01-22T08:49:47.384Z", "close_price": "116.24000000"}, {"begins_at": "2019-01-22T08:49:55.965Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:50:28.304Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:50:49.952Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:51:28.956Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:52:05.424Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:54:13.000Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:55:12.962Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:55:20.991Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T08:55:26.130Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:56:01.250Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:56:16.502Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T08:56:24.595Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T08:56:28.553Z", "close_price": "116.29000000"}, {"begins_at": "2019-01-22T08:56:29.468Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T08:56:59.417Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T08:57:26.793Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T08:59:03.420Z", "close_price": "116.30000000"}, {"begins_at": "2019-01-22T09:00:01.241Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T09:00:08.494Z", "close_price": "116.21000000"}, {"begins_at": "2019-01-22T09:00:57.705Z", "close_price": "116.21000000"}, {"begins_at": "2019-01-22T09:01:07.345Z", "close_price": "116.20000000"}, {"begins_at": "2019-01-22T09:01:50.905Z", "close_price": "116.21000000"}, {"begins_at": "2019-01-22T09:01:54.991Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T09:02:15.347Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:02:50.277Z", "close_price": "116.13000000"}, {"begins_at": "2019-01-22T09:02:59.420Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:03:17.786Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:03:19.200Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:03:51.420Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:04:26.125Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:04:27.395Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:05:08.946Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:05:20.621Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:05:42.566Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:06:24.817Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:07:18.181Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:07:22.886Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:07:33.796Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:07:38.767Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:08:19.780Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:09:56.272Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:10:04.395Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:10:27.367Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:10:30.154Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T09:10:34.220Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T09:10:37.511Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T09:10:42.996Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T09:10:53.834Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:11:16.704Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:11:21.178Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:11:50.607Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:12:08.345Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:12:39.961Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:13:17.205Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:13:29.194Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:13:54.171Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:14:28.648Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:16:28.310Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:16:46.646Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T09:16:55.918Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T09:18:56.424Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T09:19:28.654Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T09:19:44.110Z", "close_price": "115.91000000"}, {"begins_at": "2019-01-22T09:19:54.470Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T09:20:42.297Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T09:21:05.712Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T09:21:30.920Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T09:22:09.324Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T09:22:13.865Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T09:22:24.532Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T09:22:52.487Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T09:23:50.385Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T09:24:31.267Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T09:25:51.118Z", "close_price": "115.87000000"}, {"begins_at": "2019-01-22T09:25:52.593Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T09:26:19.326Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:27:01.778Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T09:28:01.909Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T09:28:18.379Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T09:29:24.325Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:29:26.741Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:29:37.144Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:29:51.353Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:30:09.712Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T09:30:14.227Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T09:30:17.471Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T09:30:31.455Z", "close_price": "115.95000000"}, {"begins_at": "2019-01-22T09:30:37.240Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T09:30:37.533Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T09:31:12.997Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:31:40.895Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:32:04.664Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:32:18.399Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T09:32:39.250Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T09:33:31.204Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T09:33:52.157Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T09:33:57.963Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T09:34:28.717Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:34:30.482Z", "close_price": "116.07000000"}, {"begins_at": "2019-01-22T09:34:41.621Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:34:58.333Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:36:17.231Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:36:18.358Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:36:20.617Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T09:36:57.295Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:36:58.547Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:37:03.656Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:37:14.692Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T09:37:18.480Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:38:16.766Z", "close_price": "116.23000000"}, {"begins_at": "2019-01-22T09:38:53.766Z", "close_price": "116.23000000"}, {"begins_at": "2019-01-22T09:38:57.183Z", "close_price": "116.23000000"}, {"begins_at": "2019-01-22T09:39:03.843Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:39:55.971Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:40:30.291Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:40:42.302Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:40:45.384Z", "close_price": "116.13000000"}, {"begins_at": "2019-01-22T09:41:28.292Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:42:04.105Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T09:43:01.278Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T09:43:11.372Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:43:22.279Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:43:57.869Z", "close_price": "116.13000000"}, {"begins_at": "2019-01-22T09:44:12.667Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:44:28.422Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:44:40.141Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T09:44:51.535Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T09:45:11.638Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:46:24.338Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:46:49.656Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:47:45.537Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:47:48.457Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:48:09.775Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T09:48:43.530Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T09:48:46.905Z", "close_price": "116.07000000"}, {"begins_at": "2019-01-22T09:48:54.323Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T09:49:06.369Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T09:49:14.784Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T09:49:23.697Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T09:49:24.480Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T09:49:32.509Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T09:49:34.855Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T09:49:35.242Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T09:50:11.326Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T09:50:15.276Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T09:51:11.980Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T09:51:20.676Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T09:51:34.874Z", "close_price": "115.84000000"}, {"begins_at": "2019-01-22T09:51:56.959Z", "close_price": "115.84000000"}, {"begins_at": "2019-01-22T09:53:31.798Z", "close_price": "115.84000000"}, {"begins_at": "2019-01-22T09:53:51.280Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T09:54:41.236Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T09:55:18.300Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T09:55:20.122Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T09:55:41.409Z", "close_price": "115.78000000"}, {"begins_at": "2019-01-22T09:56:01.977Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:24.574Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:25.901Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:47.127Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:53.499Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:54.448Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:56:56.122Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:57:15.620Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:57:39.356Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:57:48.385Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T09:58:01.325Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T09:58:08.917Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T09:59:21.536Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T09:59:23.453Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T09:59:24.783Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T09:59:29.469Z", "close_price": "115.69000000"}, {"begins_at": "2019-01-22T09:59:31.170Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T09:59:31.287Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T10:00:02.584Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T10:00:07.656Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T10:00:12.732Z", "close_price": "115.61000000"}, {"begins_at": "2019-01-22T10:00:23.123Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T10:00:31.762Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T10:00:32.203Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T10:00:35.379Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T10:00:36.647Z", "close_price": "115.44000000"}, {"begins_at": "2019-01-22T10:00:39.848Z", "close_price": "115.44000000"}, {"begins_at": "2019-01-22T10:00:44.953Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T10:00:47.295Z", "close_price": "115.35000000"}, {"begins_at": "2019-01-22T10:00:53.518Z", "close_price": "115.20000000"}, {"begins_at": "2019-01-22T10:00:55.843Z", "close_price": "115.17000000"}, {"begins_at": "2019-01-22T10:00:56.175Z", "close_price": "115.16000000"}, {"begins_at": "2019-01-22T10:00:59.523Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T10:01:00.609Z", "close_price": "115.03000000"}, {"begins_at": "2019-01-22T10:01:03.574Z", "close_price": "115.02000000"}, {"begins_at": "2019-01-22T10:01:04.509Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T10:01:08.806Z", "close_price": "115.02000000"}, {"begins_at": "2019-01-22T10:01:11.185Z", "close_price": "115.09000000"}, {"begins_at": "2019-01-22T10:01:12.694Z", "close_price": "115.08000000"}, {"begins_at": "2019-01-22T10:01:21.643Z", "close_price": "115.13000000"}, {"begins_at": "2019-01-22T10:01:31.104Z", "close_price": "115.25000000"}, {"begins_at": "2019-01-22T10:01:39.144Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:01:44.867Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:00.894Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:04.261Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:07.296Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:21.775Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:30.328Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T10:02:34.588Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T10:02:37.111Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T10:02:37.170Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T10:02:39.124Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T10:03:04.692Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T10:03:10.215Z", "close_price": "115.41000000"}, {"begins_at": "2019-01-22T10:03:17.700Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T10:03:50.352Z", "close_price": "115.37000000"}, {"begins_at": "2019-01-22T10:03:55.750Z", "close_price": "115.38000000"}, {"begins_at": "2019-01-22T10:03:59.138Z", "close_price": "115.42000000"}, {"begins_at": "2019-01-22T10:03:59.966Z", "close_price": "115.43000000"}, {"begins_at": "2019-01-22T10:04:10.972Z", "close_price": "115.45000000"}, {"begins_at": "2019-01-22T10:04:17.696Z", "close_price": "115.56000000"}, {"begins_at": "2019-01-22T10:04:17.958Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T10:04:20.928Z", "close_price": "115.66000000"}, {"begins_at": "2019-01-22T10:04:23.604Z", "close_price": "115.81000000"}, {"begins_at": "2019-01-22T10:04:24.621Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T10:04:28.974Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:04:29.456Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T10:04:37.831Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T10:04:38.852Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T10:04:40.613Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T10:04:43.922Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T10:04:44.620Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:04:47.160Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T10:04:50.617Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:04:51.420Z", "close_price": "116.21000000"}, {"begins_at": "2019-01-22T10:04:55.577Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T10:04:59.343Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T10:05:00.208Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:05:02.304Z", "close_price": "115.94000000"}, {"begins_at": "2019-01-22T10:05:09.843Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T10:05:12.595Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:05:15.227Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:05:18.725Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T10:05:22.458Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T10:05:40.215Z", "close_price": "115.90000000"}, {"begins_at": "2019-01-22T10:05:51.808Z", "close_price": "115.95000000"}, {"begins_at": "2019-01-22T10:05:55.679Z", "close_price": "116.02000000"}, {"begins_at": "2019-01-22T10:06:02.245Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T10:06:30.590Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T10:06:33.972Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:06:34.112Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:07:12.340Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T10:07:35.262Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:07:37.460Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:07:48.345Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:08:12.422Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:08:29.344Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:08:39.116Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:08:43.482Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:08:54.109Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:09:18.328Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T10:09:33.594Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:09:34.207Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:09:57.989Z", "close_price": "116.04000000"}, {"begins_at": "2019-01-22T10:11:08.873Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T10:11:29.959Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:11:31.704Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:11:41.488Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T10:11:51.451Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T10:11:59.437Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T10:12:02.536Z", "close_price": "116.24000000"}, {"begins_at": "2019-01-22T10:12:09.282Z", "close_price": "116.31000000"}, {"begins_at": "2019-01-22T10:12:15.717Z", "close_price": "116.22000000"}, {"begins_at": "2019-01-22T10:12:19.419Z", "close_price": "116.06000000"}, {"begins_at": "2019-01-22T10:12:20.790Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T10:12:25.651Z", "close_price": "116.01000000"}, {"begins_at": "2019-01-22T10:12:30.183Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:12:35.221Z", "close_price": "116.17000000"}, {"begins_at": "2019-01-22T10:12:40.803Z", "close_price": "116.08000000"}, {"begins_at": "2019-01-22T10:13:53.335Z", "close_price": "116.05000000"}, {"begins_at": "2019-01-22T10:13:57.913Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:14:03.425Z", "close_price": "116.00000000"}, {"begins_at": "2019-01-22T10:14:56.745Z", "close_price": "116.11000000"}, {"begins_at": "2019-01-22T10:15:05.170Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:15:06.632Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:15:15.884Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T10:15:16.100Z", "close_price": "116.20000000"}, {"begins_at": "2019-01-22T10:15:22.480Z", "close_price": "116.21000000"}, {"begins_at": "2019-01-22T10:15:24.993Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T10:15:55.407Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T10:16:07.771Z", "close_price": "116.11000000"}, {"begins_at": "2019-01-22T10:16:45.300Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T10:16:57.144Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T10:17:04.843Z", "close_price": "116.16000000"}, {"begins_at": "2019-01-22T10:17:32.238Z", "close_price": "116.20000000"}, {"begins_at": "2019-01-22T10:17:42.260Z", "close_price": "116.18000000"}, {"begins_at": "2019-01-22T10:18:17.832Z", "close_price": "116.19000000"}, {"begins_at": "2019-01-22T10:18:24.260Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:19:10.589Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:19:18.629Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:19:45.116Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:19:50.606Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:20:18.412Z", "close_price": "116.15000000"}, {"begins_at": "2019-01-22T10:20:40.589Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:20:48.817Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T10:21:15.392Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T10:21:18.507Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T10:22:12.898Z", "close_price": "116.12000000"}, {"begins_at": "2019-01-22T10:23:02.150Z", "close_price": "116.23000000"}, {"begins_at": "2019-01-22T10:23:12.633Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:25:09.986Z", "close_price": "116.14000000"}, {"begins_at": "2019-01-22T10:25:24.251Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:25:42.926Z", "close_price": "116.09000000"}, {"begins_at": "2019-01-22T10:25:59.492Z", "close_price": "116.10000000"}, {"begins_at": "2019-01-22T10:27:26.747Z", "close_price": "116.03000000"}, {"begins_at": "2019-01-22T10:27:35.799Z", "close_price": "115.93000000"}, {"begins_at": "2019-01-22T10:29:02.708Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T10:29:11.146Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T10:30:23.188Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T10:30:28.280Z", "close_price": "115.92000000"}, {"begins_at": "2019-01-22T10:30:46.957Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:30:57.273Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:31:34.858Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:32:33.296Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:32:41.300Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:33:18.320Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:34:14.280Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:34:19.976Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:34:51.862Z", "close_price": "115.98000000"}, {"begins_at": "2019-01-22T10:35:05.505Z", "close_price": "115.99000000"}, {"begins_at": "2019-01-22T10:35:09.333Z", "close_price": "115.97000000"}, {"begins_at": "2019-01-22T10:36:02.383Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T10:36:32.366Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T10:37:03.628Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T10:37:20.590Z", "close_price": "115.96000000"}, {"begins_at": "2019-01-22T10:37:39.519Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T10:37:47.405Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T10:37:51.123Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:38:20.828Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T10:38:21.351Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:38:46.452Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T10:38:58.886Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T10:39:21.641Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T10:39:40.467Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T10:39:44.335Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T10:40:35.290Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:40:42.843Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:41:37.621Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T10:41:54.452Z", "close_price": "115.70000000"}, {"begins_at": "2019-01-22T10:42:06.744Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T10:43:14.609Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T10:44:04.663Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T10:44:40.783Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:45:32.952Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:45:36.120Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:46:26.250Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T10:46:38.374Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T10:49:33.845Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:50:01.412Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:50:18.428Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:50:45.690Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:50:51.916Z", "close_price": "115.79000000"}, {"begins_at": "2019-01-22T10:51:09.626Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:51:27.375Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T10:51:48.674Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T10:52:19.984Z", "close_price": "115.75000000"}, {"begins_at": "2019-01-22T10:53:29.738Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T10:54:25.642Z", "close_price": "115.74000000"}, {"begins_at": "2019-01-22T10:55:22.793Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T10:55:49.397Z", "close_price": "115.65000000"}, {"begins_at": "2019-01-22T10:56:01.888Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T10:57:24.864Z", "close_price": "115.64000000"}, {"begins_at": "2019-01-22T10:57:27.481Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T10:57:32.136Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T10:57:34.151Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T10:57:50.138Z", "close_price": "115.48000000"}, {"begins_at": "2019-01-22T10:58:08.130Z", "close_price": "115.58000000"}, {"begins_at": "2019-01-22T10:58:16.524Z", "close_price": "115.68000000"}, {"begins_at": "2019-01-22T10:59:30.447Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T10:59:50.868Z", "close_price": "115.66000000"}, {"begins_at": "2019-01-22T11:01:01.621Z", "close_price": "115.65000000"}, {"begins_at": "2019-01-22T11:01:35.461Z", "close_price": "115.66000000"}, {"begins_at": "2019-01-22T11:02:14.256Z", "close_price": "115.72000000"}, {"begins_at": "2019-01-22T11:02:24.856Z", "close_price": "115.73000000"}, {"begins_at": "2019-01-22T11:03:41.625Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T11:03:46.200Z", "close_price": "115.71000000"}, {"begins_at": "2019-01-22T11:04:01.947Z", "close_price": "115.76000000"}, {"begins_at": "2019-01-22T11:04:05.551Z", "close_price": "115.80000000"}, {"begins_at": "2019-01-22T11:04:08.749Z", "close_price": "115.89000000"}, {"begins_at": "2019-01-22T11:04:19.233Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T11:04:28.719Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T11:04:30.139Z", "close_price": "115.85000000"}, {"begins_at": "2019-01-22T11:04:49.416Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T11:04:59.870Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T11:06:06.954Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T11:07:44.898Z", "close_price": "115.86000000"}, {"begins_at": "2019-01-22T11:07:49.807Z", "close_price": "115.95000000"}, {"begins_at": "2019-01-22T11:08:13.233Z", "close_price": "115.88000000"}, {"begins_at": "2019-01-22T11:08:14.822Z", "close_price": "115.82000000"}, {"begins_at": "2019-01-22T11:08:16.823Z", "close_price": "115.77000000"}, {"begins_at": "2019-01-22T11:08:17.916Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T11:08:24.643Z", "close_price": "115.46000000"}, {"begins_at": "2019-01-22T11:08:29.240Z", "close_price": "115.49000000"}, {"begins_at": "2019-01-22T11:08:33.784Z", "close_price": "115.66000000"}, {"begins_at": "2019-01-22T11:08:38.870Z", "close_price": "115.62000000"}, {"begins_at": "2019-01-22T11:08:41.198Z", "close_price": "115.48000000"}, {"begins_at": "2019-01-22T11:08:42.650Z", "close_price": "115.56000000"}, {"begins_at": "2019-01-22T11:08:43.209Z", "close_price": "115.63000000"}, {"begins_at": "2019-01-22T11:08:46.368Z", "close_price": "115.59000000"}, {"begins_at": "2019-01-22T11:10:59.550Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T11:11:01.900Z", "close_price": "115.57000000"}, {"begins_at": "2019-01-22T11:11:02.822Z", "close_price": "115.54000000"}, {"begins_at": "2019-01-22T11:11:07.126Z", "close_price": "115.54000000"}, {"begins_at": "2019-01-22T11:11:42.641Z", "close_price": "115.47000000"}, {"begins_at": "2019-01-22T11:11:46.832Z", "close_price": "115.47000000"}, {"begins_at": "2019-01-22T11:11:59.903Z", "close_price": "115.47000000"}, {"begins_at": "2019-01-22T11:12:03.457Z", "close_price": "115.46000000"}, {"begins_at": "2019-01-22T11:12:08.500Z", "close_price": "115.35000000"}, {"begins_at": "2019-01-22T11:12:11.219Z", "close_price": "115.27000000"}, {"begins_at": "2019-01-22T11:13:10.988Z", "close_price": "115.33000000"}, {"begins_at": "2019-01-22T11:13:16.125Z", "close_price": "115.30000000"}, {"begins_at": "2019-01-22T11:13:26.382Z", "close_price": "115.27000000"}, {"begins_at": "2019-01-22T11:13:30.654Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T11:13:32.375Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T11:13:51.833Z", "close_price": "115.24000000"}, {"begins_at": "2019-01-22T11:13:55.242Z", "close_price": "115.22000000"}, {"begins_at": "2019-01-22T11:14:06.902Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:14:15.112Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:14:18.102Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:14:32.113Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:14:39.111Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:14:41.880Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:15:17.348Z", "close_price": "115.16000000"}, {"begins_at": "2019-01-22T11:15:27.882Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:15:33.850Z", "close_price": "115.10000000"}, {"begins_at": "2019-01-22T11:15:59.703Z", "close_price": "115.10000000"}, {"begins_at": "2019-01-22T11:16:05.988Z", "close_price": "115.06000000"}, {"begins_at": "2019-01-22T11:16:13.584Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:16:19.136Z", "close_price": "115.06000000"}, {"begins_at": "2019-01-22T11:16:23.313Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:16:30.834Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:16:32.610Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:16:42.800Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:16:48.816Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:16:51.203Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:16:51.443Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:17:07.670Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:17:13.690Z", "close_price": "114.95000000"}, {"begins_at": "2019-01-22T11:17:15.664Z", "close_price": "114.99000000"}, {"begins_at": "2019-01-22T11:17:32.317Z", "close_price": "114.99000000"}, {"begins_at": "2019-01-22T11:17:43.538Z", "close_price": "114.98000000"}, {"begins_at": "2019-01-22T11:17:53.445Z", "close_price": "114.98000000"}, {"begins_at": "2019-01-22T11:17:54.327Z", "close_price": "114.97000000"}, {"begins_at": "2019-01-22T11:18:10.668Z", "close_price": "114.98000000"}, {"begins_at": "2019-01-22T11:18:15.722Z", "close_price": "114.97000000"}, {"begins_at": "2019-01-22T11:18:18.916Z", "close_price": "114.96000000"}, {"begins_at": "2019-01-22T11:18:19.475Z", "close_price": "114.96000000"}, {"begins_at": "2019-01-22T11:18:23.338Z", "close_price": "114.95000000"}, {"begins_at": "2019-01-22T11:18:26.658Z", "close_price": "114.95000000"}, {"begins_at": "2019-01-22T11:18:31.471Z", "close_price": "114.95000000"}, {"begins_at": "2019-01-22T11:18:37.693Z", "close_price": "114.96000000"}, {"begins_at": "2019-01-22T11:18:41.711Z", "close_price": "115.02000000"}, {"begins_at": "2019-01-22T11:18:45.398Z", "close_price": "115.03000000"}, {"begins_at": "2019-01-22T11:18:46.350Z", "close_price": "115.09000000"}, {"begins_at": "2019-01-22T11:19:02.342Z", "close_price": "115.12000000"}, {"begins_at": "2019-01-22T11:19:14.295Z", "close_price": "115.12000000"}, {"begins_at": "2019-01-22T11:19:49.232Z", "close_price": "115.15000000"}, {"begins_at": "2019-01-22T11:19:51.238Z", "close_price": "115.16000000"}, {"begins_at": "2019-01-22T11:19:55.364Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:20:47.204Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:21:40.657Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:22:49.526Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:23:07.679Z", "close_price": "115.12000000"}, {"begins_at": "2019-01-22T11:23:09.935Z", "close_price": "115.17000000"}, {"begins_at": "2019-01-22T11:23:16.950Z", "close_price": "115.11000000"}, {"begins_at": "2019-01-22T11:23:19.271Z", "close_price": "115.13000000"}, {"begins_at": "2019-01-22T11:23:19.331Z", "close_price": "115.13000000"}, {"begins_at": "2019-01-22T11:23:24.181Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:23:45.957Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:23:49.237Z", "close_price": "115.24000000"}, {"begins_at": "2019-01-22T11:23:50.577Z", "close_price": "115.26000000"}, {"begins_at": "2019-01-22T11:23:55.834Z", "close_price": "115.18000000"}, {"begins_at": "2019-01-22T11:24:02.362Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:24:44.987Z", "close_price": "115.20000000"}, {"begins_at": "2019-01-22T11:24:56.916Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:25:22.412Z", "close_price": "115.19000000"}, {"begins_at": "2019-01-22T11:25:55.502Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:26:02.481Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:26:14.642Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:26:59.198Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:27:17.205Z", "close_price": "114.99000000"}, {"begins_at": "2019-01-22T11:27:25.536Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:28:17.608Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:28:33.504Z", "close_price": "115.05000000"}, {"begins_at": "2019-01-22T11:28:36.826Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:29:15.863Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:30:29.173Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:30:43.861Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:31:03.894Z", "close_price": "115.13000000"}, {"begins_at": "2019-01-22T11:31:18.557Z", "close_price": "115.12000000"}, {"begins_at": "2019-01-22T11:31:29.130Z", "close_price": "115.00000000"}, {"begins_at": "2019-01-22T11:31:33.465Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:31:50.373Z", "close_price": "115.01000000"}, {"begins_at": "2019-01-22T11:32:24.862Z", "close_price": "115.02000000"}, {"begins_at": "2019-01-22T11:32:40.902Z", "close_price": "115.03000000"}, {"begins_at": "2019-01-22T11:33:00.393Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:33:21.593Z", "close_price": "115.07000000"}, {"begins_at": "2019-01-22T11:33:56.629Z", "close_price": "115.14000000"}, {"begins_at": "2019-01-22T11:34:15.316Z", "close_price": "115.13000000"}]
	
	#########################
	######### TO DO #########
	#########################
	# LOG DATA BY THE MINUTE

	# MOVING THRESHHOLDS
	## DISCERN BTWN WHOLE DATASET AND ENDING SET FROM DATASET TO DETERMINE THRESHOLDS
	
	# AGGREGATE THRESHOLDS
	## COMBINE OLDER DATASETS WITH NEWER

	sma_appended 	= False
	sma_total 		= 0
	sma_type 		= []

	while True:
		eth_log 	= public_client.get_product_ticker(product_id='ETH-USD')
		new_time 	= eth_log["time"]
		open_csv 	= open("test_mongo.csv", "a")
		write_csv 	= csv.writer(open_csv)
		sma_counter 	= 0

		if start_log == False:
			a.append({"begins_at":eth_log["time"], "close_price":eth_log["price"], "sma_"+str(sma_a):eth_log["price"], "sma_"+str(sma_b):eth_log["price"]})
			start_log = True
			print(a)

			for d in a:
				if sma_appended == False:
					for e in d:
						print(e)
						if "sma_" in str(e):
							sma_counter+=1
							sma_inter = int(e.replace("sma_", ""))
							sma_type.append(sma_inter)
					sma_total = sma_counter
					sma_type.sort()
					sma_appended = True
				break
		# 	try:
		# 		a = get_sma(a, 1)
		# 	except:
		# 		pass
		# 	try:
		# 		a = get_sma(a, 3)
		# 	except:
		# 		pass
		# 	write_csv.writerow([new_time, eth_log["price"]])
		# 	open_csv.close()
		# try:
		if str(a[len(a)-1]["begins_at"]) != str(new_time):
			print("-----------------------------")
			print("-----------------------------")
			a.append({"begins_at":eth_log["time"], "close_price":eth_log["price"]})
			a = get_sma(a, sma_a)
			a = get_sma(a, sma_b)
			# backtest(a[len(a)-1])
			print("---")
			print("---")
			# a[len(a)-1] = get_sma(a, 1)
			print(a)
			# print("---")
			# print("---")
			# print(eth_log)
			# print("---")
			# print("---")
			# print(a[len(a)-1])
			# print("---")
			# print("---")
			# print(len(a))
			# print("---")
			# print("---")
			write_csv.writerow([new_time, eth_log["price"]])
			backtest(a)
		# except:
		# 	pass
		# if str(e) != str(c):
			# c = str(e)
			# print("asdf")
		# b = convert_time(a["time"])
		# b = get_stats()
		open_csv.close()
		time.sleep(0.1)

#################################################
#################################################

def log_seconds():
	a = open("live_log_seconds.csv", "a+")
	b = csv.writer(a)
	while True:
		c = public_client.get_product_ticker(product_id='ETH-USD')
		print(c)
		b.writerow([c["time"], c["price"]])
		time.sleep(1)

#################################################
#################################################

log_seconds()
# testing()
# test_ws()
# wtf()
# test_mongo()

#################################################
#################################################























	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now() + timedelta(days=1))
	# print(datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=20))
	# print(datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=20))
	# print(datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=20))
	# print(datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=20))
	# print(timedelta(0, 125, 7494300, 125, 749430))
	# print(timedelta(0, 125, 7494300, 125, 749430))
	# print(timedelta(0, 125, 7494300, 125, 749430))
	# print(timedelta(0, 125, 7494300, 125, 749430))













