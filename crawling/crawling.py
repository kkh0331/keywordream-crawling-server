from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
import multiprocessing
from multiprocessing import Pool, cpu_count
from db.insert_news import insert_news
from db.get_content import get_content

def preprocess_data(news, stockCode):
  current = multiprocessing.current_process()
  try:
    detail = news["items"][0]
    newsId = detail['articleId']
    content = get_content(newsId)
    
    if content is not None:
      print("[DB]current_process : ", current.name, current._identity)
      return content
    
    print("current_process : ", current.name, current._identity)
    title = detail["titleFull"]
    press = detail["officeName"]
    newsDate = datetime.strptime(detail["datetime"], '%Y%m%d%H%M')
    imgUrl = detail["imageOriginLink"]
    originalUrl = extract_url(detail['officeId'], detail['articleId'])
    content = extract_content(originalUrl)
    
    if content is None:
      return None
    
    # db에 저장
    insert_news(title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode)
    return content
  except Exception as ex:
    print("데이터 크롤링 오류 : ", ex)
    return None

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def each_crawling(code):  
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error" # 예외처리
  num_processes = cpu_count()
  with Pool(num_processes) as pool:
    results = pool.starmap_async(preprocess_data, [(news, code) for news in news_list])
    results = results.get()
  results = [result for result in results if result is not None]
  return results