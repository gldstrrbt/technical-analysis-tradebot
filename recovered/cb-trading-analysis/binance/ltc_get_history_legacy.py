import pandas as pd
import numpy as np
import cbpro, time
import os, csv, pytz
from datetime import datetime, timedelta
from time import sleep
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from itertools import chain
import email
import imaplib


this_is 	= True

hard_stop   = False
hard_reset  = False

def send_test():
	a 		= open("ep.txt", "r+")
	b 		= [c for c in a]

	f 	= b[0]
	g 	= b[1]

	d 	= "smtp.gmail.com"
	e 	= "465"
	
	
	
	h 	= f
	i 	= [f]

	j = MIMEText("SOME MSG")
	j["Subject"] = "shit"
	j["From"] = f
	j["To"] = f
	j.set_charset("utf-8")

	k = smtplib.SMTP_SSL(d, e)
	k.login(f, g)
	k.sendmail(h, i, j.as_string())
	k.quit()


def fuck():
	a = open("ep.txt", "r+")
	b = [c for c in a]
	f = b[0]
	g = b[1]

	m = imaplib.IMAP4_SSL('imap.gmail.com')
	m.login(f, g)
	m.select()
	for uid, msg in m.idle(): # yield new messages
	    print(msg)


def read_test():
	global this_is 
	global hard_stop
	global hard_reset
	
	a = open("ep.txt", "r+")
	b = [c for c in a]
	f = b[0]
	g = b[1]

	m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
	m.login(b[0],b[1])
	
	try:	
		# m.select('"[Gmail]/All Mail"')
		# m.select('"[Gmail]/All Mail"')
		m.select('INBOX')
		subject = "shit"
		# result, data = m.uid('search', None, "ALL")
			
		while True:
			if hard_stop == True:
				result, data = m.uid('search', None, '(UNSEEN SUBJECT "asdf")')
			elif hard_stop == False:
				result, data = m.uid('search', None, '(UNSEEN SUBJECT "shit")')
			# print(data.split())
			# print("-----------")
			# result, data = m.search(None, '(SUBJECT "%s")' % subject)
			if result == 'OK':
				if len(data[0]) > 0:
					for num in data[0].split():
						result, data = m.uid('fetch', num, '(RFC822)')
						# print(data)
						# for kk in data:
							# print(kk.split())
							# for qq in kk:
							# 	print(qq)
							# 	print("-"*20)
					if result == 'OK':
						email_message = email.message_from_bytes(data[0][1])    # raw email text including headers
						print(email_message)
						print('From:' 		+ email_message['From'])
						print('Subject:' 	+ email_message['Subject'])
						if email_message["Subject"] == "shit":
							hard_stop 	= True
							hard_reset 	= True

						elif email_message["Subject"] == "asdf":
							hard_stop 	= False
							hard_reset 	= False
							print(hard_stop)
							print(hard_reset)
			time.sleep(2)

	finally:
		try:
			m.close()
		except:
			pass
		m.logout()








def init():
	global this_is 
	global hard_stop
	global hard_reset

	hard_stop 	= False
	hard_reset 	= False

	while True:
		try:
			if hard_stop == False and hard_reset == False:
				print(hard_stop)
				print(hard_reset)
				print("-----------")
				try:
					product = 'LTC-USD'
					# granularity = 60 # MINUTE INTERVALS
					granularity = 60 # MINUTE INTERVALS
					# start = (datetime.now() - timedelta(days=150)) AUGUST
					# start = (datetime.now() - timedelta(days=1))
					start = (datetime.now(pytz.timezone("America/New_York")) - timedelta(days=1))
					end = datetime.now(pytz.timezone("America/New_York"))
					delay = 1
					# output_file = datetime.now(pytz.timezone("America/New_York")).strftime("%Y%m%d_%H%M%S" + "__") + '_data.csv'
					output_file = 'buffer_data_ltc.csv'

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
						records = public_client.get_product_historic_rates(product, granularity=granularity, start=period_start.isoformat(), end=period_end.isoformat())
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

						# Convert to Pandas DataFrame
						records = np.array(records)
						df = pd.DataFrame(records[:,1:], index=records[:,0], columns=['Low', 'High', 'Open', 'Close', 'Volume'])
						df.index = pd.to_datetime(pd.to_numeric(df.index), utc=True, unit='s')
						df = df.sort_index(ascending=True)

						print ("exporting " + str(period_start))
						# df.to_csv(output_file, mode='a+', sep=',', header=False)
						df.to_csv(output_file, mode='a+', sep=',', header=False)

					time.sleep(5)
					print ("done")
				except:
					pass
			elif hard_stop == True and hard_reset == True:
				print("***********STOP***********")
				print(hard_stop)
				print(hard_reset)
				hard_stop 	=  False
				init()
				continue
		except:
			pass



Thread(target=init).start()
Thread(target=read_test).start()
# Thread(target=init).start()
# fuck()
# Thread(target=send_test).start()


# read_test()


