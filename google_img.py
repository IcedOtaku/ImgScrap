from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
from bs4 import BeautifulSoup as bs
import re
import os


google_url_part1 = 'https://www.google.com/search?q='
google_url_part2 = '&source=lnms&tbm=isch'
search_query = '停车'  
location_driver = 'C:/Users/HR/AppData/Local/Google/Chrome/Application/chromedriver.exe'
url = google_url_part1 + search_query + google_url_part2
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)
driver.maximize_window()
driver.get(url)
img_url_dic = {}
count = 0
target_num = 3
pos = 0
for i in range(1): 
    pos = i * 500  
    js = "document.documentElement.scrollTop=%d" % pos
    driver.execute_script(js)
    time.sleep(1)
    html_page = driver.page_source
    soup = bs(html_page, "html.parser")
    img_list = soup.findAll('img', {'class': 'rg_ic rg_i'})
    for img_url in img_list:
        try:
            print(count, end=' ')
            if img_url['src'] not in img_url_dic:
                target = '{}.jpg'.format(count)
                img_url_dic[img_url['src']] = ''
                urllib.request.urlretrieve(img_url['src'], target)
                count = count + 1
                if count == target_num:
                    break
        except KeyError:
            continue
    if count == target_num:
        driver.close()

