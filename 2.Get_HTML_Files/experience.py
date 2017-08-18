from bs4 import BeautifulSoup
import os
import glob
import urllib
import random
import time

site = 'http://www.payscale.com'


# input should probably be more extensible and merged with store_HTML.py
def main(level_folder='Entry-Level'):
    BASE_FOLDER_NAME = 'All_Salaries/'

    raw_accessed_files = glob.glob(os.path.join(level_folder, '*.html'))
    accessed_files = []
    for filename in raw_accessed_files:
        accessed_files.append(filename.split('/')[-1])

    # copied from SO, used to access all html files in the directory
    for filename in glob.glob(os.path.join(BASE_FOLDER_NAME, '*.html')):
        if filename.split('/')[-1] not in accessed_files:
            soup = BeautifulSoup(open(filename), 'lxml')

            a_tags = soup.find_all('a', href=True)
            if a_tags:
                download_HTML(a_tags, level_folder, filename)

    # lazy but efficient
    if level_folder == 'Entry-Level':
        main(level_folder='Mid-Career')
        main(level_folder='Experienced')
        main(level_folder='Late-Career')




def download_HTML(a_tags, level_folder, filename):
    global site
    for a in a_tags:
        # if the name is in the link, we know it is what
        # we are looking for
        if level_folder in a['href']:
            city_name = filename.split('/')[-1]
            print 'Downloading ' + level_folder + '/' + city_name
            # this should probably be a function in its own module
            # instead of copy/pasting
            # *there probably should be a better way to store the info
            # access and store the html file
            urllib.urlretrieve(site+a['href'], level_folder+'/'+city_name)

            # avoid spamming the website
            time.sleep(30+random.random()*15)

            return

if __name__ == '__main__':
    main()