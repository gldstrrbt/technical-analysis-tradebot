import os, json
# https://api.earningscalendar.net/
# https://api.earningscalendar.net/?date=20170330
# https://twitter.com/cnbcfastmoney?lang=en
# https://simfin.com/data/access/api
yield_dataset = ["14", "15", "16", "17", "18"]

for z in yield_dataset:
	data_file = open("yield_data/yield_" + z + ".json", "r+")
	data_file = json.load(data_file)
	new_arr = []
	for a in data_file:
		new_arr.append({"date": a["Date"], "1_month":a["1 mo"], "3_month":a["3 mo"], "6_month":a["6 mo"], "1_year":a["1 yr"], "2_year":a["2 yr"], "3_year":a["3 yr"], "5_year":a["5 yr"], "7_year":a["7 yr"], "10_year":a["10 yr"], "20_year":a["20 yr"], "30_year":a["30 yr"]})
		# for b in a:
			# print(b)
		# for b in a:
		# 	print(a[b])

	for a in new_arr:
		if a["1_month"] > a["3_month"]:
			print("REVERSAL: 1 month & 3 month difference")
			print(a["date"])	
			print("1 MONTH: " + str(a["1_month"]))	
			print("3 MONTH: " + str(a["3_month"]))
			print(a["3_month"]-a["1_month"])
			print(a["3_month"])
			print("-"*50)		
		# if a["3_month"]-a["1_month"] < 0.10:
		if a["3_month"]-a["1_month"] < 0.0:
			print("TOO CLOSE: 1 month & 3 month difference")
			print(a["date"])
			print("1 MONTH: " + str(a["1_month"]))	
			print("3 MONTH: " + str(a["3_month"]))	
			print(a["3_month"]-a["1_month"])
			print("-"*50)

		if a["3_month"] > a["6_month"]:
			print("REVERSAL: 3 month & 6 month difference")
			print(a["date"])		
			print("3 MONTH: " + str(a["3_month"]))	
			print("6 MONTH: " + str(a["6_month"]))
			print(a["6_month"]-a["3_month"])
			print(a["6_month"])
			print("-"*50)		
		# if a["6_month"]-a["3_month"] < 0.10:
		if a["6_month"]-a["3_month"] < 0.0:
			print("TOO CLOSE: 3 month & 6 month difference")
			print(a["date"])
			print("3 MONTH: " + str(a["3_month"]))	
			print("6 MONTH: " + str(a["6_month"]))
			print(a["6_month"]-a["3_month"])
			print("-"*50)	