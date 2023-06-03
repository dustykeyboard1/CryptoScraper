from bs4 import BeautifulSoup
import requests as regs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

def generate_crypto_list():
    crypto_list = []

    URL = 'https://www.investing.com/crypto/currencies'
    driver = webdriver.Chrome('/Users/michaelscoleri/Downloads/chromedriver_mac_arm64/chromedriver')
    driver.get(URL)

    # Wait up to 10 seconds for the page to load
    wait = WebDriverWait(driver, 10)  # This line was missing in your script

    for i in range(50):
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')  # Use Selenium's driver.page_source instead of a new request
            tbody = soup.find('tbody')
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                guide_text = cells[3].text
                if guide_text == '':
                    crypto_list.append(cells[1].text)
                else:
                    crypto_list.append(guide_text)


           # Wait for the "Next" button to become clickable
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/section/div[10]/div[2]/div[2]/div/div[2]/a')))

            # Use execute_script to click the "Next" button
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            print("ERRPR MESSAGE: ", e)
            # If the "Load More" button is not found on the page, break the loop
            break

    
    driver.quit()
    return crypto_list
crypto_list = generate_crypto_list()
with open('/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/cryptoList.pkl', 'wb') as f:
    pickle.dump(crypto_list, f)

