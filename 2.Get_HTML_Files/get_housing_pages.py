import glob
import os
import time
import random
import urllib

# WILL FAIL FOR ST. LOUIS, FIXME
def main():
    HOUSING_FOLDER = 'Housing/'
    SALARY_FOLDER = 'All_Salaries/'

    parsed_housing = glob.glob(os.path.join(HOUSING_FOLDER))

    for file_name in glob.glob(os.path.join(SALARY_FOLDER, '*.html')):
        city_name = file_name_to_city_name(file_name)
        print city_name
        if '.' in city_name:
            link = 'https://www.zillow.com/'+city_name+'/home-values/'
            urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

            urllib.urlretrieve(link, HOUSING_FOLDER + city_name + '.html')

            # avoid spamming the website
            time.sleep(30+random.random()*15)


def file_name_to_city_name(file_name):
    name_html = file_name.split('/')[1]
    # removes the .html extension
    name = name_html[:-5]
    return name


if __name__ == '__main__':
    main()
