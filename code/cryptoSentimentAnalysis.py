"""
Filename: cryptoSentimentAnalysis.py
Author: Michael Scoleri
Date: 06.03.23
Scrape the internet for cryptoCurrency articles and use 
ML for Sentiement analysis
"""

# Importing required libraries
import pickle
import pandas as pd
import reticker
from textblob import TextBlob
import requests 
import re
from bs4 import BeautifulSoup 
from newsapi import NewsApiClient

# ---- Functions for web scraping and data extraction ----

# Function to get news articles related to volatile cryptocurrency
def find_raw_articles():
    api = NewsApiClient(api_key='51f442a4fab8401ca0e0bc020ee6ae90')
    sources = api.get_everything(q='volatile cryptocurrency')
    return sources

# Function to create list of URLs from the sources 
def create_url_list(book1):
    url_list = []
    articles = book1['articles']
    for item in articles:
        if item not in url_list:
            url_list.append(item['url'])
    print(len(url_list))
    return url_list

# Function to get the HTML content of a given URL
def get_html(my_url):
    article = ''
    response = requests.request(url = my_url, method="GET")
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.find_all('p'):
        article = article + item.text
    return article

# ---- Functions for ticker identification ----

def identify_tickers(text_list):
    # Load data from a pickle file
    with open('/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/cryptoList.pkl', 'rb') as f:
        cryptoList = pickle.load(f)

    ticker_list = []
    for text in text_list:
        tick = reticker.TickerExtractor().extract(text)
        for item in tick:
            if item in cryptoList:
                match = re.search(item, text)
                pair = []
                start = match.start() - 500
                end = match.end() + 500
                if start < 0:
                    start = 0

                if end > len(text) - 1:
                    end = -1
                chunk = text[start:end]
                pair.append(text[match.start():match.end()])
                pair.append(chunk)
                ticker_list.append(pair)
    return ticker_list

def create_new_list(list):
    text_list = []
    match_list = []
    for item in list:
        text_list.append(item[1])
        match_list.append(item[0])
    return text_list, match_list

# ---- Functions for sentiment analysis ----

def perform_sentiment_analysis(list_of_strings, tickers):
    sentiment_scores = []
    for text, ticker in zip(list_of_strings, tickers):
        # Get the sentiment of the text
        blob = TextBlob(text)
        sentiment = blob.sentiment

        sentiment_scores.append({
            'ticker' : ticker,
            'text': text,
            'polarity': sentiment.polarity,  # Polarity: -1 means negative, 0 means neutral, +1 means positive
            'subjectivity': sentiment.subjectivity,  # Subjectivity: 0.0 is very objective, 1.0 is very subjective
        })
    
    return sentiment_scores

def sentiment_scores_to_excel(sentiment_scores, filename):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(sentiment_scores)

    # Write the DataFrame to an Excel file
    df.to_excel(filename, index=False)

# ---- Main function to call all the defined functions ----

def main():
    # Find raw articles
    dict1 = find_raw_articles()

    # Create list of article URLs
    url_list = create_url_list(dict1)

    # Get HTML content of each URL
    text_list = [get_html(item) for item in url_list]

    # Identify tickers in the texts
    poss_ticker = identify_tickers(text_list)

    # Create new lists for text and matching tickers
    string_list, match_list = create_new_list(poss_ticker)

    # Perform sentiment analysis
    sentiment_score_dictionary = perform_sentiment_analysis(string_list, match_list)

    # Export sentiment scores to an Excel file
    sentiment_scores_to_excel(sentiment_score_dictionary, '/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/Excel Sheet/cryptoResults.xlsx')

# Call the main function
main()
