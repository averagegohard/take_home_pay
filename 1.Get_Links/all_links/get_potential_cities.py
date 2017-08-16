import requests
from bs4 import BeautifulSoup
from string import ascii_uppercase
import time
import random

# quick and dirty way to get the potential cities
# will need cleanup if used again
def main():
	potential_cities = get_potential_cities()
	with open('potential_cities.csv', 'w') as f:
		for city in potential_cities:
			f.write(city+'\n')

def get_potential_cities():
	# use payscale location index to get potential cities
	base_url = 'https://www.payscale.com/index/US/Location/*'
	names = []
	for c in ascii_uppercase:
		base_url = base_url[:-1] + c
		soup = get_soup(base_url)

		names += get_names(soup)

	return names


def get_names(soup):
	# get city names from index page
	table = soup.findAll('table')[0].findAll('tr')
	names = []
	for tag in table:
		# FIXME: first line for each character is just 1 comma
		name = ''
		count = ''
		for res in tag.findAll('a'):
			# remove whitespace between city and state
			name = res.text.replace(', ',',')

		for counts in tag.findAll('td', { "class" : "hidden-xs" }):
			count = counts.text.strip().replace(',','')
		name_and_rank = name+','+count
		names.append(name_and_rank.encode('utf-8'))

	return names

def get_soup(url):
	# get the soup while trying not to spam
	time.sleep(3+random.random()*15)
	return BeautifulSoup(requests.get(url).content, "html.parser")


if __name__ == '__main__':
	main()