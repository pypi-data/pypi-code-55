import os
import time
from datetime import datetime as dt # strftime, today
import requests
import json
import pandas as pd
import configparser
import selenium
from bs4 import BeautifulSoup

########GLOBALS########
SCHEMA_jobs = [
    'search',
    # 'Job Number', 
    'Location',
    'Job Title',
    'Company',
    'Salary',
    'Description Simple' 
    ]

# search_terms = [
#     'aerospace+engineer',
#     'electrical+engineer',
#     'mechanical+engineer',
#     'propulsion+engineer',
#     'software+engineer',
#     'test+engineer',
#     'systems+engineer',
#     'manufacturing+engineer',
#     'quality+engineer',
#     'design+engineer',
#     'satellite',
#     'satellite+operator'
#                 ]

with open('search_terms.json', 'r') as file:
    search_terms = json.load(file)

search_terms = search_terms['search terms']

search_term = 'design+engineer'
job_number = 1

########END GLOBALS########

########FUNCTIONS########

def get_browser():
    '''set up webdriver as browser'''
    logger.info('Configuring browser')
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser

def send_request(search_term, num_results_offset):
    base_url = 'https://indeed.com/jobs'

    # payload = {
    #           'q': search_term,
    #           'l': 'United States',
    #           }

    url = (f'{base_url}'
           f'?q={search_term}'
            '&l=United+States&'
           f'start={str(num_results_offset)}') #test

    # print(f'----- PAGE {page_num} -----')

    # request = requests.get(base_url, params=payload) 
    request = requests.get(url) #test

    # print(request.url) #debug

    return request

def process_request(search_term, request, jobs_df):

    soup = BeautifulSoup(request.text, 'html.parser')
    # print(soup.prettify()) #debug

    job_titles = get_job_titles(soup)

    companies = get_company_names(soup)

    locations = get_locations(soup)

    salaries = get_salaries(soup)

    descriptions_simple = get_descriptions_simple(soup)

    # descriptions = get_descriptions(request, fields)

    '''add to jobs df'''
    for  index in range(len(job_titles)):
        try:
            job_row = pd.DataFrame([[
                search_term, 
                # job_number,
                locations[index],
                job_titles[index],
                companies[index],
                salaries[index],
                descriptions_simple[index]
                ]], columns=SCHEMA_jobs)

            jobs_df = jobs_df.append(job_row)
        except IndexError:
            pass

    return jobs_df


def get_job_titles(soup):
    job_titles = []
    for div in soup.find_all(name='div',
                             attrs={'class': 'row'}):
        for a in div.find_all(name='a',
                              attrs={'data-tn-element': 'jobTitle'}):
            job_titles.append(a['title'])

    # print(job_titles) #debug
    # print(len(job_titles)) #debug

    return job_titles

def get_company_names(soup):
    companies = []
    for div in soup.find_all(name='div',
                             attrs={'class': 'row'}):
        company = div.find_all(name='span',
                               attrs={'class': 'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            next_try = div.find_all(name='span',
                                    attrs={'class': 'result-link-source'})
            for span in next_try:
                companies.append(span.text.strip())

    # print(companies) #debug
    # print(len(companies)) #debug

    return companies

def get_locations(soup):
    locations = []
    divs = soup.find_all('div',
                         attrs={'class': 'recJobLoc'})
    for div in divs:
        locations.append(div['data-rc-loc'])

    # print(locations) #debug
    # print(len(locations)) #debug

    return locations

def get_salaries(soup):
    salaries = []
    for div in soup.find_all(name='div',
                             attrs={'class': 'row'}):

        try:
            span = div.find(name='span',
                            attrs={'class': 'salaryText'})
            salaries.append(span.text.strip())
        except:
            salaries.append('none')

    # print(salaries) #debug
    # print(len(salaries)) #debug

    return salaries

def get_descriptions_simple(soup):

    descriptions_simple = []
    divs = soup.find_all('div',
                         attrs={'class': 'summary'})
    for div in divs:
        descriptions_simple.append(div.text.strip())

    # print(descriptions_simple) #debug
    # print(len(descriptions_simple)) #debug
    
    return descriptions_simple

def get_descriptions():
    browser = get_browser()
    browser.get(request.url)

    return descriptions

def clean_data(jobs_data):
    cleaner_data = jobs_data
    cleaner_data['City'], cleaner_data['State'] = \
        cleaner_data['Location'].str.split(',', 1).str

    return(cleaner_data)

########END FUNCTIONS########

'''Creating browser'''
# browser = get_browser()

########MAIN########
def main():

    res_dir = f'{os.path.dirname(os.path.realpath(__file__))}/results'

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    date_today = dt.strftime(dt.today(), '%Y_%m_%d')
    df_list = []

    for term in search_terms:
        jobs_df = pd.DataFrame([], columns=SCHEMA_jobs)
        max_results_offset = 2000
        for num_results_offset in range(0, max_results_offset, 19):
            print('\n' * 5)
            term_readable = term.replace('+', ' ')
            request = send_request(term, num_results_offset)
            jobs_df = process_request(term_readable, request, jobs_df)
            print(f"{term_readable}: {len(jobs_df)} records")
            '''drop duplicates'''
        jobs_df = jobs_df.drop_duplicates()
        jobs_df = clean_data(jobs_df)
        df_list.append(jobs_df)

    all_jobs_df = pd.concat(df_list)

    all_jobs_df.to_csv(f'{res_dir}/{date_today}_indeed_jobs_results.csv',
                       index=False)



########END MAIN########

if __name__ == '__main__':
    main()

