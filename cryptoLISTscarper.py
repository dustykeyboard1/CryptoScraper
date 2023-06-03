"""
Filename: cryptoLISTscraper.py
Author: Michael Scoleri
Date: 06.03.23
Function: Create a list of crypto coins and save to pickle file.
Using BeautifulSoup, parses the current page for all crypto currency tags. 
Then using Selenium, navigates to the next page and repeats 50 times.
"""

# Import necessary libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

def generate_crypto_list():
    # Initialize the crypto_list
    crypto_list = []

    # The URL of the website
    URL = 'https://www.investing.com/crypto/currencies'
    
    # Initialize webdriver and open the URL
    driver = webdriver.Chrome('/Users/michaelscoleri/Downloads/chromedriver_mac_arm64/chromedriver')
    driver.get(URL)

    # Wait up to 10 seconds for the page to load
    wait = WebDriverWait(driver, 10)  

    # Loop to parse through 50 pages
    for i in range(50):
        try:
            # Create a BeautifulSoup object and find the table body
            soup = BeautifulSoup(driver.page_source, 'html.parser')  
            tbody = soup.find('tbody')
            
            # Loop through each row in tbody and append the cryptos to crypto_list
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                new_sticker = cells[3].text
                if new_sticker not in crypto_list:
                    crypto_list.append(cells[3].text)

            # Wait for the "Next" button to become clickable and click it
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/section/div[10]/div[2]/div[2]/div/div[2]/a')))
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            # If the "Next" button is not found on the page, break the loop
            print("ERROR MESSAGE: ", e)
            break
    
    # Quit the driver after parsing the pages
    driver.quit()

    return crypto_list

# Generate the crypto list
crypto_list = generate_crypto_list()

#filter out duplicates 

# Save the list to a pickle file
with open('/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/cryptoList.pkl', 'wb') as f:
    pickle.dump(crypto_list, f)
