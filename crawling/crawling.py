from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
from multiprocessing import Pool
from bs4 import BeautifulSoup

def preprocess_data(news):
  try:
    detail = news["items"][0]
    news_info = {}
    news_info["title"] = detail["title"]
    news_info["press"] = detail["officeName"]

    news_info["date"] = datetime.strptime(detail["datetime"], '%Y%m%d%H%M')
    news_info["imgUrl"] = detail["imageOriginLink"]
    url = extract_url(detail['officeId'], detail['articleId'])
    news_info["url"] = url
    content = extract_content(url)
    news_info["content"] = content
    # TODO 뉴스 DB에 저장
    return content
  except:
    print("데이터 크롤링 오류")
    pass

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def each_crawling(code):
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error"# 예외처리
  num_processes = 4
  with Pool(num_processes) as pool:
    results = pool.map(preprocess_data, news_list)
  return results
  
def total_crawling(stockList):
  stock_news = {}
  for stock in stockList:
    stock_news[stock] = each_crawling(stock)
  return stock_news