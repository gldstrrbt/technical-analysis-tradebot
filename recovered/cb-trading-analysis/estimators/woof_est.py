import random

start_qty 			= 1500
#start_daily_output 	= 48
start_daily_output 	= 396
gen_ratio 			= start_daily_output/start_qty
# current_val 		= 4.50
current_val 		= 5.0

new_qty 			= start_qty
new_output 			= start_daily_output
# new_val 			= 

woofed_percent 		= 0.67
compounded_percent 	= 0.33
woofed_amount 		= 36.57522
compounded_amount 	= 0.33

counter				= 0
days 				= 180


def fantasy_estimate():
	while counter < days:
		# random.uniform(1.5, 1.9)
		# gen_ratio 	= start_daily_output/start_qty
		new_qty += (new_output*compounded_percent)/2
		new_output 	= new_qty*gen_ratio
		print("counter   : ", counter)
		print("new_qty   : ", new_qty)
		print("new_output: ", new_output)
		print("output_val: ", current_val*new_output)
		print("total_val : ", current_val*new_qty)
		print("*"*50)
		counter+=1


def sslp_fantasy_estimate():
	global counter
	global days
	sslp_start 	= 4.19417
	start_rate 	= 6.1
	new_rate 	= start_rate
	sslp_output = ((sslp_start*new_rate)*compounded_percent)/2

	while counter < days:
		print("counter    : ", counter)
		print("sslp_start : ", sslp_start)
		print("sslp_output: ", sslp_output)
		print("new_rate   : ", new_rate)
		print("output_val : ", current_val*sslp_output)
		print("total_val  : ", current_val*sslp_start)
		print("*"*50)
		sslp_start += sslp_output
		new_rate 	= random.uniform(0.15, 10.0)
		sslp_output = ((sslp_start*new_rate)*compounded_percent)/2 
		counter+=1


def realistic_estimate():
	global counter
	global days
	# global new_qty
	# global new_output
	new_qty 			= start_qty
	new_output 			= start_daily_output
	new_price 			= current_val
	fuck_counter 		= 0
	total_locked 		= 672
	while fuck_counter < days:
		# random.uniform(1.5, 1.9)
		# gen_ratio 	= start_daily_output/start_qty
		new_qty += (new_output*compounded_percent)/2
		total_locked += new_output*0.67;
		new_output = (new_qty*gen_ratio)*random.uniform(0.05, 0.8)
		print("counter   : ", counter)
		print("new_qty   : ", new_qty)
		print("new_output: ", new_output)
		print("new_price : ", new_price)
		print("output_val: ", new_price*new_output)
		print("total_val : ", new_price*new_qty)
		print("total_locked : ", total_locked)
		print("locked_val : ", total_locked*new_price)
		print("*"*50)
		# new_price = random.uniform(0.25,6.0)
		new_price = random.uniform(2.25,7.50)
		fuck_counter+=1
	return new_price*new_qty


def average_output():
	avg_counter = 0
	avg_steps 	= 100
	avg_arr 	= []
	while avg_counter < avg_steps:
		avg_arr.append(realistic_estimate())
		avg_counter+=1
	print(avg_arr)
	print(sum(avg_arr)/len(avg_arr))


def init():
	# fantasy_estimate()
	# sslp_realistic_estimate()
	realistic_estimate()
	# average_output()

init()