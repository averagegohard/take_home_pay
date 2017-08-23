import time
import random
from bs4 import BeautifulSoup
import requests
import glob
import os


def main(level_folder='Entry-Level'):
    BASE_FOLDER_NAME = '../2.Get_HTML_Files/'
    RESULTS_FOLDER_NAME = 'Taxed_Results/'

    results_filename = RESULTS_FOLDER_NAME + level_folder+'.csv'
    cities_directory = BASE_FOLDER_NAME + level_folder+'/'

    # open the results file once so we don't need to open it for each stackframe
    # created in write_results
    with open(results_filename, 'a+r', 1) as res_file:

        # reading the file also moves the file pointer to EOF, a space efficient
        # implementation could just reset the file pointer instead
        processed_data = res_file.read()

        for filename in get_files_in_folder(cities_directory):
            formatted_city = city_name(filename)

            # more robust check (regex) may be necessary (St. Louis fucking dammit)
            if formatted_city not in processed_data:
                print 'Processing', level_folder, formatted_city
                salaries = get_salaries(filename, formatted_city)
                write_results(salaries, res_file, formatted_city)
            else:
                print level_folder, formatted_city, 'already processed'

        # lazy solution, but it works
        recursive_calls(level_folder)


def city_name(file_name):
    file = file_name.split('/')[3]
    # removes the .html extension
    name = file[:-5]
    return name


def recursive_calls(level_folder):
    if level_folder == 'Entry-Level':
        main(level_folder='All_Salaries')
        main(level_folder='Mid-Career')
        main(level_folder='Experienced')
        main(level_folder='Late-Career')


def write_results(salaries, res_file, formatted_city):
    res_file.write(formatted_city)
    if len(salaries) == 3:
        res_file.write(',,')

    for salary in salaries:
        res_file.write(','+str(int(salary)))

    if len(salaries) == 3:
        res_file.write(',')

    res_file.write('\n')



def get_salaries(filename, formatted_city):
    soup = get_soup_from_file(filename)
    salaries = get_salaries_from_soup(soup)

    net_salaries = []
    for salary in salaries:
        net_salary = deduct_taxes(salary, formatted_city)
        net_salaries.append(net_salary)
    return net_salaries


def get_files_in_folder(folder, filetype='.html'):
    return glob.glob(os.path.join(folder, '*' + filetype))


def get_soup_from_file(path):
    f = open(path)
    return BeautifulSoup(f.read(), 'html.parser')


def get_salaries_from_soup(soup):
    #CLEANME       
    salaries = soup.findAll("div", { "class" : "results-salary"})
    salaries = salaries[0]
    chart = salaries.find_all("div", { "class" : "ticker"})
    chart = chart[1:]
    length = len(chart)
    salaries = []
    for i in range(length/2):
        salary_string = chart[i].text.strip().encode('utf-8')
        salary = salary_string.replace('$','').replace("K","000")
        salaries.append(salary)
    return salaries


def deduct_taxes(salary, formatted_city):
    # HONESTLY HOW DOES THIS WORK???
    cookies = {
        '_sa_orig_ex': '1UltVGfbfaONCs3sXK5ZOhQyb1wTTxhqN1gbBgdopBMVhwW1oqoCf5qCHg537RF8',
        '_sa_lt': 'KetVAVdA2u0Wr8cxZe3AC1vrWrtodXGF',
        '_sa_pt': '1S5V7HolV2LKnn1xkAzgupSZNCCWcwRn8P3o5XzAD6lgfSSRoast7JvLzqlOQcZI',
        '_sa_st': 'BDenPcZHZnVhxxo39Fz0zhou',
        '_sa_st_w_studentloancalculator': 'YxxJNsGnPJb0cRlFiV89qt6R',
        '_sa_st_w_mortgagerefinancerates': 'Tug9ZMSVDGfick3gJmtK6FVb',
    }

    headers = {
        'Origin': 'https://smartasset.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Referer': 'https://smartasset.com/taxes/income-taxes',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Save-Data': 'on',
        'DNT': '1',
    }

    params = (
        ('render', 'json'),
        ('', ''),
    )


    location = formatted_city.replace('-',' ')
    location = 'CITY|' + location[:-3]+'|'+location[-2:]
    data = [
      ('ud-current-location', location),
      ('ud-it-household-income', salary)

    ]

    r = requests.post('https://smartasset.com/taxes/income-taxes', headers=headers, params=params, cookies=cookies, data=data)
    ret_json = r.json()
    income_after_tax = ret_json['page_data']['incomeAfterTax']

    # avoid spamming the website
    time.sleep(2+random.random()*5)

    return income_after_tax/12.0


if __name__ == '__main__':
    main()