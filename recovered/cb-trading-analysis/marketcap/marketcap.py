import os, json, matplotlib, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def plot_marketcap_init(df, color):
	plt.plot(df["data"],label="cur", color=color)
	plt.plot(df["data"],label="Marketcap", color=color)
	plt.legend(loc='best')
	plt.title('Crypto Marketcap\nClose and Moving Averages')
	plt.show()

def marketcap_moving_average(df, n, color):
	compiled_sma 	= pd.Series(df["data"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	plt.plot(df["sma_"+str(n)],label="sma_"+str(n), color=color)
	return df

def load_json(filepath):
	a = open(filepath, "r+")
	return json.load(a)

def convert_json(dataset):
	pd.set_option('display.float_format', lambda x: '%.3f' % x)
	return pd.read_json(dataset, orient="records")

def moving_average(df, n):
	compiled_sma 	= pd.Series(df["data"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df

def init():
	filepath 	= "./historical-marketcap-total.json"
	colors 		= ["#ff00ff", "#00ccff", "#ff1100"]
	df 			= convert_json(filepath)
	df 			= marketcap_moving_average(df, 200, colors[0])
	df 			= marketcap_moving_average(df, 50, colors[1])
	df 			= marketcap_moving_average(df, 20, colors[2])
	plot_marketcap_init(df, "black")

init()