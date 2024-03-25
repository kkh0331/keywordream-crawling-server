from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
import multiprocessing
from multiprocessing import Pool, cpu_count, Manager
from db.insert_news import insert_news
from db.get_content import get_content
from db.check_news_id import check_news_id

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def preprocess_data(detail, stockCode):
  current = multiprocessing.current_process()
  try:
    newsId = detail['articleId']
    
    print("current_process : ", current.name, current._identity)
    title = detail["titleFull"]
    press = detail["officeName"]
    newsDate = datetime.strptime(detail["datetime"], '%Y%m%d%H%M')
    imgUrl = detail["imageOriginLink"]
    originalUrl = extract_url(detail['officeId'], detail['articleId'])
    content = extract_content(originalUrl)
    
    if content is None:
      return None
    
    values = (title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode)
    return values
  except Exception as ex:
    print("데이터 크롤링 오류 : ", ex)
    return None

def each_crawling(code):  
  news_list = naver_news_api(code)
  if(news_list =="Error"): return "Error" # 예외처리
  news_list = [item for news in news_list for item in news['items']]
  newsId_list = [news["articleId"] for news in news_list]
  newsId_DB, content_DB = check_news_id(newsId_list) # DB에 있는 내용 가져옴
  news_list_not_DB = [news for news in news_list if news['articleId'] not in newsId_DB]
  
  num_processes = cpu_count()
  with Pool(num_processes) as pool:
    results = pool.starmap_async(preprocess_data, [(news, code) for news in news_list_not_DB])
    results = results.get()

  insert_news(results)
  
  content_not_DB = [news[3] for news in results]
  total_content = content_not_DB + content_DB;
  total_content = [result for result in total_content if result is not None]
  return total_content