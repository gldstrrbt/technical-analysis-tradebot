import requests
from bs4 import BeautifulSoup as soup

urls = [
	{
		"index":"https://theblockcrypto.com",
		"index_src":"",
		"collected_links":[],
		"domain_links":[]
	}, 
	{
		"index":"https://dailyhodl.com",
		"index_src":"",
		"collected_links":[],
		"domain_links":[]
	}, 
	{
		"index":"https://news.bitcoin.com",
		"index_src":"",
		"collected_links":[],
		"domain_links":[]
	}, 
	{
		"index":"https://cointelegraph.com",
		"index_src":"",
		"collected_links":[],
		"domain_links":[]
	}, 
	{
		"index":"https://decrypt.co",
		"index_src":"",
		"collected_links":[],
		"domain_links":[]
	}, 
	{
		"index":"https://www.coindesk.com"
	}]


def get_url(url):
	a = requests.get(url)
	return a.content

def soupify(dataset):
	return soup(dataset, "html.parser")

def get_links(dataset):
	a = dataset.find_all("a")
	for b in a:
		print(b)
	print("*"*50)

def init():
	for a in urls:
		b = get_url(a["index"])
		c = soupify(b)
		get_links(c)

init()