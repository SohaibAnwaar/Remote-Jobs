import time
import traceback
import requests
from bs4 import BeautifulSoup
def company_url_main(company):
    if company != None:
        # time.sleep(1)
        try:
            CompanyUrl = get_company_url_google_updated(company)
            if CompanyUrl == None or CompanyUrl == '':
                CompanyUrl = get_company_url_bing(company)
        except:
            CompanyUrl = None
        return CompanyUrl

def get_company_url_bing(name):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    url = 'https://www.bing.com/search?q={}&form=QBLH&sp=-1&pq=&sc=0-0&qs=n&sk=&cvid=31EB454614E0442BA696F4F0C44E3327'.format(name)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.findAll('div', class_='b_attribution')
    for single_link in links:
        link = single_link.cite.text.strip()
        # print(link)
        if 'wikipedia' not in link and 'facebook' not in link \
                and 'youtube' not in link and 'linkedin' not in link \
                and 'twitter' not in link and 'play.google' not in link \
                and '#' not in link and 'www.bloomberg.com' not in link and \
                "imdb" not in link and "dictionary" not in link and "dnb.com" not in link\
                and "thesaurus.com" not in link:
            return link

def get_company_url_google(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    url ='https://www.google.com/search?source=hp&ei=eZtPX7bHBYejULfdDQ&q={}&oq={}&gs_lcp=CgZwc3ktYWIQAzICCAAyCAguEMcBEK8BMgIIADICCAAyAggAMggILhDHARCvATICCAAyAggAMgIIADICCAA6BwghEAoQoAE6DggAEOoCELQCEJoBEOUCUO0HWOUtYJkwaAJwAHgAgAGRAogB4wWSAQMyLTOYAQCgAQKgAQGqAQdnd3Mtd2l6sAEG&sclient=psy-ab&ved=0ahUKEwj259Gwx8rrAhWHERQKHbduAwAQ4dUDCAc&uact=5'.format(name, name)
    # print(url)
    r = requests.get(url, headers=headers)
    # time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')
    # ol = soup.find('ol', id='b_results')
    link = soup.findAll('div', class_="g")[1:]
    for single_li in link:
        try:
            # linkedin_link = single_li.find('h2')
            # print(linkedin_link)
            try:
                company_name = single_li.find('a')['href']
                # print(company_name)
                if 'wikipedia' not in company_name and 'facebook' not in company_name \
                        and 'youtube' not in company_name and 'linkedin' not in company_name \
                        and 'twitter' not in company_name and 'play.google' not in company_name \
                        and '#' not in company_name and 'www.bloomberg.com' not in company_name \
                        and "imdb" not in company_name and "dictionary" not in company_name \
                        and "dnb.com" not in company_name and "thesaurus.com" not in company_name:
                        return company_name
                    # pass
            except:
                traceback.print_exc()
                company_name = None
        except:
            pass
def get_company_url_google_updated(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    url ='https://www.google.com/search?source=hp&ei=eZtPX7bHBYejULfdDQ&q={}&oq={}&gs_lcp=CgZwc3ktYWIQAzICCAAyCAguEMcBEK8BMgIIADICCAAyAggAMggILhDHARCvATICCAAyAggAMgIIADICCAA6BwghEAoQoAE6DggAEOoCELQCEJoBEOUCUO0HWOUtYJkwaAJwAHgAgAGRAogB4wWSAQMyLTOYAQCgAQKgAQGqAQdnd3Mtd2l6sAEG&sclient=psy-ab&ved=0ahUKEwj259Gwx8rrAhWHERQKHbduAwAQ4dUDCAc&uact=5'.format(name, name)
    # print(url)
    r = requests.get(url, headers=headers)
    # time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')
    # ol = soup.find('ol', id='b_results')
    try:
        company_name = soup.find('div', {'class':'QqG1Sd'}).a['href']
        if 'wikipedia' not in company_name and 'facebook' not in company_name \
                and 'youtube' not in company_name and 'linkedin' not in company_name \
                and 'twitter' not in company_name and 'play.google' not in company_name \
                and '#' not in company_name and 'www.bloomberg.com' not in company_name and \
                "imdb" not in company_name and "dictionary" not in company_name and "dnb.com" not in company_name \
                and "thesaurus.com" not in company_name:
            if '.com' in company_name:
                return company_name
            else:
                print(0 / 0)
    except:
        try:
            company_name = soup.find('a', {'class':'B1uW2d ellip PZPZlf'})['href']
            if 'wikipedia' not in company_name and 'facebook' not in company_name \
                    and 'youtube' not in company_name and 'linkedin' not in company_name \
                    and 'twitter' not in company_name and 'play.google' not in company_name \
                    and '#' not in company_name and 'www.bloomberg.com' not in company_name and \
                    "imdb" not in company_name and "dictionary" not in company_name \
                    and "dnb.com" not in company_name and "thesaurus.com" not in company_name:
                if '.com' in company_name:
                    return company_name
                else:
                    print(0 / 0)
        except:
            link = soup.findAll('div', class_="g")
            for single_li in link:
                    try:
                        # linkedin_link = single_li.find('h2')
                        # print(linkedin_link)
                        try:
                            company_name = single_li.find('a')['href']
                            if 'wikipedia' not in company_name and 'facebook' not in company_name \
                                    and 'youtube' not in company_name and 'linkedin' not in company_name \
                                    and 'twitter' not in company_name and 'play.google' not in company_name \
                                    and '#' not in company_name and 'www.bloomberg.com' not in company_name and \
                                    "imdb" not in company_name and "dictionary" not in company_name \
                                    and "dnb.com" not in company_name and "thesaurus.com" not in company_name:
                                return company_name
                            # pass
                        except:
                            traceback.print_exc()
                            company_name = None
                    except:
                        traceback.print_exc()
                        company_name = None
