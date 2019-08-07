from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin
import time

browser = webdriver.Chrome()
browser.get('https://sports.163.com/nba/')
wait = WebDriverWait(browser, 10)

browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(3)
count = 5
while count:
    try:
        load_more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="load_more_btn"]')))
        ActionChains(browser).click(load_more_btn).perform()
        time.sleep(1)
        count -= 1
    except:
        break
titles = []
lists = browser.find_elements(By.CSS_SELECTOR, 'div.ndi_main > div.data_row.news_article.clearfix')
for l in lists:
    titles.append(l.find_element(By.CSS_SELECTOR, 'div > div.news_title > h3 > a').text)

with open('titles.txt', 'a') as f:
    for title in titles:
        f.write(title)
        f.write('\n')
time.sleep(5)
browser.close()