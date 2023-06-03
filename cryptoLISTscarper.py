from bs4 import BeautifulSoup
import requests as regs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_crypto_list():
    URL = 'https://coinmarketcap.com/all/views/all/'
    driver = webdriver.Chrome('/Users/michaelscoleri/Downloads/chromedriver_mac_arm64/chromedriver')
    driver.get(URL)

    # Wait up to 10 seconds for the page to load
    wait = WebDriverWait(driver, 10)  # This line was missing in your script

    for i in range(3):
        try:
            # Wait for the "Load More" button to become clickable
            load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[1]/div/div[3]/button')))
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            load_more_button.click()
        except Exception as e:
            print("ERRPR MESSAGE: ", e)
            # If the "Load More" button is not found on the page, break the loop
            break

    crypto_list = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Use Selenium's driver.page_source instead of a new request
    tbody = soup.find('tbody')
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        guide_text = cells[2].text
        if guide_text == '':
            crypto_list.append(cells[1].text)
        else:
            crypto_list.append(guide_text)
    return crypto_list

print(generate_crypto_list())
