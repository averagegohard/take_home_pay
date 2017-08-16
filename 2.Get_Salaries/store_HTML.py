import time
import us
import urllib
import random

# global value containing state codes so it wont need to be
# created each time we want to use it
state_codes = us.states.mapping('name', 'abbr')

#access and store the html files to minimize the number of requests
def main():
	links = '../1.Get_Links/processed_links/city_links.csv'

	for line in open(links, 'r'):
		# could be changed into an object, but ehhh
		city_info = line.strip().split(',')
		link = city_info[-1]

		FOLDER_NAME = 'All_Salaries/'
		# there probably should be a better way to store the info
		file_name = FOLDER_NAME + extract_formatted_name(city_info)+'.html'
		print file_name
		# access and store the html file
		urllib.urlretrieve(link, file_name)

		# avoid spamming the website
		time.sleep(30+random.random()*15)


# technically this should be placed in its own module instead of
# copy/pasted from get_potential_cities.py
def extract_formatted_name(values):
    global state_codes
    # format the name for use in the url
    return values[0].replace(' ', '-') + '-' + state_codes[values[1].decode('utf-8')].encode('utf-8')


if __name__ == '__main__':
	main()