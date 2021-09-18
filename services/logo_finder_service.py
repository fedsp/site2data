from config import settings
import re

class LogoFinderService():
    def __init__(self,soup_obj,website_url):
        self.soup_obj = soup_obj
        self.website_url = website_url
        self.scrapping_settings = settings['ScrappingSettings']

    def find_logo(self) -> str:
        '''returns a list of scrapped logo full paths'''
        image_objects = self.soup_obj.find_all('img')
        logos = []
        for image in image_objects:
            image_address = image.get('src')
            if image_address != None:
                if self.scrapping_settings['LogoTextIdentifier'] in image_address.lower():
                    logos.append(image_address)
            if 'class' in image.attrs:
                classnames = image.attrs['class']
                for classname in classnames:
                    if self.scrapping_settings['LogoTextIdentifier'] in classname.lower():
                        logos.append(image_address)
                
        if len(logos) == 0:
            return "NO LOGO FOUND"            
        logo = logos[0]
        regex_item = settings['ScrappingSettings']['AbsoluteVsRelativeRegexChecker']
        logo_relative_or_absolute = re.findall(regex_item,logo)
        if len(logo_relative_or_absolute) == 0:
            logo = self.website_url+logo
        if len(logos) >1:
            print(f'More than one logo found for:{self.website_url}. The first one was chosen arbitrary.')
            logo = f"AMBIGUOUS LOGO: {logo}"
        return logo