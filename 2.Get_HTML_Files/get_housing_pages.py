import glob
import os
import time
import random
import urllib


def main():
    HOUSING_FOLDER = 'Housing/'
    SALARY_FOLDER = 'All_Salaries/'

    for file_name in glob.glob(os.path.join(SALARY_FOLDER, '*.html')):
        city_name = file_name_to_city_name(file_name)
        print city_name

        link = 'https://www.zillow.com/'+city_name+'/home-values/'
        urllib.urlretrieve(link, HOUSING_FOLDER + city_name + '.html')

        # avoid spamming the website
        time.sleep(30+random.random()*15)


def file_name_to_city_name(file_name):
    return file_name.split('/')[1].split('.')[0]


if __name__ == '__main__':
    main()