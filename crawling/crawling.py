from crawling.api import naver_news_api

def extract_link(news_list):
  link_list = []
  for news in news_list:
    link_list.append(news["link"])
  return link_list

def each_crawling(name, code):
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error"# 예외처리
  # start_urls = extract_link(news_list)
  
  return news_list
  
  
def total_crawling(stockList):
  # for stock in stockList:
  #   each_crawling(stock['name'], stock['code'])
  return each_crawling(stockList[0]['name'], stockList[0]['code'])