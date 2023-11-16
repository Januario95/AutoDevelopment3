from selenium import webdriver


def initiate_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    
    driver = webdriver.Chrome('C:/Users/a248433/Documents/drivers/chromedriver106v.exe',
                    options=options)
    driver.maximize_window()
    return driver



