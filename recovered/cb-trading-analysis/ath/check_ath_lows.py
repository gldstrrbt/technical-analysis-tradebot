import requests, json, os, csv, time, datetime


def read_csv(filename):
	a = open(filename+".csv", "r")
	b = csv.reader(a)
	return [c for c in b]


def write_csv(filename):
	a = open(filename+".csv", "w", errors="ignore", newline="")
	return csv.writer(a)


def get_list():
	a = requests.get("https://api.coingecko.com/api/v3/coins/list")
	b = a.content
	return json.loads(b)


def get_coin_details():
	a = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=alpha-finance&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h")
	b = a.content
	return json.loads(b)


def get_coin(id):
	# a = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+id+"&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=24h")
	time.sleep(0.5)
	a = requests.get("https://api.coingecko.com/api/v3/coins/"+id)
	b = a.content
	if "Throttled" in str(b):
		print(id)
		print(b)
		print("*"*20)
		return None
	else:
		return json.loads(b)


def write_list(dataset, csv_file):
	csv_file.writerow(["id", "symbol", "name"])
	for a in dataset:
		csv_file.writerow([a["id"], a["symbol"], a["name"]])


def write_ath_list(csv_read, csv_write):
	csv_write.writerow(["market_cap_rank", "id", "symbol", "name", "current_price", "price_change_percentage_24h_in_currency", "market_cap", "market_cap_change_24h_in_currency", "volume", "total_volume", "ath", "ath_change_percentage", "ath_date", "market_cap_change_24h", "circulating_supply", "total_supply"])
	for z, a in enumerate(csv_read):
		if z != 0:
			# try:
			b = get_coin(a[0])
			if b != None and b["market_data"]["market_cap_rank"] != "" and b["market_data"]["market_cap_rank"] != None and int(b["market_data"]["market_cap_rank"]) < 1000:	
				csv_write.writerow([b["market_data"]["market_cap_rank"], b["id"], b["symbol"], b["name"], b["market_data"]["current_price"]["usd"], b["market_data"]["price_change_percentage_24h_in_currency"]["usd"], b["market_data"]["market_cap"]["usd"], b["market_data"]["market_cap_change_24h_in_currency"]["usd"], b["market_data"]["total_volume"]["usd"], b["market_data"]["total_volume"]["usd"], b["market_data"]["ath"]["usd"], b["market_data"]["ath_change_percentage"]["usd"], b["market_data"]["ath_date"]["usd"], b["market_data"]["market_cap_change_24h"], b["market_data"]["circulating_supply"], b["market_data"]["total_supply"]])
				print(z)
				print(a[0])
				print("^^^^^^^^^^^^^^^^^^^pass")
				time.sleep(0.2)
			# except:
			# 	pass


def get_top_coins():
	page = 1
	gathered_list = []
	while page < 8:
		a = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page="+str(page))
		b = a.content
		c = json.loads(b)
		gathered_list.append(c)
		page+=1 
		time.sleep(0.5)
	return gathered_list


def write_detailed_list(csv_read, csv_write):
	csv_write.writerow(["market_cap_rank", "id", "symbol", "name", "ath_change_percentage", "ath_date", "ath", "price_change_percentage_24h", "current_price", "price_change_24h", "market_cap", "total_volume", "total_volume", "market_cap_change_24h", "circulating_supply", "total_supply"])
	# print("len(csv_read)", len(csv_read))
	for z, y in enumerate(csv_read):
		for a in y:
			csv_write.writerow([a["market_cap_rank"], a["id"], a["symbol"], a["name"], a["ath_change_percentage"], a["ath_date"], a["ath"], a["price_change_percentage_24h"], a["current_price"], a["price_change_24h"], a["market_cap"], a["total_volume"], a["total_volume"], a["market_cap_change_24h"], a["circulating_supply"], a["total_supply"]])
		# print(a)
		# print("*"*50)


# def init():
# 	# a = get_list()
# 	# b = write_csv("coinlist")
# 	# write_list(a, b)
# 	####################################
# 	filename = datetime.datetime.now()
# 	filename = str(filename).replace(" ", "_").replace(":", "-").replace(".", "_")
# 	print()
# 	print("Date Stamp: ")
# 	print(str(filename))
# 	c = write_csv(filename)
# 	# c = write_csv("crypto_ath_tracker_marketcap_top_500")
# 	# d = read_csv("coinlist")
# 	# write_ath_list(d, c)
# 	####################################
# 	e = get_top_coins()
# 	f = write_detailed_list(e, c)
# 	print()
# 	print("CSV File Exported: ")
# 	print(filename + ".csv")
# 	print("#"*50)

# init()

def write_dub(dataset):
	a = write_csv("processed_test_double_aug_21")
	a.writerow(["market_cap_rank", "id", "symbol", "name", "ath_date", "potential_new_multiples", "potential_new_high", "ath_price", "current_price" ])
	for c, b in enumerate(dataset):
		if c != 0:	
			potential_new_high 		= float(b[6])*2
			potential_new_multiples = potential_new_high/float(b[8])
			a.writerow([b[0], b[1], b[2], b[3], b[5], potential_new_multiples, potential_new_high, b[6], b[8]])


def init_dub():
	a = read_csv("test_double_aug_21")
	write_dub(a)
	# print(a[0][6])
	# print(a[0][8])


init_dub()