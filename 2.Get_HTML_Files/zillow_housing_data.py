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

    for file_name in get_files_in_folder(SALARY_FOLDER):
        download_page(file_name)


def city_name(file_name):
    file = file_name.split('/')[1]
    # removes the .html extension
    name = file[:-5]
    return name


def get_files_in_folder(folder, filetype='.html'):
    return glob.glob(os.path.join(folder, '*' + filetype))


def download_page(file_name):
    name = city_name(file_name)
    housing_file = create_housing_path(file_name)
    if not exists(housing_file):
        print name, 'page has not been downloaded'
        get_page(housing_file)

    elif is_captcha(housing_file):
        print name, 'is a captcha page'
        get_page(housing_file)

    else:
        print name, 'is already stored correctly'


def create_housing_path(file_name):
    global HOUSING_FOLDER
    tmp_name = HOUSING_FOLDER + city_name(file_name) + '.html'
    return tmp_name


def exists(file_name):
    return file_name in get_files_in_folder(HOUSING_FOLDER)


def get_page(file_name, sleep_time = 30):
    sleep_time += random.random()*15

    # functionality for acquiring the page
    global HOUSING_FOLDER
    # get the pages
    name = city_name(file_name)
    print 'Downloading', name

    link = 'https://www.zillow.com/'+name+'/home-values/'
    urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

    time.sleep(sleep_time)
    file_name, _ = urllib.urlretrieve(link, HOUSING_FOLDER + name + '.html')
    
    if is_captcha(file_name):
        # if we receive a captcha page, increase the sleep time by a random factor
        # so eventually the captcha will be resolved
        get_page(file_name, sleep_time*(1+random.random()))


# will need more robust check in the future
def is_captcha(file_name):
    with open(file_name) as f:
        return 'captcha' in f.read()


if __name__ == '__main__':
    main()
