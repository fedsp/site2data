import dataclasses
import os
from datetime import datetime
import json

@dataclasses.dataclass
class LogItem:
    '''This class stores a single log item'''
    website: str
    message_content: str

class LogRepository():
    def __init__(self):
        self.log_list = []

    def add_new_item(self,item_to_be_added:LogItem)->None:
        '''Adds a new item to the result list'''
        self.log_list.append(dataclasses.asdict(item_to_be_added))

    def save_log(self):
        '''stores the log as a json file at the root of the project'''
        if not os.path.isdir('./log'):
            os.mkdir('log')
        timestamp = str(datetime.now()).replace(" ","").replace(":","").replace("-","").replace(".","")
        with open(f"./log/{timestamp}.json","w") as jsonfile:
            json.dump(self.log_list,jsonfile)

