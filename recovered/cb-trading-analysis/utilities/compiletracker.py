import csv

def read_csv(filepath):
	a = open(filepath, "r")
	b = csv.reader(a)
	return [c for c in b]

def write_csv(filepath, dataset):
	new_filepath = "total_" + filepath
	a = open(new_filepath, "w", newline="")
	b = csv.writer(a)
	for c in dataset:
		b.writerow(c) 

def sum_csv(dataset):
	a = []
	for b, c in enumerate(dataset):
		if b != 0:
			d 		= []
			for f, e in enumerate(c):
				if e == "":
					break
				if f != 0:	
					print(e)
					print(float(e))
					print(isinstance(float(e), float))
					print("*"*50)
					if isinstance(float(e), float):
						d.append(float(e))
			d = [c[0]] + d + [sum(d)]
			a.append(d)
	return a

def init():
	filepath 	= "tracking_10-25-2021.csv"
	a 			= read_csv(filepath)
	b 			= sum_csv(a)
	print(b)
	write_csv(filepath, b)

init()