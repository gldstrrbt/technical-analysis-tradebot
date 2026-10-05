import os, csv, pytz, cbpro
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from time import sleep

class history_data():
	def __init__(self):
		print(self)
	def get_history_data(auth, product_symbol, num_days):  
		try:	
			product = product_symbol+'-USD'
			granularity = 60 # SECOND INTERVALS
			# start = (datetime.now() - timedelta(days=150)) AUGUST
			# start = (datetime.now() - timedelta(days=1))
			start = (datetime.now(pytz.timezone("America/New_York")) - timedelta(days=num_days))
			end = datetime.now(pytz.timezone("America/New_York"))
			delay = 1
			output_file = product_symbol+'_buffer_data.csv'

			a = open(str(output_file), "w+")
			b = csv.writer(a)

			# if os.path.exists(output_file):
			#     os.remove(output_file)
				

			public_client = auth
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

				# print(records)
				# Convert to Pandas DataFrame
				if end < period_end:
					# print(records)
					# print(records[len(records)-1])
					zz = public_client.get_product_ticker(product_id=product_symbol+'-USD')
					# print(zz["price"])
					records[len(records)-1][3] = float(zz["price"])
					print(records[len(records)-1])
					# print(records)
				records = np.array(records)
				# print("")
				# print("")
				# print("")
				# print(records)
				# print("----------------")
				df = pd.DataFrame(records[:,1:], index=records[:,0], columns=['low', 'high', 'open', 'close', 'volume'])
				# df = pd.DataFrame(records[:,1:], index=records[:,0], columns=['open', 'high', 'low', 'close', 'volume'])
				df.index = pd.to_datetime(pd.to_numeric(df.index), unit='s')
				df = df.sort_index(ascending=True)

				print ("exporting " + str(period_start))
				# df.to_csv(output_file, mode='a+', sep=',', header=False, columns=['low', 'high', 'open', 'close', 'volume'])
				df.to_csv(output_file, mode='a+', sep=',', header=False)
			a.close()
			print ("done")
		except:
			pass