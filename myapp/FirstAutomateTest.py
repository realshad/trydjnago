import os
from selenium import webdriver
import pandas as pd
import numpy as np
import time

chromedriver = "C:/venu/chromedriver_win32/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("http://127.0.0.1:8000/PTRCalc/")

data = pd.read_csv("C:/GitDjango/Mybatch1Project/tryjango/myapp/Templates/PTRTestData.csv")
print('data', data)

for index,row in data.iterrows():
    P = driver.find_element_by_id("Price")
    P.clear()
    P.send_keys(row['p'].astype(str))

    T = driver.find_element_by_id("Time")
    T.clear()
    T.send_keys(row['t'].astype(str))

    R = driver.find_element_by_id("Rate")
    R.clear()
    R.send_keys(row['r'].astype(str))

    element = driver.find_element_by_id("Calc")
    element.click()

    print('calc value', driver.find_element_by_id("Calcval").get_attribute('value'))

    #print ('P', P.get_attribute("value"))
    #print('T', T.get_attribute("value"))
    #print('R', R.get_attribute("value"))
    #print('C', C.get_attribute("value"))


driver.quit()