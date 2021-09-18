#########################
import sys
import os 
path = os.getcwd()
sys.path.insert(0, path)
#########################
import json

def test_main():
    from main import multi_run
    with open ('./test/websites_test.txt') as test_data:
        site_list = test_data.readlines()    
    multi_run(site_list)
    with open ('./test/result_template.json') as result_template_file:
        result_template = json.load(result_template_file)  
    with open ('./result.json') as actual_result_file:
        result = json.load(actual_result_file)  
    assert result_template == result

if __name__ == '__main__':
    test_main()

