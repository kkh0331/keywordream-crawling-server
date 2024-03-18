from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
from multiprocessing import Pool
from db.insert_news import insertNews
from db.get_content import getContent
from db.check_insert_stock import checkInsertStock

def preprocess_data(news, stockCode):
  try:
    detail = news["items"][0]
    newsCode = detail['articleId']
    content = getContent(newsCode)
    if content != None:
      return content
    press = detail["officeName"]
    newsDate = datetime.strptime(detail["datetime"], '%Y%m%d%H%M')
    imgUrl = detail["imageOriginLink"]
    originalUrl = extract_url(detail['officeId'], detail['articleId'])
    title, content = extract_content(originalUrl)
    
    # db에 저장
    insertNews(title, press, newsDate, content, imgUrl, originalUrl, newsCode, stockCode)
  
    return content
  except Exception as ex:
    print("데이터 크롤링 오류 : ", ex)
    pass

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def each_crawling(name, code):
  checkInsertStock(name, code)
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error"# 예외처리
  num_processes = 4
  with Pool(num_processes) as pool:
    results = pool.starmap(preprocess_data, [(news, code) for news in news_list])
  return results
  
# def total_crawling(stockList):
#   stock_news = {}
#   for stock in stockList:
#     stock_news[stock] = each_crawling(stock)
#   return stock_news