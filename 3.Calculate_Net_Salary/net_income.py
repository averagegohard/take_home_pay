from bs4 import BeautifulSoup

def main(level_folder='Entry-Level'):
	post_tax_results_file = 'Taxed_Results/' + level_folder + '.csv'
	net_income_file = 'Net_Income/' + level_folder + '.csv'

	with open(post_tax_results_file, 'r') as res_file:
		with open(net_income_file, 'w') as net_file:
			for line in res_file:
				data = line.strip().split(',')

				formatted_city = data[0]
				rent = get_rent(formatted_city)

				write_results(data[1:], net_file, formatted_city, rent)



        # lazy solution, but it works
        recursive_calls(level_folder)



def write_results(salaries, res_file, formatted_city, rent):
    res_file.write(formatted_city)

    for salary in salaries:
        res_file.write(',')
        if salary != '0':
            res_file.write(str(int(salary) - rent))

    res_file.write('\n')


def city_name(file_name):
    file = file_name.split('/')[1]
    # removes the .html extension
    name = file[:-5]
    return name


def get_rent(formatted_city):
    # hard code some outliers with different formatting
    # this is probably because I used random user agents so the page returned is different
    # depending on the user agent used
    if formatted_city == 'Santa-Barbara-CA':
        return 4050
    elif formatted_city == 'Tucson-AZ':
        return 764
    elif formatted_city == 'Logan-UT':
        return 1146
    elif formatted_city == 'San-Luis-Obispo-CA':
        return 2381
    elif formatted_city == 'Tysons-Corner-VA':
        return 3744
    elif formatted_city == 'Burlington-VT':
        return 1801
    elif formatted_city == 'Johnstown-PA':
        # monthly mortgage payment, no rent info available
        return 1394
    else:
        HOUSING_FOLDER = '../2.Get_HTML_Files/Housing/'
        filename = HOUSING_FOLDER + formatted_city + '.html'

        with open(filename, 'r') as f:
            print filename,
            soup = BeautifulSoup(f.read(), 'html.parser')
            soup = soup.find_all('div', {'class' : 'bar bar-1'})[-1]
            rent = soup.find_all('span', {'class':'bar-value info zsg-fineprint'})[0]
            rent = rent.text.strip().replace('$','').replace(',','')
            print rent
            return int(rent)


def recursive_calls(level_folder):
    if level_folder == 'Entry-Level':
        main(level_folder='All_Salaries')
        main(level_folder='Mid-Career')
        main(level_folder='Experienced')
        main(level_folder='Late-Career')


if __name__ == '__main__':
	main()