#  yeeyi rent information scraper(outdated)
 
 
---
 

## Description
This Python project is designed to scrape and analyze rental information from 'yeeyi.com'. The main objective is to gather rental information, such as rental type, room type, rent price, house type, and address, among other details. It then inserts this information into a table for later use.
>   * use **selenium to simulate browser behavior** in order to hide the DDoS attack detection from cloudflare and get index page source code and detail page source code(through multiprocessing)

>  * use **bs4 and regular expression** to process page source codes and collect entity data which saves in sqlite database 

> * PS: I also  calculate  the distance between my school and rent addresses through google map(using selenium)
## Installation
This project requires the following Python libraries:
- bs4 (BeautifulSoup)
- re (Regular Expressions)
- time
- datetime
- selenium
- multiprocessing
- threading
- traceback

To install these libraries, use the following pip command:
```
pip install beautifulsoup4 selenium datetime multiprocessing traceback
```

## Usage

``` 
1.change chrome or firefox webdriver address(functs.headless.py)

2.create a sqlite table in 'functs' folder according to functs.rent_inf.py

3.run main.py
```


## Contributing
Please feel free to fork this repository, make amendments, and create pull requests.

## Credits
This project utilizes the BeautifulSoup and Selenium libraries for web scraping, as well as several other standard Python libraries.

## License
Include your license information here, if applicable.

--- 

