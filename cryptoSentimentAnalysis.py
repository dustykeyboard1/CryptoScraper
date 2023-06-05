import pickle
import requests as regs 
import datetime
from bs4 import BeautifulSoup 
from newsapi import NewsApiClient


with open('/Users/michaelscoleri/Desktop/NitroTrading/Coding/Sentiment Analysis/cryptoList.pkl', 'rb') as f:
    loaded_list = pickle.load(f)

def find_raw_articles():
    api = NewsApiClient(api_key='51f442a4fab8401ca0e0bc020ee6ae90')
    sources = api.get_everything(q='cryptocurrency')
    return regs.get(sources).json()

    # domains_string = 'hello'
    # todays_date = datetime.datetime.today()
    # todays_date_formatted = todays_date.strftime ('20%y-%m-%d')
    # todays_date_formatted = str(todays_date_formatted)
    # url1 = ('https://newsapi.org/v2/everything?'
    #     'q=cryptocurrency&'
    #     f'from={todays_date_formatted}&'
    #     'sortBy=relevancy&'
    #     'domains=marketwatch.com,investing.com,seekingalpha.com,fool.co.uk,ino.com/blog,moneycontrol.com,news.alphastreet.com,equitymaster.com,indiainfoline.com/markets/news,stocksnewsfeed.com,ragingbull.com,scanz.com/blog,wsj.com,nytimes.com'
    #     'page=1&'
    #     'apiKey=51f442a4fab8401ca0e0bc020ee6ae90')

    # url2 = ('https://newsapi.org/v2/everything?'
    #     'q=cryptocurrency&'
    #     'domains=marketwatch.com,investing.com,seekingalpha.com,fool.co.uk,ino.com/blog,moneycontrol.com,news.alphastreet.com,equitymaster.com,indiainfoline.com/markets/news,stocksnewsfeed.com,ragingbull.com,scanz.com/blog,wsj.com,nytimes.com'
    #     f'from={todays_date_formatted}&'
    #     'sortBy=relevancy&'
    #     'page=2&'
    #     'apiKey=51f442a4fab8401ca0e0bc020ee6ae90')

    # url3 = ('https://newsapi.org/v2/everything?'
    #     'q=cryptocurrency&'
    #     'domains=marketwatch.com,investing.com,seekingalpha.com,fool.co.uk,ino.com/blog,moneycontrol.com,news.alphastreet.com,equitymaster.com,indiainfoline.com/markets/news,stocksnewsfeed.com,ragingbull.com,scanz.com/blog,wsj.com,nytimes.com'
    #     f'from={todays_date_formatted}&'
    #     'sortBy=relevancy&'
    #     'page=3&'
    #     'apiKey=51f442a4fab8401ca0e0bc020ee6ae90')

    # url4 = ('https://newsapi.org/v2/everything?'
    #     'q=cryptocurrency&'
    #     'domains=marketwatch.com,investing.com,seekingalpha.com,fool.co.uk,ino.com/blog,moneycontrol.com,news.alphastreet.com,equitymaster.com,indiainfoline.com/markets/news,stocksnewsfeed.com,ragingbull.com,scanz.com/blog,wsj.com,nytimes.com'
    #     f'from={todays_date_formatted}&'
    #     'sortBy=relevancy&'
    #     'page=4&'
    #     'apiKey=51f442a4fab8401ca0e0bc020ee6ae90')

    # url5 = ('https://newsapi.org/v2/everything?'
    #     'q=cryptocurrency&'
    #     'domains=marketwatch.com,investing.com,seekingalpha.com,fool.co.uk,ino.com/blog,moneycontrol.com,news.alphastreet.com,equitymaster.com,indiainfoline.com/markets/news,stocksnewsfeed.com,ragingbull.com,scanz.com/blog,wsj.com,nytimes.com'
    #     f'from={todays_date_formatted}&'
    #     'sortBy=relevancy&'
    #     'page=5&'
    #     'apiKey=51f442a4fab8401ca0e0bc020ee6ae90')

    # response1 = regs.get(url1)
    # response2 = regs.get(url2)
    # response3 = regs.get(url3)
    # response4 = regs.get(url4)
    # response5 = regs.get(url5)

    #return response1.json(), response2.json(), response3.json(), response4.json(), response5.json()

def create_url_list(book1, book2, book3, book4, book5):
    url_list = []
    articles = book1['articles'] + book2['articles'] + book3['articles'] + book4['articles'] + book5['articles']
    for item in articles:
        if item not in url_list:
            url_list.append(item['url'])
    print(len(url_list))
    return url_list

def get_html(my_url):
    article = ''
    response = regs.request(my_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for item in soup.find_all('p'):
        article = article + item.text
    return article


def main():
    dict1 = find_raw_articles()
    # dict1, dict2, dict3, dict4, dict5 = find_raw_articles()
    url_list = create_url_list(dict1)
    # text_list = [get_html(item) for item in url_list]
    # print(text_list[0])

main()