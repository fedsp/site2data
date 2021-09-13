from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit, urlunsplit
from logo_finder_service import LogoFinderService
from phone_finder_service import PhoneFinderService
from config import settings
from time import sleep
import traceback

class ScrappingService():
    def __init__(self,website_url,driver):
        self.website_url = website_url
        if self.website_url[-1]=='/':
            self.website_url = self.website_url[:-1]
        split = urlsplit(website_url)
        if split.scheme == "":
            raise Exception(f"Error: {website_url} url without scheme.")
        self.website_url = f"{split.scheme}://{split.netloc}"
        try:
            driver.get(self.website_url)
            self.valid = True
        except(Exception) as err:
            if err.msg[:44]=="unknown error: net::ERR_CONNECTION_TIMED_OUT":
                self.valid = False
                return
            else:
                raise Exception('Unknow error:'+traceback.format_exc())        
        sleep(4)
        self.home_soup_obj = BeautifulSoup(driver.page_source,'html.parser')
        self.contact_url = self.find_contact_page()
        driver.get(self.contact_url)
        sleep(4)
        self.contact_soup_obj = BeautifulSoup(driver.page_source,'html.parser')

    def scrap(self):
        
        logo_seach_obj = LogoFinderService(
            soup_obj=self.home_soup_obj,
            website_url=self.website_url
        )        
        self.logo = logo_seach_obj.find_logo()
        phone_seach_obj = PhoneFinderService(
            soup_obj=self.contact_soup_obj,
            website_url=self.website_url
        )
        self.phones = phone_seach_obj.find_phones()

    def find_contact_page(self)->str:
        '''In case of the page provided is the homepage, it gets the website contacts page'''
        all_links = self.home_soup_obj.find_all('a',href=True)
        contact_text = settings['ScrappingSettings']['ContactIdentifier']
        contact_links = [item for item in all_links if contact_text in item.text.lower()]
        if len(contact_links)<1:
            return self.website_url
        contact_link = contact_links[0]
        contact_url = contact_link.attrs['href']
        if contact_url[0] == '/':
            contact_url = self.website_url+contact_url
        return contact_url