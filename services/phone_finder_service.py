from config import settings
import re

class PhoneFinderService():
    def __init__(self,soup_obj,website_url):
        self.soup_obj = soup_obj
        self.website_url = website_url
        self.scrapping_settings = settings['ScrappingSettings']

    def find_phones(self):
        
        text_content_list = self.soup_obj.findAll(text=True)
        visible_text_content_list = filter(self.find_visible_text, text_content_list) 
        phones = []
        regex_list = self.scrapping_settings['PhoneRegexList']
        for visible_text_content in visible_text_content_list:   
            for regex_item in regex_list:
                finds = re.findall(
                    regex_item,
                    visible_text_content
                )
            if len(finds)>0:
                phones.append(visible_text_content)
        phones = list(set(phones))
        if len(phones) == 0:
            return (["NO PHONE FOUND"])        
        return phones

    def find_visible_text(self,bs4_object):
        if bs4_object.parent.name in self.scrapping_settings['PossibleTextParents']:
            return False
        if re.match(r"[\n]+",str(bs4_object)): 
            return False
        return True
                
