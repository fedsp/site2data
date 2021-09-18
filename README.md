# site2data
## webscrapping tool

**site2data** is a Selenium/Chrome/Python based webscrapping tool. The initial goal of this tool is: For a given website list, find out the site logo and phone numbers.
### Wow the scrapping works:
1. Multiple threads are executed in parallel, one for each site (the max number of simultaneous workes are pre-configured)
2. For each run, it will:
2.1 Access the home page, independent if a specific url path is informed 
2.3 Obtain the logo picture
2.2 Scrap the home to find a 'contact us' or similar page
2.3 Obtain the 'contact us' page link
2.4 Scrap the 'contact us' page looking for phone numbers based on a series of regex statements
3. If any step from 2.1 to 2.4 fails, repeat the same but using a selenium webdriver instead of a simple http request
4. Prints the result on the screen
5. Logs the run (errors, if any) as a json file on the ./log folder


## Installation
Run the following command to mount your container

```sh
docker build . -t site2data
```
Run the container passing the stdin input
Windows:
```sh
type C:\Pathtomyfile\websites_test.txt | docker run -i  site2data
```
Linux:
```sh
cat C:\Pathtomyfile\websites_test.txt | docker run -i  site2data
```

## How to use

Load your content (it could be a txt file containing one website per line) and run the docker image.

```sh
cat websites.txt | docker run 123
```

## Unit Test

There is a small yet functional test data to run the application end to end. 
All unit tests can be executed running the command 

```sh
pytest
```

## Known technical debts

* _On scrapping_service, on scrap_using_selenium_: Instead of a simple sleep(X), create a actual routine that checks if the browser already loaded javascript. If not, wait a small fixed amount of time and try again.