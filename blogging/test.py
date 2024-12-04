from newsapi import NewsApiClient # type: ignore

# Init
newsapi = NewsApiClient(api_key='183da19345114658a34ecc68dd92ff82')

# /v2/everything
all_articles = newsapi.get_top_headlines(q='general')

# /v2/top-headlines/sources
sources = newsapi.get_sources()

print(sources)