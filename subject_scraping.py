from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import math
import argparse
from webdriver_manager.chrome import ChromeDriverManager
import time 

def wait_for_page(driver,elem_id,delay=3):
    try:
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'ctl00_Content_grdResultPlans')))
        print("Page is ready")
    except TimeoutException:
        print("Timeout: page is not ready")


# process the course table 
def init_subject_dict():

    fp = open("subjects.data","r+");
    lines = fp.readlines()
    if len(lines) == 0:

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
        driver.get('https://sws.unimelb.edu.au/2019/')

        timetable = driver.find_element_by_id('LinkBtn_modules')
        timetable.click()
        wait_for_page(driver,"pObject")
# now we can do something 
        table = driver.find_element_by_id('pObject')
        # table header index mapping  
        subjects = {}
        # look at each sub
        subs_arr = table.find_elements_by_tag_name('option')
        # go through each row
        for s in subs_arr:
            data = s.text.split(' - ')
            sub = (data[0].split('/'))[0]
            print("sub: {}".format(sub),end="\r")
            subjects[sub] = []
            fp.write(sub+"\n")
    else:
        subs_arr = lines
        fp.close()
        for s in lines:
            subjects[s] = []
    return subjects

subjects = init_subject_dict()
print(len(subjects))
