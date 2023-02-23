"""Glassdoor scraper."""
import os
import sys
import time
from multiprocessing.pool import ThreadPool
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from scrappers.scraper import Scrapper
from scrappers.shared_attr import posted_date_list, title_keywords
from scrappers.helper import get_title
from shared_layer.logger import logger



class Glassdoor(Scrapper):  # Inherit from Scrapper
    """Scraping Glassdoor job leads

    Args:
        - base_url  (str): Base url of the Glassdoor
        - job_portal (str): Job portal url
        - headers  (str) : Headers need to scrap Glassdoor
        - remove_companies (list): Do not scrap data of companies present in list
        - tags (list): tags associated with the lead collected with this scrapper
        - delay (int): Delay between next start of scrapper (1st day 12:00) next start after 1380 hours
        - name (str): Name of a scrapper
    """

    def __init__(self):
        super().__init__()
        self.glassdoor_url_list = [
            [
                "https://www.glassdoor.com/Job/us-{}-jobs-SRCH_IL.0,2_IN1_KO3,13_IP{}.htm?fromAge=1&radius=25",
                "United States",
            ],
            [
                "https://www.glassdoor.com/Job/australia-{}-jobs-SRCH_IL.0,9_IN16_KO10,13_IP{}.htm?fromAge=1&radius=25",
                "Australia",
            ],
            [
                "https://www.glassdoor.com/Job/indonesia-{}-jobs-SRCH_IL.0,9_IN113_KO10,27_IP{}.htm?fromAge=1",
                "Indonesia",
            ],
            [
                "https://www.glassdoor.com/Job/dubai-{}-jobs-SRCH_IL.0,5_IC2204498_KO6,12.htm?fromAge=3",
                "Dubai",
            ],
            [
                "https://www.glassdoor.com/Job/bahrain-{}-jobs-SRCH_IL.0,7_IN21_KO8,11.htm?fromAge=3",
                "Bahrain",
            ],
            [
                "https://www.glassdoor.com/Job/qatar-{}-jobs-SRCH_IL.0,5_IN199_KO6,9.htm?fromAge=3",
                "Qatar",
            ],
            [
                "https://www.glassdoor.com/Job/malaysia-{}-jobs-SRCH_IL.0,8_IN170_KO9,26_IP{}.htm?fromAge=1",
                "Malaysia",
            ],
            [
                "https://www.glassdoor.com/Job/new-zealand-{}-jobs-SRCH_IL.0,11_IN186_KO12,29_IP{}.htm?fromAge=1",
                "New Zealand",
            ],
            [
                "https://www.glassdoor.com/Job/singapore-{}-jobs-SRCH_IL.0,9_IC3235921_KO10,27_IP{}.htm?fromAge=1",
                "Singapore",
            ],
            [
                'https://www.glassdoor.com/Job/vietnam-{}-jobs-SRCH_IL.0,7_IN251_KO8,25_IP{}.htm?fromAge=1',
                'Vietnam',
            ],
            [
                'https://www.glassdoor.com/Job/thailand-{}-jobs-SRCH_IL.0,8_IN229_KO9,16_IP{}.htm?fromAge=1',
                'Thailand',
            ],
            [
                "https://www.glassdoor.com/Job/united-arab-emirates-{}-jobs-SRCH_IL.0,20_IN6_KO21,38_IP{}.htm?fromAge=1",
                "United Arab Emirates",
            ],
            [
                "https://www.glassdoor.com/Job/saudi-arabia-{}-jobs-SRCH_IL.0,12_IN207_KO13,16_IP{}.htm?fromAge=1",
                "Saudi Arabia",
            ],
            [
                "https://www.glassdoor.com/Emploi/france-{}-emplois-SRCH_IL.0,6_IN86_KO7,10_IP{}.htm?fromAge=1",
                "France",
            ],
            [
                "https://www.glassdoor.com/Job/germany-{}-jobs-SRCH_IL.0,7_IN96_KO8,25_IP{}.htm?fromAge=1",
                "Germany",
            ],
            [
                "https://www.glassdoor.com/Job/hungary-{}-jobs-SRCH_IL.0,7_IN111_KO8,21_IP{}.htm?fromAge=1",
                "Hungary",
            ],
            [
                "https://www.glassdoor.com/Job/switzerland-{}-jobs-SRCH_IL.0,11_IN226_KO12,25_IP{}.htm?fromAge=1",
                "Switzerland",
            ],
            [
                "https://www.glassdoor.com/Job/sweden-{}-jobs-SRCH_IL.0,6_IN223_KO7,20_IP{}.htm?fromAge=1",
                "Sweden",
            ],
            [
                "https://www.glassdoor.com/Job/denmark-{}-jobs-SRCH_IL.0,7_IN63_KO8,14_IP{}.htm?fromAge=1",
                "Denmark",
            ],
            [
                "https://www.glassdoor.com/Empleo/spain-{}-empleos-SRCH_IL.0,5_IN219_KO6,19_IP{}.htm?fromAge=1",
                "Spain",
            ],
        ]
        self.base_url = "https://www.glassdoor.com/"
        self.job_portal = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36"
        }
        self.remove_companies = []
        self.tags = []
        self.name = "glassdoor.com"
        self.logger = logger.get_logger(self.name)
        self.lead_collected = 0

    def __del__(self):
        """Calling destructor for deleting db object when object is destroyed

        Returns:
            SuperClass : Calls super class desctructor
        """
        self.logger.info(f"Closing {self.name} db Object")
        return super().__del__()

    

    def get_jobs(self, job_collection, country):
        """Get New Jobs(leads) and save in the database jobs_leads table

        Args
            - job_collection  (list): List of jobs elements
            - country (str): Target Country / Remote
            - company_list  (list) : list of already scraped companies
            - db1 (DataBase): Database instance object to interact with database

        return
            - void

        """
        for job in job_collection:

            try:
                job_container = job.findAll("div")[1]
            except:
                job_container = job.find("div", class_="jobContainer")
            try:
                company = job_container.find("a").text.strip()
            except:
                company = None

            try:
                job_url = job_container.find("a")["href"]
                job_url = urljoin(self.base_url, job_url)
            except:
                job_url = None

            try:
                title = job_container.findAll("a")[1].text.strip()
            except:
                title = None
            try:
                location = job_container.find(
                    "div", class_="jobInfoItem empLoc flex-wrap"
                ).span.text.strip()
            except:
                try:
                    location = job_container.find(
                        "div", class_="d-flex flex-wrap css-11d3uq0 e1rrn5ka1"
                    ).span.text.strip()
                except:
                    location = None
            try:
                city = location.split(",")[0]
            except:
                city = location
            
            try:
                description = job_container.find("div", id="JobDescriptionContainer"
                ).text.strip()
            except:
                description = ""
            try:
                state = location.split(",")[1]
            except:
                state = None
            try:
                posted_date = job_container.find(
                    "div", {"data-test": "job-age"}
                ).text.strip()
            except:
                posted_date = None

            if posted_date in posted_date_list \
                    and company is not None \
                    and company not in self.remove_companies:
                
                # Getting Description
                r = requests.get(job_url, headers=self.headers)
                soup = BeautifulSoup(r.text, "html.parser")
                try:
                    description = soup.find("div", id="JobDescriptionContainer"
                    ).get_text(separator="\n").strip()
                except:
                    description = ""

                self.store_jobs(title, company, city,
                                  state, job_url, posted_date,
                                   country, description)

    def main_code(self, url_list):
        """Extract Jobs(leads) against every glassdoor_url

        Args
            - url_list  (list): List of glassdoor links with region ---(keywords.py - glassdoor_url_list)

        return
            - void

        """
        
        for glassdoor_url in url_list[:2]:
            # This page_url is incomplete and needs formatting down.
            page_url = glassdoor_url[0]
            region = glassdoor_url[1]

            for keyword in title_keywords:
                self.logger.info(f"Scrapping keyword {keyword}")
                keyword = keyword.replace(" ", "-")
                try:
                    pg = 0
                    end = self.page_limit
                    while pg < end:
                        pg += 1
                        # Format the page_url
                        url = page_url.format(keyword, pg)
                        self.logger.info(f"url: {url}")
                        r = requests.get(url, headers=self.headers)
                        
                        if r.status_code != 200:
                            self.logger.info(f"Status Code: {r.status_code}")
                            break

                        time.sleep(2)
                        soup = BeautifulSoup(r.text, "html.parser")
                        try:
                            article = soup.find(
                                "article", id="MainCol").find("ul")
                            job_collection = article.findAll("li")
                            if len(job_collection) != 0:
                                self.get_jobs(
                                    job_collection, region
                                )
                            else:
                                break
                        except:
                            self.logger.exception(
                                "Error Occurred in main_code - Inner Except"
                            )
                            break

                except Exception as e:
                    self.logger.exception(
                        f"Error Occurred in main_code - Outer Except {e}")
                    continue

    def scrap(self, row_id):
        """Main function

        Args:
            scrapper_id (_type_): _description_
            id (_type_): _description_
        """
        try:
            id = row_id
            # Getting the starting time
            start_time = time.time()
            self.main_code(self.glassdoor_url_list)
            # Getting time taken by the scrapper to get leads
            time_taken_by_scrapper = (time.time() - start_time) // 60
            # Logging things.
            self.logger.info(f" - leads Collected {self.lead_collected}")
        except Exception as e:
            self.logger.exception(f"Error Occured {self.name}")
            self.logger.info(f" - leads Collected {self.lead_collected}")
            time_taken_by_scrapper = 0
            
        finally:
            self.logger.info(f" - Time Taken {time_taken_by_scrapper} minutes")
            # Updating the scrapper logs
            status, message = self.update_logs_in_db(
                time_taken_by_scrapper, self.lead_collected, id, self.logger
            )


def get_scraper():  # by default None
    """Get the scraper Object

    Returns:
       GlassDoor : Initialize Scraper object and return object
    """
    return Glassdoor()
