from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

url_base = 'https://wdwpassport.com/wait-times/'
# park, ride index, final hour
parks = [['magic-kingdom', 24, 22], ['epcot', 12, 21], ['hollywood-studios', 12, 21], ['animal-kingdom', 10, 20]]

# Finds the ride name and wait time
def ride(n):
    name_xpath = '//*[@id="app"]/div/div/ul/li['+str(n)+']/h3'
    time_xpath = '//*[@id="app"]/div/div/ul/li['+str(n)+']/div[1]/div/div'
    ride_name = driver.find_element_by_xpath(name_xpath)
    ride_time = driver.find_element_by_xpath(time_xpath)
    return ride_name.text, ride_time.text

# Checks if the ride is down
def check_ride_down(n):
    try:
        down_xpath = '//*[@id="app"]/div/div/ul/li['+str(n)+']/div[1]/div[1]/div'
        driver.find_element_by_xpath(down_xpath)
    except NoSuchElementException:
        return False
    return True

# Collects the wait times 
def collect_times(url_base=url_base, parks=parks):
    wait_list = []
    for park in parks:
        if int(datetime.now().strftime("%H")) < park[2]:
            url = url_base + park[0]
            driver.get(url)
            time.sleep(1)
            for n in range(2, park[1]):
                if check_ride_down(n) == True:
                    a = ride(n)
                    wait_list+=[[date.today().strftime("%m/%d/%Y"),
                                 datetime.now().strftime("%H:%M"), 
                                 park[0], 
                                 a[0], 
                                 a[1]]]
    return wait_list
    
def update_file():
    df_new = pd.DataFrame(np.array(collect_times()), columns=['date', 'time', 'park', 'ride', 'wait'])
    df_old = pd.read_csv('wait_time.csv')
    df_combine = pd.concat([df_old, df_new])
    df_combine.to_csv(index=False, path_or_buf='wait_time.csv', mode='w+')
    
while int(datetime.now().strftime("%H")) < 22:
    if int(datetime.now().strftime("%M")) % 5 == 0:
        update_file()
        time.sleep(295)