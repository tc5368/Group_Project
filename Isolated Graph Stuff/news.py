from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='0f58067ab2ad447ba8e4af81ecea25c5')

# /v2/top-headlines
news = newsapi.get_everything(q='NVDA',language='en',sort_by='relevancy')
#top_headlines = top_headlines['articles']
if news['totalResults'] > 0 and news['status'] == 'ok':
    article = news['articles'][0]
    for i in article:
        print(i)
else:
    print("Couldn't find any news")
