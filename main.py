from requests import *
from datetime import *
import os
from twilio.rest import Client

account_sid = os.getenv('sid')
auth_token = os.getenv('auth')
company_symbol = 'TSLA'
company_name = 'TESLA'
stock_parameters = {
    'apikey': os.getenv('apikey'),
    'function': 'TIME_SERIES_DAILY',
    'symbol': company_symbol,

}
url = f'https://www.alphavantage.co/query'
r = get(url, params=stock_parameters)
r.raise_for_status()
stock_data = r.json()
stock_data_list = [i for i in stock_data['Time Series (Daily)']][:2]
closing_prices = [stock_data['Time Series (Daily)'][i]['4. close'] for i in stock_data_list]
difference = round(float(closing_prices[0]) - float(closing_prices[1]), 2)
print(closing_prices)
print(difference)
news_parameters = {
    'apikey': os.getenv('news_apikey'),
    'q': company_name,
    'language': 'en',
}
news = get('https://newsapi.org/v2/top-headlines', params=news_parameters)
news.raise_for_status()
news_json = news.json()
news_articles = [{
    'title': i['title'],
    'description': i['description'],
    'link': i['url']
} for i in news_json['articles']]
print(news_articles)


def send_price_margin():
    percentage = round((difference/float(closing_prices[0]))*100,2)
    if difference < 0:
        return f'🔻{percentage}'
    elif difference == 0:
        return f'👀{percentage}'
    else:
        return f'🔺{percentage}🤑'


def send_news():
    final_news = ''
    for i in news_articles:
        title = i['title']
        desc = i['description']
        link = i['link']
        final_news += f'Headline:{title}\nMore Info:{desc}\nNews Link:{link}\n'
    return final_news


client = Client(account_sid, auth_token)
message = client.messages \
    .create(
    body=f'Company Name : {company_name}\nStock Percentage :{send_price_margin()}\n{send_news()}',
    from_='+17055351044',
    to='+17097250935'
)
