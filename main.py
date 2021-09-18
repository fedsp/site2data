from repositories.log_repository import LogItem
import config
from scrapping_service import ScrappingService
from scrapping_result_repository import ResultRepository,ScrappingResult
from log_repository import LogRepository,LogItem
from concurrent.futures import ThreadPoolExecutor
import sys
result_repo = ResultRepository()
log_repo = LogRepository()
import json
import traceback

def main(website):  
    try:
        scrapping_obj = ScrappingService(website_url=website)
        if scrapping_obj.check_if_website_exists == False:
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
    except(Exception) as err:
        result_repo.add_new_item(
                ScrappingResult(
                    website=website,
                    phones="ERROR. SEE LOG FOR DETAILS",
                    logo="ERROR. SEE LOG FOR DETAILS"
                )
        )
        log_repo.add_new_item(
            LogItem(
                    website=website,
                    message_content=str(traceback.format_exc())
                )
        )
        

def multi_threading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

def multi_run(website_list):
    website_list = [item.replace('\n','') for item in website_list]
    multi_threading(main, website_list, config.settings['MaxParallelSessions'])
    log_repo.save_log()
    print("Results: \n")
    json_list = []
    for item in result_repo.result_list:
        dict_to_be_printed = {
            "logo":item.logo,
            "phones":item.phones,
            "website":item.website,
            }
        print(dict_to_be_printed)
    ###############################################################
    #If you want to debug the output as a json uncomment this block
        #json_list.append(dict_to_be_printed)   
    # with open('./result.json','w') as jsonfile:
    #     json.dump(json_list,jsonfile)
    ###############################################################    

if __name__=='__main__':
    website_list = []
    for line in sys.stdin:
        website_list.append(line)
    multi_run(website_list)
