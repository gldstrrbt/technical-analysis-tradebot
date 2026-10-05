import pandas as pd
import numpy as np
import cbpro
import os, csv
from datetime import datetime, timedelta
from time import sleep

class history_data():
	def __init__(self):
		print(self)
	def get_history_data():  
		product = 'LTC-USD'
		# granularity = 60 # MINUTE INTERVALS
		granularity = 60 # MINUTE INTERVALS
		# start = (datetime.now() - timedelta(days=150)) AUGUST
		start = (datetime.now() - timedelta(days=1))
		end = datetime.now()
		delay = 1
		output_file = datetime.now().strftime("buffer" + "__") + '_data.csv'
		# output_file = datetime.now().strftime("%Y%m%d_%H%M%S" + "__") + '_data.csv'

		a = open(str(output_file), "w+")
		b = csv.writer(a)

		# if os.path.exists(output_file):
		#     os.remove(output_file)
			

		public_client = cbpro.PublicClient()
		data_frames = []

		step = timedelta(seconds=(granularity * 250))

		periods = (end - start).total_seconds() / granularity
		period_start = start
		period_end = start + step

		if period_end > end:
			period_end = end

		while period_end <= end:
			# Retrieve the set
			# records = public_client.get_product_historic_rates(product, granularity=granularity, start=period_start.isoformat(), end=period_end.isoformat())
			records = public_client.get_product_historic_rates(product, granularity=granularity, start=period_start, end=period_end)
			if not isinstance(records, (list)):
				raise TypeError("Instance is not a list: %s" % records)

			# coinbasepro has a strict use policy
			if delay and delay > 0:
				sleep(delay)

			# Iterate and observe any remaining elements after boundary
			period_start += step
			period_end += step
			if period_end > end and period_start < end:
				period_end = end

			if not records:
				continue

			print(records)
			# Convert to Pandas DataFrame
			records = np.array(records)
			print("")
			print("")
			print("")
			print(records)
			print("----------------")
			df = pd.DataFrame(records[:,1:], index=records[:,0], columns=['low', 'high', 'open', 'close', 'volume'])
			# df = pd.DataFrame(records[:,1:], index=records[:,0], columns=['open', 'high', 'low', 'close', 'volume'])
			df.index = pd.to_datetime(pd.to_numeric(df.index), unit='s')
			df = df.sort_index(ascending=True)

			print ("exporting " + str(period_start))
			# df.to_csv(output_file, mode='a+', sep=',', header=False, columns=['low', 'high', 'open', 'close', 'volume'])
			df.to_csv(output_file, mode='a+', sep=',', columns=['low', 'high', 'open', 'close', 'volume'])
		a.close()
		print ("done")

	def csv_header():
		a = open("buffer___data.csv", "r+")
		b = csv.reader(a)
		c = [d for d in b]
		d = c[0][0] = "date"
		e = open("buffer___data.csv", "w+")
		f = csv.writer(e)
		for h, g in enumerate(c):
			f.writerow(g)
		e.close()
		print(d)
		print ("done")
