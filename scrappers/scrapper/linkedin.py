import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)

import datetime
import time
import traceback
from multiprocessing.pool import ThreadPool
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from scrappers.scraper import Scrapper, in_progress_jobs
from scrappers.shared_attr import posted_date_list, title_keywords
from scrappers.helper import get_title
from shared_layer.logger import logger
from shared_layer.variables import in_progress

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from scrappers.company_url import get_company_url_bing, get_company_url_google, get_company_url_google_updated


# from Scraping.generic_func import get_title, job_category, runChromeOverServer
# from Scraping.keywords import job_keywords, new_keywords
# from Scraping.location import uk_location
# from Scraping.Scrapers import Scrapper




class LinkedIn(Scrapper):  # Inherit from Scrapper
    """Scraping linkedin job leads

    Args:
        - base_url  (str): Base url of the linkedin
        - job_portal (str): Job portal url
        - headers  (str) : Headers need to scrap linkedin
        - remove_companies (list): Do not scrap data of companies present in list
        - tags (list): tags associated with the lead collected with this scrapper
        - delay (int): Delay between next start of scrapper (1st day 12:00) next start after 1380 hours
        - name (str): Name of a scrapper
    """

    def __init__(self):
        super().__init__()
        self.base_url = "https://ca.linkedin.com/jobs"
        self.job_portal = "https://ca.linkedin.com/jobs/search?keywords={}&location=Worldwide&locationId=&geoId=92000000&f_TPR=r86400&distance=100&f_WT=2&position=1&pageNum={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36"
        }
        self.remove_companies = []
        self.tags = [" "]
        self.name = "linkedin"
        self.logger = logger.get_logger(self.name)
        self.lead_collected = 0
        self.leads = []  # It is leads list for bulk insert

    def infinite_scrolling(self, driver, page_no):
        elem = driver.find_element_by_tag_name('body')
        while page_no:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            page_no -= 1

    def runChromeOverServer(self):
        while True:
            try:
                proxies = '206.198.131.172:80'
                display = ''
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-notifications')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--shm-size=2g')
                options.add_argument('--no-sandbox')
                options.add_argument('--remote-debugging-port=9222')
                
                try:
                    driver = webdriver.Chrome(
                        ChromeDriverManager().install(), chrome_options=options)
                except:
                    driver = webdriver.Chrome(
                        executable_path='chromedriver76',  chrome_options=options)
                finally:  
                    driver.set_page_load_timeout(60)
                    return driver, display
            except Exception as e:
                self.logger.error(e)
                break
                

    def get_jobs(self, jobs, scrapped_list):
        """Get New Jobs(leads) and save in the database jobs_leads table

        Args
            - scrapped_list  (list): List of jobs elements
            - country (str): Target Country / Remote
            - company_list  (list) : list of already scraped companies
            - db1 (DataBase): Database instance object to interact with database

        return
            - void

        """

        global insertion
        for job in jobs:
            try:
                job_url = job.find('a', {
                                   "class": "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"})['href']
            except:
                job_url = ''

            if job_url not in scrapped_list:
                try:
                    title = job.find(
                        'span', {'class': 'sr-only'}).text.strip()
                except:
                    title = ''

                try:
                    location = job.find(
                        'span', {'class': 'job-search-card__location'}).text.strip()
                except:
                    location = ''
                try:
                    city = location.split(',')[0]
                except:
                    city = ''
                try:
                    state = location.split(',')[1]
                except:
                    state = ''
                try:
                    company = job.find('a',
                                       class_='hidden-nested-link').text.strip()

                except:
                    company = ''

                try:
                    posted_date = job.find('time').text.strip()
                except:
                    posted_date = ''
                try:
                    if posted_date in posted_date_list or 'today' in posted_date or "hours" in posted_date or "minutes" in posted_date:
                        valid = get_title(title)
                        if valid:
                            self.store_jobs(title, company, city,
                            state, job_url, posted_date,
                            'state', '')

                        else:
                            self.logger.info(f"Invalid job -- {title}")
                    else:
                        self.logger.info(
                            f"Job is {posted_date} older -- {title}")
                except:
                    self.logger.exception("Error Occurred in get_jobs")
                    continue

    def main_code(self):
        """Extract Jobs(leads) against every location

        return
            - void

        """
        driver, display = self.runChromeOverServer()
        driver.maximize_window()
        try:
            for keyword in title_keywords:
                self.logger.info(f'Getting leads for keyword {keyword}')
                end = 2
                page = 0
                while page < end:
                    try:
                        page += 1
                        keyword = keyword.replace(" ", "%20")
                        url = self.job_portal.format(keyword, page)
                        self.logger.info(f"processing url: {url}")

                        driver.get(url)
                        driver.implicitly_wait(10)
                        time.sleep(3)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        all_jobs = soup.findAll(
                            'div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
                        if all_jobs is not None:
                            if len(all_jobs) > 0:
                                self.get_jobs(
                                    all_jobs, self.remove_companies)
                            else:
                                break
                        self.infinite_scrolling(driver, 8)
                    except:
                        self.logger.exception(
                            "Error Occurred in us_main_code - Inner Except"
                        )
                        break
        except:
            self.logger.exception(
                "Error Occurred in us_main_code - Outer Except"
            )
        driver.quit()

    @in_progress_jobs
    def scrap(self, id):
        """Main function

        Args:
            scrapper_id (_type_): _description_
            id (_type_): _description_
        """
        try:
            
            self.logger.info(f" Scrapper Started {self.name}")
            # Getting the starting time
            start_time = time.time()
            # Getting leads in multiprocessing
            self.main_code()
            # Getting time taken by the scrapper to get leads
            time_taken_by_scrapper = (time.time() - start_time) / 60
            # Logging things.
            self.logger.info(f" - leads Collected {self.lead_collected}")
        except Exception as e:
            self.logger.exception(f"Exception Occurred")

        finally:
            self.logger.info(f" - Time Taken {time_taken_by_scrapper} minutes")
            # Updating the scrapper logs
            status, message = self.update_logs_in_db(
                time_taken_by_scrapper, self.lead_collected, id, self.logger
            )


def get_scraper():  # by default None
    """Get the scraper Object

    Returns:
       LinkedIn : Initialize Scraper object and return object
    """
    return LinkedIn()
