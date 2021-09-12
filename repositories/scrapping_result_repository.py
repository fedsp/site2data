from dataclasses import dataclass

@dataclass
class ScrappingResult:
    '''This class stores a single scrapping result'''
    website: str
    phones: list
    logo: str

class ResultRepository():
    def __init__(self):
        self.result_list = []

    def add_new_item(self,item_to_be_added:object)->None:
        '''Adds a new item to the result list'''
        self.result_list.append(item_to_be_added)

if __name__ == '__main__':
    repo = ResultRepository()
    result1 = ScrappingResult(
        website="www.google.com",
        phones=[123456],
        logo="www.google.com/logo.png"
    )
    repo.add_new_item(result1)
    x = ""