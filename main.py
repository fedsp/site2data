import setup
from scrapping_service import ScrappingService
import sys


def main(websites):
    for website in websites:
        scrapping_obj = ScrappingService('https://www.google.com')
        print(website)

if __name__=='__main__':
    website_list = []
    for line in sys.stdin:
            website_list.append(line)
    main(website_list)
