from scrappers.shared_attr import title_keywords
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import os


def absolutePath(path=None):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    if path == None:
        return PROJECT_ROOT
    else:
        return PROJECT_ROOT + path

def get_title(title):
    title = title.lower()
    if 'intern' not in title and 'teacher' not in title \
            and 'lecturer' not in title and 'student' not in title \
            and 'professor' not in title:
        for keyword in title_keywords:
            if keyword in title:
                return True
        else:
            return False
    else:
        return False
    


def runChromeOverServer():
    try:
        proxies = '89.238.167.42:3128'
        display = ''
        options = Options()
        options.add_argument(
            f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36')
        # options.add_argument('--proxy-server=%s' % proxies)
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--shm-size=2g')
        options.add_argument('--no-sandbox')
        options.add_argument(
            '--disable-blink-features=AutomationControlled')
        # options.add_argument('--remote-debugging-port=9222')
        while True:
            try:
                driver = webdriver.Chrome(
                    ChromeDriverManager().install(), chrome_options=options)
            except Exception as e:
                print(f"Exception as {e}")
                driver = webdriver.Chrome(executable_path=absolutePath(
                    "/ChromeDrivers/chromedriver-3"), chrome_options=options)
                # driver = webdriver.Chrome(executable_path='chromedriver85',  chrome_options=options)
            break
        print('driver created')
        return driver, display
    except Exception as e:
        traceback.print_exc()
        print('driver while exception')
        return '', ''