import glob
import os
import time
import random
import urllib

# TODO find way to avoid using ugly global variables
HOUSING_FOLDER = 'Housing/'
SALARY_FOLDER = 'All_Salaries/'

def main():
    global HOUSING_FOLDER
    global SALARY_FOLDER

    for file_name in glob.glob(os.path.join(SALARY_FOLDER, '*.html')):
        download_page(file_name)


def download_page(file_name):
    time.sleep(sleep_time)
    if not exists(file_name):
        get_page(file_name)
    elif is_captcha(file_name):
        get_page(file_name)

def exists(file_name):
    global HOUSING_FOLDER
    parsed_housing = glob.glob(os.path.join(HOUSING_FOLDER))
    # checks if a file already exists
    return file_name in parsed_housing


def get_page(file_name, sleep_time = 30):
    sleep_time += random.random()*15

    # functionality for acquiring the page
    global HOUSING_FOLDER
    # get the pages
    city_name = file_name_to_city_name(file_name)
    print city_name

    link = 'https://www.zillow.com/'+city_name+'/home-values/'
    urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

    time.sleep(sleep_time)
    file_name, _ = urllib.urlretrieve(link, HOUSING_FOLDER + city_name + '.html')
    
    if is_captcha(file_name):
        # if we receive a captcha page, increase the sleep time by a random factor
        # so eventually the captcha will be resolved
        get_page(file_name, sleep_time*(1+random.random())


# will need more robust check in the future
def is_captcha(file_name):
    with open(file_name) as f:
        return 'captcha' in f.read()


def file_name_to_city_name(file_name):
    name_html = file_name.split('/')[1]
    # removes the .html extension
    name = name_html[:-5]
    return name


if __name__ == '__main__':
    main()
