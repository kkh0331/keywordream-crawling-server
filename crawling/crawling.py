from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def extract_required_data(news_list):
  content_list = []
  for news in news_list:
    detail = news["items"][0]
    news_info = {}
    news_info["title"] = detail["title"]
    news_info["press"] = detail["officeName"]

    news_info["date"] = datetime.strptime(detail["datetime"], '%Y%m%d%H%M')
    news_info["imgUrl"] = detail["imageOriginLink"]
    url = extract_url(detail['officeId'], detail['articleId'])
    news_info["url"] = url
    res_content, db_content = extract_content(url)
    news_info["content"] = db_content
    # TODO 뉴스 DB에 저장
    content_list.append(res_content)
  return content_list

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def each_crawling(code):
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error"# 예외처리
  reauired_news_list = extract_required_data(news_list)
  return reauired_news_list
  
def total_crawling(stockList):
  stock_news = {}
  for stock in stockList:
    stock_news[stock] = each_crawling(stock)
  return stock_news