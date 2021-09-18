from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit, urlunsplit
from config import settings
from logo_finder_service import LogoFinderService
from phone_finder_service import PhoneFinderService
from time import sleep
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class ScrappingService():
    def __init__(self, website_url:str) -> None:
        self.website_url = website_url
        if self.website_url[-1] == '/':
            self.website_url = self.website_url[:-1]
        split = urlsplit(website_url)
        if split.scheme == "":
            raise Exception(f"Error: {website_url} url without scheme.")
        self.website_url = f"{split.scheme}://{split.netloc}"

    def check_if_website_exists(self) -> bool:
        '''Simple and fast requests get just to check if the domain returns something.'''
        response = requests.get(self.website_url)
        if 200 <= response.code <= 299:
            return True
        else:
            return False

    def scrap(self) -> None:
        '''Main scrapping orchestrator'''
        self.scrap_using_simple_request()
        if (self.logo == "NO LOGO FOUND") or (self.phones[0] == "NO PHONE FOUND"):
            self.scrap_using_selenium()

    def scrap_using_simple_request(self) -> None:
        '''Initial try to obtain the data. Faster than Selenium, but does not work at dynamic generated js pages'''
        response = requests.get(self.website_url)
        home_soup_obj = BeautifulSoup(response.content, 'html.parser')
        logo_seach_obj = LogoFinderService(
            soup_obj=home_soup_obj,
            website_url=self.website_url
        )
        self.logo = logo_seach_obj.find_logo()

        contact_url = self.find_contact_url(home_soup_obj)
        response = requests.get(contact_url)
        contact_soup_obj = BeautifulSoup(response.content, 'html.parser')
        phone_seach_obj = PhoneFinderService(
            soup_obj=contact_soup_obj,
            website_url=self.website_url
        )
        self.phones = phone_seach_obj.find_phones()

    def scrap_using_selenium(self) -> None:
        '''Slower than scrap_using_simple_request, but works for dynamic js sites'''
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_options.add_argument(
            f'user-agent={settings["ScrappingSettings"]["BrowserUserAgent"]}')
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        #driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.website_url)
        sleep(settings['SleepTimeToLoadJavascript'])
        home_body = driver.find_element_by_tag_name("body")
        home_body = home_body.get_attribute('innerHTML')
        home_soup_obj = BeautifulSoup(home_body, 'html.parser')
        logo_seach_obj = LogoFinderService(
            soup_obj=home_soup_obj,
            website_url=self.website_url
        )
        self.logo = logo_seach_obj.find_logo()

        contact_url = self.find_contact_url(soup_obj=home_soup_obj)
        driver.get(contact_url)
        sleep(settings['SleepTimeToLoadJavascript'])
        contact_body = driver.find_element_by_tag_name("body")
        contact_body = contact_body.get_attribute('innerHTML')
        contact_soup_obj = BeautifulSoup(contact_body, 'html.parser')
        phone_seach_obj = PhoneFinderService(
            soup_obj=contact_soup_obj,
            website_url=self.website_url
        )
        self.phones = phone_seach_obj.find_phones()
        driver.close()
        driver.quit()

    def find_contact_url(self,soup_obj:BeautifulSoup) -> str:
        '''In case of the page provided is the homepage, it gets the website contacts page'''
        all_links = soup_obj.find_all('a', href=True)
        contact_text = settings['ScrappingSettings']['ContactIdentifier']
        contact_links = [
            item for item in all_links if contact_text in item.text.lower()]
        if len(contact_links) < 1:
            return self.website_url
        contact_link = contact_links[0]
        contact_url = contact_link.attrs['href']
        if contact_url[0] == '/':
            contact_url = self.website_url+contact_url
        return contact_url
