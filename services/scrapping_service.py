from bs4 import BeautifulSoup
import requests

class ScrappingService():
    def __init__(self,website_url):
        site_response = requests.get(website_url)
        self.soup_obj = BeautifulSoup(site_response.content,'html.parser')
        x = ""