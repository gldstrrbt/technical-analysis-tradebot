import os
import json
import robin_stocks as r
import pandas as pd 
# import numpy as np


un = os.getenv("ROBINHOOD_USERNAME", "")
pw = os.getenv("ROBINHOOD_PASSWORD", "")
login = r.authentication.login(un, pw, expiresIn=86400, scope="internal", by_sms=True, store_session=True) if un and pw else None


buy 		= True
start 		= 100
crypt 		= 0
balance		= start
fin_price 	= 0.0

def relative_strength_index(df, n):
	"""Calculate Relative Strength Index(RSI) for given data.
	
	:param df: pandas.DataFrame
	:param n: 
	:return: pandas.DataFrame
	"""
	i = 0
	UpI = [0]
	DoI = [0]
	# print(df.columns())
	while i + 1 <= df.index[-1]:
		UpMove = float(df.loc[i + 1, 'high_price']) - float(df.loc[i, 'high_price'])
		DoMove = float(df.loc[i, 'low_price']) - float(df.loc[i + 1, 'low_price'])
		if UpMove > DoMove and UpMove > 0:
			UpD = UpMove
		else:
			UpD = 0
		UpI.append(UpD)
		if DoMove > UpMove and DoMove > 0:
			DoD = DoMove
		else:
			DoD = 0
		DoI.append(DoD)
		i = i + 1
	UpI = pd.Series(UpI)
	DoI = pd.Series(DoI)
	PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
	NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
	# RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI_' + str(n))
	RSI = pd.Series(PosDI / (PosDI + NegDI), name='rsi')
	df = df.join(RSI)
	return df

def rsi_check(df):
	global buy
	global start
	global crypt
	global balance
	global fin_price
	a = 0
	while a <= df.index[-1]:
		print(df.loc[a])
		if float(df.loc[a ,"rsi"]) >= 0.90 and buy == False:
			balance = crypt*float(df.loc[a ,"close_price"])
			crypt 	= 0.0
			buy 	= True
		if float(df.loc[a ,"rsi"]) <= 0.10 and buy == True:
			print(a)
			crypt 	= balance/float(df.loc[a ,"close_price"])
			balance = 0.0
			buy 	= False

		fin_price = float(df.loc[a ,"close_price"])
		a+=1
	print(balance)
	print(crypt*fin_price)

def init():
	a = r.get_crypto_historicals("DOGE", interval='10minute', span='week', bounds='24_7', info=None)
	# print(a)
	# a = json.loads(a)
	# b = pd.read_json(a)
	b = pd.json_normalize(a)
	c = relative_strength_index(b, 7)
	# print(c)
	rsi_check(c)

init()