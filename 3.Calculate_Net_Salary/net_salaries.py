import time
import random
from bs4 import BeautifulSoup
import requests
import glob
import os



# TODO specify that this file includes rent prices
def main(level_folder='Entry-Level'):
    BASE_FOLDER_NAME = '../2.Get_HTML_Files/'
    RESULTS_FOLDER_NAME = 'Results/'
    with open(RESULTS_FOLDER_NAME + level_folder+'.csv', 'a', 1) as results:
        # could be its own function
        for filename in glob.glob(os.path.join(BASE_FOLDER_NAME + level_folder+'/', '*.html')):
            soup = get_soup_from_file(filename)
            salaries = get_salaries_from_soup(soup)

            formatted_city = filename.split('/')[-1].split('.')[0]
            print level_folder, formatted_city
            rent = get_rent(formatted_city)
            net_salaries = []
            for salary in salaries:
                net_salary = deduct_taxes(salary, formatted_city) - rent
                net_salaries.append(net_salary)



            
            results.write(formatted_city+','+str(rent))
            if len(net_salaries) == 3:
                results.write(',,')
            for salary in net_salaries:
                results.write(','+str(int(salary)))
            if len(net_salaries) == 3:
                results.write(',')
            results.write('\n')

    if level_folder == 'Entry-Level':
        main(level_folder='All_Salaries')
        main(level_folder='Mid-Career')
        main(level_folder='Experienced')
        main(level_folder='Late-Career')


def get_soup_from_file(path):
    f = open(path)
    return BeautifulSoup(f.read(), 'html.parser')


def get_salaries_from_soup(soup):
    #ClEANME       
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

    # avoid spamming the website********
    time.sleep(30+random.random()*15)

    return income_after_tax/12.0



def get_rent(formatted_city):
    HOUSING_FOLDER = '../2.Get_HTML_Files/Housing/'
    filename = HOUSING_FOLDER + formatted_city + '.html'
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        rent = soup.find_all('div', {'class' : 'bar bar-1'})[1].find_all('span', {'class':'bar-value info zsg-fineprint'})[0]
        rent = rent.text.strip().replace('$','').replace(',','')
        return int(rent)



if __name__ == '__main__':
    main()