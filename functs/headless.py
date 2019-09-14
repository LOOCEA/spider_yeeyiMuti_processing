from selenium import webdriver

def getBrowser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    posC="C:\Download\small App\WebDriver\chromedriver.exe"
    b = webdriver.Chrome(executable_path=posC, options=chrome_options)
    return b

