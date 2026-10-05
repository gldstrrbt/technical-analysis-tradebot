import selenium, time, imaplib, email, base64,pickle, os.path
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import robin_stocks as r
import robin_stocks.crypto as crypto
import robin_stocks.orders as orders
import robin_stocks.helper as helper
# gmail_client_id 		= "<REDACTED>"
# gmail_client_secret 	= "<REDACTED>" 

###################################################################################

login = r.login(os.getenv("ROBINHOOD_USERNAME", ""), os.getenv("ROBINHOOD_PASSWORD", ""))

###################################################################################

options = Options()
driver = webdriver.Firefox(executable_path=r'./geckodriver')
driver.set_window_position(1024, 0)
actions = ActionChains(driver) 

###################################################################################

def open_new_tab():
	driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 

###################################################################################

def close_tab():
	driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 

###################################################################################

def open_rh():
	driver.get("https://robinhood.com")
	for a in driver.find_elements_by_css_selector('a[rel="noopener"]'):
		if "Log In" in str(a.text):
			a.click()
			break
	time.sleep(2)
	driver.find_element_by_css_selector('input[name="username"]').send_keys(os.getenv("ROBINHOOD_USERNAME", ""))
	driver.find_element_by_css_selector('input[name="password"]').send_keys(os.getenv("ROBINHOOD_PASSWORD", ""))
	driver.find_element_by_css_selector('button[type="submit"]').click()
	time.sleep(1)
	for a in driver.find_elements_by_css_selector('button'):
		if "Email Me" in str(a.text):
			a.click()
			break

###################################################################################

def enter_code(verification_code):
	driver.find_element_by_css_selector('input[name="response"]').send_keys(verification_code)
	for a in driver.find_elements_by_css_selector('button'):
		if "Confirm" in str(a.text):
			a.click()
			break

###################################################################################

def navigate_btc():
	time.sleep(10)
	driver.find_element_by_css_selector('a[href="/crypto/BTC"]').click()
	# driver.get("https://robinhood.com/crypto/BTC")

###################################################################################

def get_quote():
	a = driver.find_elements_by_css_selector("h1")[1]
	b = ""
	if len(a.text) == 1:
		try:	
			for c in a.find_elements_by_css_selector("span"):
				if c != "$" and c != "," and len(c) == 1: 
					b+=c.text
			return float(b)
		except:
			pass
	else:
		try:	
			return float(a.text.replace("$", "").replace(",", ""))
		except:
			pass

###################################################################################

def click_sell_tab():
	driver.find_element_by_css_selector('span[data-testid="OrderFormHeading-Sell"]').click()

###################################################################################

def click_buy_tab():
	for a in driver.find_elements_by_css_selector('h3'):
		if "Buy BTC" in a.text:
			a.click()

###################################################################################

def amount_input(currency_amount):
	driver.find_element_by_css_selector('input[name="amount"]').send_keys(currency_amount)

###################################################################################

def amount_price(usd_amount):
	global actions
	actions = actions.send_keys(Keys.TAB).send_keys(usd_amount)
	actions.perform()

###################################################################################

def review_order_button():
	for a in driver.find_elements_by_css_selector('button[type="submit"]'):
		if "Review Order" in a.find_element_by_css_selector('span').text:
			a.click()

###################################################################################

def submit_order(buy_sell):
	try:
	    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
	    WebDriverWait(driver, 3).until(element_present)
	except TimeoutException:
		print("Timed out waiting for page to load")
		for a in driver.find_elements_by_css_selector('button[type="button"]'):
			if "Cancel" in a.text:
				a.click()
				pass
			if "Cancel" in a.find_element_by_css_selector("span").text:
				a.click()
				pass

	# try:
	# 	driver.find_elements_by_css_selector('button[type="submit"]')[0].click()
	# except:
	# 	time.sleep(2)
	# 	driver.find_elements_by_css_selector('button[type="submit"]')[0].click()
	# for a in driver.find_elements_by_css_selector('button[type="submit"]'):
	# 	if str("Submit " + buy_sell) in a.find_element_by_css_selector('span').text:
	# 		a.click()

###################################################################################

def done_order():
	time.sleep(2)
	for a in driver.find_elements_by_css_selector('button[type="button"]'):
		if "Done" in a.find_element_by_css_selector('span').text:
			a.click()
	time.sleep(0.2)
	# countdown_to_cancel()

###################################################################################

def submit_buy(currency_amount, usd_amount):
	# cancel_placed_orders()
	click_buy_tab()
	a = get_usd_balance()
	if float(a) > 10: 
		set_to_limit_order()
		time.sleep(0.01)
		amount_input(currency_amount)
		time.sleep(0.01)
		amount_price(usd_amount)
		review_order_button()
		submit_order("Buy")
		time.sleep(0.1)
		try:
			check_modal_verification()
			done_order()
		except:
			pass

###################################################################################

def submit_sell(currency_amount, usd_amount):
	# cancel_placed_orders()
	click_buy_tab()
	set_to_limit_order()
	amount_input(currency_amount)
	amount_price(usd_amount)
	review_order_button()
	submit_order("Sell")
	time.sleep(0.1)
	try:
		check_modal_verification()
		done_order()
	except:
		pass

###################################################################################

def get_usd_balance():
	click_buy_tab()
	for a in driver.find_elements_by_css_selector('footer'):
		if "Buying Power Available" in a.text and a.text != "Available":
			return a.text.split("Buying")[0].replace("$","").replace(" ","").replace(",","")

###################################################################################

def get_crypto_balance():
	try:
		click_sell_tab()
		for a in driver.find_elements_by_css_selector('footer'):
			if "Buying Power" not in a.text:
				return a.text.split("Available")[0].replace("$","").replace(" ","").replace(",","")
	except:
		return 0.00

###################################################################################

def set_to_limit_order():
	for a in driver.find_elements_by_css_selector('header.card-heading'):
		b = a.find_elements_by_css_selector("div")
		b[7].click()
	for a in driver.find_elements_by_css_selector('a.menu-option'):
		if "Limit Order" in a.text:
			a.click()

###################################################################################

def cancel_placed_orders():
	a = driver.find_elements_by_css_selector("section")
	a = a[len(a)-1].find_elements_by_css_selector("div")
	for b in a:
		try:
			b.click()
			try:
				for c in b.find_elements_by_css_selector("a"):
					if "Cancel Order" in c.text:
						c.click()
			except:
				pass
		except:
			pass

###################################################################################

def check_modal_verification():
	# driver.execute_script('''
	# 		function cancel_orders(){var a = document.getElementsByTagName("a");for(b=0;b<a.length;b++){if("Cancel".indexOf(a[b].innerHTML >= 0)){console.log(a[b]);a[b].click();close_modal();}}}cancel_orders();function close_modal(){var a = document.getElementsByClassName("modal-container");if(a.length > 0){a = a[0];a.querySelector('button[type="submit"]')[0].click();}}
	# 	''')
	a = driver.find_elements_by_css_selector('div[class="modal-container"]')
	if len(a) > 0:
		for b in a:
			for c in b.find_elements_by_css_selector("span"):
				if "Verify Your Account" in d.text:
					b.find_element_by_css_selector('button[type="submit"]').click()

###################################################################################

def countdown_to_cancel():
	a = 0
	b = 9
	while a < b:
		if a == b:
			cancel_placed_orders()
			break
		a = a+1
		time.sleep(0.5)

###################################################################################

def get_emails():
	SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	service = build('gmail', 'v1', credentials=creds)
	results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
	messages = results.get('messages', [])
	for message in messages:
			msg = service.users().messages().get(userId='me', id=message['id']).execute()
			if "Your Email Verification Code" in str(msg):
				return soup(base64.urlsafe_b64decode(msg["payload"]["parts"][1]["body"]["data"])).find("h3").text

###################################################################################

def launch_robinhood():
	open_rh()
	time.sleep(10)
	a = get_emails()
	print(a)
	enter_code(a)
	navigate_btc()
	time.sleep(3)
	cancel_placed_orders()
	# time.sleep(3)

###################################################################################

def moving_average_alt(df, n):
	compiled_sma 	= pd.Series(df["mark_price"].rolling(n, min_periods=n).mean(), name='sma_' + str(n))
	df 				= df.join(compiled_sma)
	return df

###################################################################################

def data_to_df(datas):
	a = pd.DataFrame(datas, columns={"mark_price"})
	return a

###################################################################################

def init():
	launch_robinhood()
	amount 			= 0
	start_balance 	= float(get_usd_balance() )
	balance 		= float(start_balance) 
	
	in_order 		= False
	signal 			= True
	purchase_price 	= 0
	skim 			= 0
	y 				= 0
	data_array 		= [5,3,4,5,12]
	time_int 		= 0.5
	crypto_name 	= "BTC"
	crypto_balance 	= float(get_crypto_balance())

	while True:
		# try:	
		fuck = crypto.get_crypto_quote(crypto_name)
		data_array.append(float(fuck["mark_price"]))
		if len(data_array) > 20:
			data_array.pop(0)
		a = data_to_df(data_array)
		a = moving_average_alt(a, 3)
		a = moving_average_alt(a, 5)
		b = a.iterrows()
		c = []
		for d, e in b:
			t = []
			for s, r in enumerate(e):
				t.append(float(r))
			c.append(t)
		if in_order == True:
			y+=1
		balance 		= float(get_usd_balance())
		# time.sleep(0.2)
		crypto_balance 	= float(get_crypto_balance())
		print(balance)
		print(crypto_balance)
		submit_sell(str(crypto_balance), str(c[len(c)-1][0]))
		if signal == True and balance > 15 and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
		# if signal != True and signal != False and balance > 10 and y == 0 and (c[len(c)-2][1] >= c[len(c)-2][2] and c[len(c)-3][1] < c[len(c)-3][2]):
			if in_order == False: 
				if balance > start_balance:	
					submit_buy(str(start_balance), c[len(c)-1][0])
					purchase_price 	= float(c[len(c)-1][0])
					signal 			= False 
				else:
					submit_buy(str(balance), str(c[len(c)-1][0]))
					signal 			= False 
				in_order 		= True
			else:
				cancel_placed_orders()
				in_order = False
				signal = False
				y = 0

		# elif signal == True and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		elif signal == False and crypto_balance > 1 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
		# elif signal != True and signal != False and crypto_balance > 1 and (c[len(c)-2][1] <= c[len(c)-2][2] and c[len(c)-3][1] > c[len(c)-3][2]):
			if in_order == False: 
				submit_sell(str(crypto_balance), str(c[len(c)-1][0]))
				signal = True
				in_order 		= True
			else:
				cancel_placed_orders()
				in_order = False
				signal = True
				y = 0
	

		# if y == 9:
		# 	cancel_placed_orders()
		# 	y=0
		# 	if balance > 10:
		# 		signal = True
		# 	else:
		# 		signal = False
		# 	in_order == False
		# except:
		# 	pass
		
		print("-"*50)
		skim = balance-start_balance
		print("*"*100)
		print("*"*100)
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print(c[len(c)-1])
		print("BUY TRIGGER: " + str(balance > 10))
		print("SELL TRIGGER: " + str(crypto_balance > 1))
		print("*"*50)
		print("Y:   	"+str(y))
		print("curr:   	"+str(c[len(c)-1][0]))
		print("balance: "+str(balance))
		print("amount:  "+str(crypto_balance))
		print("signal:  "+str(signal))
		print("in_order:"+str(in_order))
		print("value:   "+str(balance+crypto_balance))
		print("skim:  	"+str(skim))
		print("*"*50)

		time.sleep(0.5)


###################################################################################

init()