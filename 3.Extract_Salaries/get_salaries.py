
def get_salaries_from_soup(soup):
    #FIXME       
    salaries = soup.find_all("div", { "class" : "results-salary"})
    salaries = salaries[0]
    chart = salaries.find_all("div", { "class" : "ticker"})
    chart = chart[1:]
    length = len(chart)
    salaries = {}
    for i in range(length/2):
        salaries[chart[i+length/2].text.strip()] = chart[i].text.strip()
    return salaries


def deduct_taxes(salary, city_name, state):
    sleep()
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

    def format_city(city_name, state):
        return 'CITY|'+city_name.replace(' ','-')+'|'+state

    location = format_city(city_name, state)


    data = [
      ('ud-current-location', location),
      ('ud-it-household-income', salary)

    ]

    r = requests.post('https://smartasset.com/taxes/income-taxes', headers=headers, params=params, cookies=cookies, data=data)
    ret_json = r.json()
    income_after_tax = ret_json['page_data']['incomeAfterTax']
    return income_after_tax/12.0

