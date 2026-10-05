import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
plt.style.use('ggplot')

def get_stock_data(ticker, start_date, end_date):
	df = web.DataReader(ticker,'stooq', start_date, end_date)
	return df

def closing_moving_average(df, n, color):
	compiled_sma 	= pd.Series(df["Close"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	plt.plot(df["sma_"+str(n)],label="sma_"+str(n), color=color)
	return df

def reorder_dataframe(df):
	return df.iloc[::-1]

def plot_init(df, ticker, color):
	plt.plot(df["Close"],label="Close", color=color)
	plt.legend(loc='best')
	plt.title(str(ticker)+'\nClose and Moving Averages')
	plt.show()

def init():
	start_date 	= datetime.datetime(2016, 1, 1)
	end_date 	= datetime.datetime(2020, 1, 6)
	ticker 		= "amd"
	colors 		= ["#ff00ff", "#00ccff", "#ff1100"]
	df 			= get_stock_data(ticker, start_date, end_date)
	df 			= reorder_dataframe(df)
	# df 			= closing_moving_average(df, 21, colors[1])
	# df 			= closing_moving_average(df, 9, colors[2])
	df 			= closing_moving_average(df, 200, colors[0])
	df 			= closing_moving_average(df, 50, colors[1])
	df 			= closing_moving_average(df, 20, colors[2])
	plot_init(df, ticker, "black")
	print(df)

init()