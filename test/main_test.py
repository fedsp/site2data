#########################
import sys
import os 
path = os.getcwd()
sys.path.insert(0, path)
#########################


def main_test():
    from main import multi_run
    with open ('./test/websites_test.txt') as test_data:
        site_list = test_data.readlines()
        site_list = [item.replace('\n','') for item in site_list]
    multi_run(site_list)
    assert 5 == 5

if __name__ == '__main__':
    main_test()