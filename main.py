import config
from scrapping_service import ScrappingService
from scrapping_result_repository import ResultRepository,ScrappingResult
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import sys
result_repo = ResultRepository()


def main(website):    
    chrome_options = Options()
    userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
    chrome_options.add_argument(f'user-agent={userAgent}')
    #chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path=config.settings['ChromeDriverBinLocation'],
        options=chrome_options
    )
    scrapping_obj = ScrappingService(
        website_url=website,
        driver=driver)
    if scrapping_obj.valid == False:
        result_repo.add_new_item(
            ScrappingResult(
                website=website,
                phones="SITE NOT FOUND",
                logo="SITE NOT FOUND"
            )
        )
    else:
        scrapping_obj.scrap()
        result_repo.add_new_item(
            ScrappingResult(
                website=website,
                phones=scrapping_obj.phones,
                logo=scrapping_obj.logo
            )
        )

    
def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

def multi_run(website_list):
    multithreading(main, website_list, 20)
    x = ""

if __name__=='__main__':
    website_list = []
    for line in sys.stdin:
        website_list.append(line)
    multithreading(main, website_list, 20)
    x = ""
    #main(website_list)
