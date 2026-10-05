from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# test = cg.get_price(ids='bitcoin', vs_currencies='usd')
# print(test)

# asdf = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
# print(asdf)

# a = cg.get_coins_list()
# print(a)
# print(len(a))

# b = cg.get_search_trending()

top_cap_change = {"symbol":"", "cap_change":0}
low_cap_change = {"symbol":"", "cap_change":0}


def test():
	b = cg.get_coins_markets(vs_currency="usd")
	for a in b:	
		for c in a:
			print(c)
		print(a)
		print(a["name"])
		print(a["symbol"])
		print("PRICE CHANGE 24H               : " + str(a["price_change_24h"]))
		print("PRICE CHANGE 24H %             : " + str(a["price_change_percentage_24h"])+" %")
		print("TOTAL VOUME                    : " + str(a["total_volume"]))
		print("MARKET CAP                     : " + str(a["market_cap"]))
		print("TOTAL MARKET CAP CHANGE 24H    : " + str(a["market_cap_change_24h"]))
		print("TOTAL MARKET CAP CHANGE 24H %  : " + str(a["market_cap_change_percentage_24h"])+" %")
		print("-"*50)
		if a["market_cap_change_24h"] > top_cap_change["cap_change"]:
			top_cap_change["symbol"] 						= a["symbol"]
			top_cap_change["cap_change"] 					= a["market_cap_change_24h"]
			top_cap_change["cap_change_percentage"] 		= a["market_cap_change_percentage_24h"]
			top_cap_change["total_volume"] 					= a["total_volume"]
			top_cap_change["price_change_percentage_24h"] 	= a["price_change_percentage_24h"]
		if a["market_cap_change_24h"] < low_cap_change["cap_change"] and a["symbol"] != "usdc" and a["symbol"] != "busd" and a["symbol"] != "tusd":
			low_cap_change["symbol"] 						= a["symbol"]
			low_cap_change["cap_change"] 					= a["market_cap_change_24h"]
			low_cap_change["cap_change_percentage"] 		= a["market_cap_change_percentage_24h"]
			low_cap_change["total_volume"] 					= a["total_volume"]
			low_cap_change["price_change_percentage_24h"] 	= a["price_change_percentage_24h"]
		print(top_cap_change)
		print(low_cap_change)
		# print(a["item"]["name"])

def test_hist():
	a = cg.get_coin_market_chart_range_by_id(id="bitcoin", vs_currency="usd", from_timestamp="2020-11-24T11:20:14+00:00", to_timestamp="2020-11-25T11:20:14+00:00")
	# b = cg.get_coins_markets(vs_currency="usd")
	print(a)

test_hist()