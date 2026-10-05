import requests, csv, json, os
from datetime import datetime
from datetime import timedelta


# AAVE is actually logged from the daily scale
##############################
### INCOMPLETE TIME FRAMES ###
##############################
# AKRO
# ALPHA
# BZRX
# AST (IN BTC)

	
	# "akro":[
	# 	{
	# 		"date":"11/09/2020",
	# 		"close_val":0.010688
	# 	},
	# 	{
	# 		"date":"11/21/2020",
	# 		"close_val":0.010124
	# 	}
	# ],
	# "alpha":[
	# 	{
	# 		"date":"10/08/2020",
	# 		"close_val":0.05799
	# 	},
	# 	{
	# 		"date":"11/05/2020",
	# 		"close_val":0.04164
	# 	}
	# ],

##############################
######### WATCH LIST #########
##############################
# ALGO
# COCOS

date_data = {
	"theta":[
		{
			"date":"05/25/2020",
			"close_val":0.38112
		},
		{
			"date":"08/01/2020",
			"close_val":0.3469
		},
		{
			"date":"08/29/2020",
			"close_val":0.49297
		},
		{
			"date":"10/08/2020",
			"close_val":0.73222
		}
	],
	"aave":[
		{
			"date":"10/14/2020",
			"close_val":45.605
		},
		{
			"date":"11/05/2020",
			"close_val":35.372
		},
		{
			"date":"11/10/2020",
			"close_val":61.014
		},
		{
			"date":"11/20/2020",
			"close_val":72.583
		}
	],
	"ada":[
		{
			"date":"07/28/2020",
			"close_val":0.14466
		},
		{
			"date":"11/13/2020",
			"close_val":0.10669
		}
	],
	"aion":[
		{
			"date":"08/21/2020",
			"close_val":0.1417
		},
		{
			"date":"11/21/2020",
			"close_val":0.0725
		}
	],
	"algo":[
		{
			"date":"08/13/2020",
			"close_val":0.6493
		},
		{
			"date":"11/21/2020",
			"close_val":0.3191
		}
	],
	"ankr":[
		{
			"date":"08/09/2020",
			"close_val":0.014141
		},
		{
			"date":"11/17/2020",
			"close_val":0.009102
		}
	],
	"ardr":[
		{
			"date":"08/25/2020",
			"close_val":0.08186
		},
		{
			"date":"11/17/2020",
			"close_val":0.05530
		}
	],
	"arpa":[
		{
			"date":"08/13/2020",
			"close_val":0.04458
		},
		{
			"date":"11/21/2020",
			"close_val":0.02215
		}
	],
	"ast":[
		{
			"date":"08/13/2020",
			"close_val":0.00001850
		},
		{
			"date":"11/21/2020",
			"close_val":0.00000526
		}
	],
	"bat":[
		{
			"date":"08/17/2020",
			"close_val":0.3616
		},
		{
			"date":"11/17/2020",
			"close_val":0.2157
		}
	],
	"bch":[
		{
			"date":"07/28/2020",
			"close_val":302.51
		},
		{
			"date":"11/13/2020",
			"close_val":252.66
		}
	],
	"btc":[
		{
			"date":"07/28/2020",
			"close_val":11345.11
		},
		{
			"date":"10/08/2020",
			"close_val":11250.67
		}
	],
	"bts":[
		{
			"date":"08/29/2020",
			"close_val":0.04201
		},
		{
			"date":"11/21/2020",
			"close_val":0.02495
		}
	],
	"btt":[
		{
			"date":"08/13/2020",
			"close_val":0.0004993
		},
		{
			"date":"11/21/2020",
			"close_val":0.0003270
		}
	],
	"bzrx":[
		{
			"date":"08/29/2020",
			"close_val":1.2856
		},
		{
			"date":"11/21/2020",
			"close_val":0.3490
		}
	],
	"cgld":[
		{
			"date":"08/29/2020",
			"close_val":3.9273
		},
		{
			"date":"11/21/2020",
			"close_val":1.8148
		}
	],
	"cocos":[
		{
			"date":"08/05/2020",
			"close_val":0.000534
		},
		{
			"date":"11/17/2020",
			"close_val":0.000287
		}
	],
	"coti":[
		{
			"date":"08/29/2020",
			"close_val":0.08523
		},
		{
			"date":"11/21/2020",
			"close_val":0.04521
		}
	],
	"crv":[
		{
			"date":"08/13/2020",
			"close_val":8.290
		},
		{
			"date":"11/21/2020",
			"close_val":0.852
		}
	],
	"ctxc":[
		{
			"date":"08/25/2020",
			"close_val":0.1607
		},
		{
			"date":"11/21/2020",
			"close_val":0.0851
		}
	],
	"cvc":[
		{
			"date":"08/17/2020",
			"close_val":0.04636
		},
		{
			"date":"11/01/2020",
			"close_val":0.03085
		},
		{
			"date":"11/09/2020",
			"close_val":0.12325
		}
	],
	"dash":[
		{
			"date":"08/05/2020",
			"close_val":96.20
		},
		{
			"date":"11/13/2020",
			"close_val":79.60
		}
	],
	"dent":[
		{
			"date":"08/05/2020",
			"close_val":0.0003146
		},
		{
			"date":"11/21/2020",
			"close_val":0.0001942
		}
	],
	"doge":[
		{
			"date":"07/08/2020",
			"close_val":0.0042145
		},
		{
			"date":"11/13/2020",
			"close_val":0.0028771
		}
	],
	"dusk":[
		{
			"date":"08/13/2020",
			"close_val":0.1092
		},
		{
			"date":"11/21/2020",
			"close_val":0.0468
		}
	],
	"eos":[
		{
			"date":"08/17/2020",
			"close_val":3.5151
		},
		{
			"date":"11/17/2020",
			"close_val":2.9131
		}
	],
	"etc":[
		{
			"date":"08/01/2020",
			"close_val":7.4669
		},
		{
			"date":"11/17/2020",
			"close_val":6.0448
		}
	],
	"eth":[
		{
			"date":"08/13/2020",
			"close_val":428.47
		},
		{
			"date":"10/12/2020",
			"close_val":375.23
		}
	],
	"fet":[
		{
			"date":"08/17/2020",
			"close_val":0.13948
		},
		{
			"date":"11/21/2020",
			"close_val":0.06011
		}
	],
	"flm":[
		{
			"date":"09/26/2020",
			"close_val":0.8518
		},
		{
			"date":"11/13/2020",
			"close_val":0.1878
		}
	],
	"ftm":[
		{
			"date":"09/02/2020",
			"close_val":0.04115
		},
		{
			"date":"11/21/2020",
			"close_val":0.01986
		}
	],
	"ftt":[
		{
			"date":"08/29/2020",
			"close_val":4.171
		},
		{
			"date":"11/17/2020",
			"close_val":3.921
		}
	],
	"gto":[
		{
			"date":"08/29/2020",
			"close_val":0.01256
		},
		{
			"date":"11/21/2020",
			"close_val":0.00740
		}
	],
	"hbar":[
		{
			"date":"08/13/2020",
			"close_val":0.05475
		},
		{
			"date":"11/21/2020",
			"close_val":0.03293
		}
	],
	"hive":[
		{
			"date":"08/17/2020",
			"close_val":0.2766
		},
		{
			"date":"11/21/2020",
			"close_val":0.1302
		}
	],
	"hot":[
		{
			"date":"08/13/2020",
			"close_val":0.0008752
		},
		{
			"date":"11/21/2020",
			"close_val":0.0005571
		}
	],
	"idex":[
		{
			"date":"08/29/2020",
			"close_val":0.11502
		},
		{
			"date":"11/17/2020",
			"close_val":0.04581
		}
	],
	"iost":[
		{
			"date":"08/17/2020",
			"close_val":0.007358
		},
		{
			"date":"11/17/2020",
			"close_val":0.004986
		}
	],
	"iotx":[
		{
			"date":"08/29/2020",
			"close_val":0.010739
		},
		{
			"date":"11/21/2020",
			"close_val":0.007879
		}
	],
	"jst":[
		{
			"date":"08/13/2020",
			"close_val":0.07469
		},
		{
			"date":"11/21/2020",
			"close_val":0.02441
		}
	],
	"kava":[
		{
			"date":"08/13/2020",
			"close_val":4.6238
		},
		{
			"date":"11/17/2020",
			"close_val":1.8733
		}
	],
	"key":[
		{
			"date":"08/25/2020",
			"close_val":0.005149
		},
		{
			"date":"11/21/2020",
			"close_val":0.002759
		}
	],
	"knc":[
		{
			"date":"08/13/2020",
			"close_val":1.817
		},
		{
			"date":"11/21/2020",
			"close_val":1.035
		}
	],
	"lrc":[
		{
			"date":"09/14/2020",
			"close_val":0.25949
		},
		{
			"date":"11/17/2020",
			"close_val":0.19049
		}
	],
	"ltc":[
		{
			"date":"08/17/2020",
			"close_val":63.38
		},
		{
			"date":"11/09/2020",
			"close_val":62.22
		}
	],
	"matic":[
		{
			"date":"08/13/2020",
			"close_val":0.02865
		},
		{
			"date":"11/21/2020",
			"close_val":0.01941
		}
	],
	"mft":[
		{
			"date":"08/25/2020",
			"close_val":0.003430
		},
		{
			"date":"11/21/2020",
			"close_val":0.002204
		}
	],
	"mith":[
		{
			"date":"08/13/2020",
			"close_val":0.001132
		},
		{
			"date":"11/21/2020",
			"close_val":0.00551
		}
	],
	"nbs":[
		{
			"date":"09/18/2020",
			"close_val":0.01266
		},
		{
			"date":"11/13/2020",
			"close_val":0.00666
		}
	],
	"neo":[
		{
			"date":"09/14/2020",
			"close_val":23.148
		},
		{
			"date":"11/21/2020",
			"close_val":18.123
		}
	],
	"one":[
		{
			"date":"08/13/2020",
			"close_val":0.01270
		},
		{
			"date":"11/21/2020",
			"close_val":0.00560
		}
	],
	"ong":[
		{
			"date":"06/26/2020",
			"close_val":0.2517
		},
		{
			"date":"11/21/2020",
			"close_val":0.1275
		}
	],
	"oxt":[
		{
			"date":"09/18/2020",
			"close_val":0.3395
		},
		{
			"date":"11/21/2020",
			"close_val":0.2606
		}
	],
	"perl":[
		{
			"date":"08/13/2020",
			"close_val":0.07882
		},
		{
			"date":"11/21/2020",
			"close_val":0.02273
		}
	],
	"qtum":[
		{
			"date":"08/17/2020",
			"close_val":3.919
		},
		{
			"date":"11/21/2020",
			"close_val":2.654
		}
	],
	"ren":[
		{
			"date":"08/29/2020",
			"close_val":0.48720
		},
		{
			"date":"11/21/2020",
			"close_val":0.35409
		}
	],
	"req":[
		{
			"date":"07/16/2020",
			"close_val":0.00000479
		},
		{
			"date":"11/21/2020",
			"close_val":0.00000135
		}
	],
	"rsr":[
		{
			"date":"08/29/2020",
			"close_val":0.02845
		},
		{
			"date":"11/17/2020",
			"close_val":0.02212
		}
	],
	"sand":[
		{
			"date":"08/13/2020",
			"close_val":0.066703
		},
		{
			"date":"11/21/2020",
			"close_val":0.039217
		}
	],
	"stmx":[
		{
			"date":"08/13/2020",
			"close_val":0.003523
		},
		{
			"date":"11/21/2020",
			"close_val":0.002353
		}
	],
	"sushi":[
		{
			"date":"08/29/2020",
			"close_val":8.566
		},
		{
			"date":"11/21/2020",
			"close_val":1.613
		}
	],
	"tct":[
		{
			"date":"08/29/2020",
			"close_val":0.21100
		},
		{
			"date":"11/21/2020",
			"close_val":0.008717
		}
	],
	"tfuel":[
		{
			"date":"05/21/2020",
			"close_val":0.013507
		},
		{
			"date":"11/21/2020",
			"close_val":0.009165
		}
	],
	"trx":[
		{
			"date":"09/02/2020",
			"close_val":0.03576
		},
		{
			"date":"11/21/2020",
			"close_val":0.02972
		}
	],
	"win":[
		{
			"date":"09/02/2020",
			"close_val":0.00012422
		},
		{
			"date":"11/21/2020",
			"close_val":0.00009817
		}
	],
	"wtc":[
		{
			"date":"08/21/2020",
			"close_val":0.6686
		},
		{
			"date":"11/21/2020",
			"close_val":0.3571
		}
	],
	"xlm":[
		{
			"date":"08/13/2020",
			"close_val":0.10861
		},
		{
			"date":"11/13/2020",
			"close_val":0.08402
		}
	],
	"xrp":[
		{
			"date":"08/13/2020",
			"close_val":0.30641
		},
		{
			"date":"11/09/2020",
			"close_val":0.25761
		}
	],
	"zec":[
		{
			"date":"08/05/2020",
			"close_val":94.81
		},
		{
			"date":"11/17/2020",
			"close_val":68.15
		}
	],
	"zrx":[
		{
			"date":"08/21/2020",
			"close_val":0.6973
		},
		{
			"date":"11/21/2020",
			"close_val":0.4094
		}
	]
}

def format_date(some_date):
	a = some_date.split("/")
	return datetime(int(a[2]), int(a[0]), int(a[1]))

def get_day_count(date_a, date_b):
	try:
		return date_a - date_b
	except:
		return None

def get_vals(val_a, val_b):
	try:
		return val_a - val_b
	except:
		return None

def thet_ratio(date_data, current_index):
	print(current_index)
	# for a, b in enumerate(date_data[current_index]):
		# try:
	c = get_day_count(format_date(date_data[current_index][1]["date"]), format_date(date_data[current_index][0]["date"]))
	d = get_day_count(format_date(date_data["theta"][1]["date"]), format_date(date_data["theta"][0]["date"]))
	e = get_day_count(format_date(date_data[current_index][0]["date"]), format_date(date_data["theta"][0]["date"]))
	# f = get_day_count(format_date(date_data["theta"][len(date_data["theta"])-1]["date"]), format_date(date_data["theta"][len(date_data["theta"])-2]["date"]))
	f = get_day_count(format_date(date_data["theta"][len(date_data["theta"])-2]["date"]), format_date(date_data["theta"][len(date_data["theta"])-3]["date"]))
			# f = format_date(date_data[current_index][a+1]["date"]) + 
	
	# z = date_data[current_index][1]["close_val"] - date_data[current_index][0]["close_val"]

	# get the percentage of growth of thet, for the step others have yet to jump from aka their second index
	y = (date_data["theta"][2]["close_val"] / date_data["theta"][1]["close_val"])
	x = (date_data["theta"][3]["close_val"] / date_data["theta"][1]["close_val"])
	w = (date_data["theta"][1]["close_val"] / date_data["theta"][0]["close_val"]) / (date_data[current_index][1]["close_val"] / date_data[current_index][0]["close_val"])


	estimate_days 	= int((c/d)*int(str(f).split(" days")[0]))
	estimate_date 	= timedelta(days=estimate_days) + format_date(date_data[current_index][len(date_data[current_index])-1]["date"])
	estimate_val 	= y*date_data[current_index][1]["close_val"]
	estimate_val_b 	= w*date_data[current_index][1]["close_val"]
	fin_val_est 	= x*date_data[current_index][1]["close_val"]
	curr_val 		= date_data[current_index][len(date_data[current_index])-1]["close_val"]
	fin_val_est_b 	= x*curr_val
	# estimate_date = timedelta(days=estimate_days) + format_date(date_data[current_index][len(date_data[current_index])-1]["date"])
	
	# print(z)
	# print(c)
	# print(d)
	# print(e)
	# print(f)
	print("estimate_days    :   " + str(estimate_days))
	print("estimate_date    :   " + str(estimate_date))
	print("curr_val         :   " + str(curr_val))
	print("estimate_val     :   " + str(estimate_val))
	print("estimate_val_b   :   " + str(estimate_val_b))
	print("fin_val_est      :   " + str(fin_val_est))
	print("fin_val_est_b    :   " + str(fin_val_est_b))
	print("-"*50)
			# return 
		# except:
			# pass
	print("-"*50)

def init():
	for a in date_data:
		z = thet_ratio(date_data, a)
		# print(z)
		# for c, b in enumerate(date_data[a]):
			# try:
				# d = get_day_count(format_date(date_data[a][c+1]["date"]), format_date(date_data[a][c]["date"]))
				# e = date_data[a][c+1]["close_val"] - date_data[a][c]["close_val"]
				# f = date_data[a][c+1]["close_val"] / date_data[a][c]["close_val"]
				# g = date_data[a][len(date_data[a])-1]["close_val"] / date_data[a][0]["close_val"]
				# h = date_data[a][len(date_data[a])-1]["close_val"] / date_data[a][len(date_data[a])-2]["close_val"]
				# e = get_day_count(format_date(date_data[a][c+1]["date"]), format_date(date_data[a][c]["date"]))
				# if h > 1.0:
				# 	print(a)
				# 	print(d)
				# 	# print(f)
				# 	print(h)
				# 	print("-"*50)
			# except:
			# 	pass

init()

# IN
# algo
# bat
# coti
# ftm
# knc
# btc
# ftt
# arpa
# fet
# hive
# iost
# jst
# tfuel
# theta
# wtc
# iotx
# dent
# ast
# hbar
# btt
# kava
# matic
# neo
# one
# perl
# ctxc
# req
# mith
# mft
# tct
# zrx

# OUT
# etc
# ada
# gto
# rsr
# sand
# stmx
# lrc
# ltc
# hot
# bch
# cvc
# dash
# bzrx
# oxt
# crv
# sushi


# MEH/IDK
# xlm
# xrp
# zec
# flm
# trx
# win
# qtum
# strax
# ren
# key
# nbs
# idex
# ong
# crv
# akro
# bts
# doge
# dusk
# eos
# cgld
# cocos
# aave
# aion
# alpha
# ardr
# ankr