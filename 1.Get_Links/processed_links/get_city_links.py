from google import search, get_random_user_agent
import re
import random
import us
import time


# global value containing state codes so it wont need to be
# created each time we want to use it
state_codes = us.states.mapping('name', 'abbr')

def main():
    # find out current progress
    total_progress = 0
    for line in open('city_links.csv', 'r'):
        total_progress += 1

    for line in open('failures.csv','r'):
        total_progress += 1


    # line buffered open
    f = open('city_links.csv', 'a', 1)
    fail = open('failures.csv', 'a', 1)
    # count will count the number of lines we have already processed
    # so that we can pick up where we left off if the program terminated
    count = 0
    #print total_progress
    for line in open('../all_links/potential_cities.csv','r'):
        # allows program to pick up where it left off
        if count < total_progress:
            count += 1
            continue

        values = line.split(',')
        city = values[0] + ',' + values[1]

        formatted_city = extract_formatted_name(values)
        print formatted_city
        base_link = quick_link(formatted_city)
        if base_link:
            # [ugly]
            f.write(values[0]+','+values[1]+','+values[2].strip()+',' + base_link + '\n')
            f.flush()
        else:
            fail.write(line)
            fail.flush()

        # [ugly]
        count += 1
        total_progress += 1
    f.close()
    fail.close()


def extract_formatted_name(values):
    global state_codes
    # format the name for use in the url
    return values[0].replace(' ', '-') + '-' + state_codes[values[1].decode('utf-8')].encode('utf-8')


def is_result(link, formatted_city):
    # allows for us to find the exact link we are looking for
    # the wildcard in the link represents a hash that payscale uses to prevent
    # people from accessing their data by changing the url
    pre = 'http://www.payscale.com/research/US/Job=Software_Engineer/Salary/ec3cdd66/'
    if link[len(pre):] == formatted_city:
        return True
    return False


def quick_link(formatted_city):
    # search string to get the exact website we want
    q = 'site:payscale.com/research/US/Job=Software_Engineer/Salary/*/' + formatted_city
    try:
        for result in search(q, stop=5, pause=30+random.random()*15, user_agent=get_random_user_agent()):
            if is_result(result, formatted_city):
                return result
    except Exception as e:
        # wait five minutes before rerunning program
        # to get around 503 error when spamming google too often
        time.sleep(60*5)
        return quick_link(formatted_city)
    return None


if __name__ == '__main__':
    main()