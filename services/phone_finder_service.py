from config import settings
import re

class PhoneFinderService():
    def __init__(self,soup_obj,website_url):
        self.soup_obj = soup_obj
        self.website_url = website_url
        self.scrapping_settings = settings['ScrappingSettings']

    def find_phones(self) -> list:
        '''Returns a list of scrapped phones'''
        text_content_list = self.soup_obj.findAll(text=True)
        visible_text_content_list = filter(self.find_visible_text, text_content_list) 
        phones = []
        regex_list = self.scrapping_settings['PhoneRegexList']
        for visible_text_content in visible_text_content_list: 
            splitted_text_content_list = visible_text_content.split(':')
            for splitted_text_content in splitted_text_content_list:
                for regex_item in regex_list:
                    finds = re.findall(
                        regex_item,
                        splitted_text_content
                    )
                    if len(finds)>0:
                        clean_text_content = list(finds[0])
                        if clean_text_content[0]!="":
                            clean_text_content[0] = clean_text_content[0].replace("(","").replace(")","").replace("+","")
                            clean_text_content[0]=f"+({clean_text_content[0]})"
                        clean_text_content = [item for item in clean_text_content if item!=""]
                        clean_text_content = " ".join(clean_text_content)
                        phones.append(clean_text_content)
        phones = list(set(phones))
        if len(phones) == 0:
            return (["NO PHONE FOUND"])        
        return phones

    def find_visible_text(self,bs4_object) -> bool:
        '''Based on the settings, finds all text tags'''
        if bs4_object.parent.name in self.scrapping_settings['PossibleTextParents']:
            return False
        if re.match(r"[\n]+",str(bs4_object)): 
            return False
        return True
                
