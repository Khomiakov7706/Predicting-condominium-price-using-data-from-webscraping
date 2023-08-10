# -*- coding: utf-8 -*-

# Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import pandas as pd
import pickle as pk

# Create an 'instance' of the driver.
# A new Chrome (or other browser) window should open up if options.headless = False (default)
# Create an 'instance' of the driver.
# A new Chrome (or other browser) window should open up if options.headless = False (default)
CHROMEDRIVER_PATH = "./_chromedriver/chromedriver.exe"
options = Options()
#options.add_argument('--headless')
#options.add_argument(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(options=options)

# Enter the main page, all condos in Phuket are grouped by district.
url ='https://www.hipflat.co.th/en/thailand-projects/condo/phuket-pu'
driver.get(url)
#assert "Phuket" in driver.title

# Write function to scrape all links from the webpage.
# Write function to scrape all links from the webpage.
def get_all_links(driver):
    links = []
    elements = driver.find_elements(By.CLASS_NAME, 'directories__lists-element-name')
    for elem in elements:
        #print(elem.get_attribute("outerHTML"))
        href = elem.get_attribute("href")
        links.append(href)  
    return links


# Run and store the links in district_links
start_time = datetime.now() 
district_links=get_all_links(driver)
time_elapsed = datetime.now() - start_time 
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))

# Check the length of 'district_links', there are 50 districts in Phuket. 
print('districs number:\t', str(len(district_links)))

# Re-run the function to retrive all condo links in each district.
# Append to condo_links.
start_time = datetime.now()
condo_links=[]
for district in district_links:
    print(len(condo_links),district)
#implicitly_wait - Specifies the amount of time the driver should wait 
#when searching for an element if it is not immediately present.
    driver.implicitly_wait(10)
    driver.get(district)
    links = get_all_links(driver)
    print(links)
    condo_links.append(get_all_links(driver))
    time_elapsed = datetime.now() - start_time 
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
print("completed")

# Now we got lists within a list (nested list)
# Turn a (nested) python list into a single list, that contains all the elements of sub lists
# Named as 'condo_links_all'

from itertools import chain
condo_links_all=list(chain.from_iterable(condo_links))
print("Total condo listings = "+str(len(condo_links_all)))
# Result in 2566 condo listings

# Dump the retrived links to text file.
with open("condo_links_all.txt", "w") as f:
    for s in condo_links_all:
        f.write(str(s) +"\n")
print("completed")


