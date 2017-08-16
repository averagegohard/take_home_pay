from bs4 import BeautifulSoup
import os
import glob

site = 'http://www.payscale.com'


# input should probably be more extensible and merged with store_HTML.py
def main(level_folder='Entry-Level/'):
	global site
	BASE_FOLDER_NAME = 'All_Salaries/'

	# copied from SO, used to access all html files in the directory
	for filename in glob.glob(os.path.join(BASE_FOLDER_NAME, '*.html')):
	    print filename
		soup = BeautifulSoup(open(filename))


		for a in soup.findall('a', href=True):
			# if the name is in the link, we know it is what
			# we are looking for
			if level_folder in a['href']:

				# this should probably be a function in its own module
				# instead of copy/pasting
				# *there probably should be a better way to store the info
				# access and store the html file
				urllib.urlretrieve(site+a['href'], level_folder+'/'+filename)

				# avoid spamming the website
				time.sleep(30+random.random()*15)

				break


if __name__ == '__main__':
	main()