from crawling.api import naver_news_api
from crawling.bs4 import extract_content
from datetime import datetime
import multiprocessing
from multiprocessing import Pool, cpu_count
from db.insert_news import insert_news
from db.check_news_id import check_news_id
from db.insert_news_stock import insert_news_stock
import json
import time

def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"

def preprocess_data(news):
  # current = multiprocessing.current_process()
  # startTime = time.time()
  try:
    newsId = news['articleId']
    title = news["titleFull"]
    press = news["officeName"]
    newsDate = datetime.strptime(news["datetime"], '%Y%m%d%H%M')
    imgUrl = news["imageOriginLink"]
    originalUrl = extract_url(news['officeId'], news['articleId'])
    content = extract_content(originalUrl)
    if content is None:
      return None
    values = (title, press, newsDate, content, imgUrl, originalUrl, newsId)
    # endTime = time.time()
    # print(endTime - startTime, " ", news["titleFull"])
    return values
  except Exception as ex:
    print("데이터 크롤링 오류 : ", ex)
    return None
  
def each_crawling(code):
  time0 = time.time()
  news_list = naver_news_api(code)
  if news_list == []: return [] # 예외처리 없을 경우
  news_list = [item for news in news_list for item in news['items']]
  newsId_list = [news["articleId"] for news in news_list]
  newsId_DB, content_DB = check_news_id(newsId_list) # DB에 있는 내용 가져옴
  news_list_not_DB = [news for news in news_list if news['articleId'] not in newsId_DB]
  time1 = time.time()
  print("time1 - time0 : ", time1 - time0)
  # num_processes = cpu_count()
  # with Pool(num_processes) as pool:
  #   results = pool.map_async(preprocess_data, news_list_not_DB)
  #   results = list(filter(None, results.get()))
  results = []
  crawling_newsId = []
  content_not_DB = []
  for news in news_list_not_DB:
    startTime = time.time()
    result = preprocess_data(news)
    if result is not None:
      # print(type(result))
      results.append(result)
      crawling_newsId.append(result[6])
      content_not_DB.append(result[3])
    endTime = time.time()
    print(endTime-startTime, " ", news["titleFull"])
  time2 = time.time()
  print("time2 - time1 : ", time2 - time1)
  crawling_newsId = [result[6] for result in results]
  newsId_list = newsId_DB + crawling_newsId
  newsIds = json.dumps(newsId_list, ensure_ascii=False)
  time3 = time.time()
  print("time3 - time2 : ", time3 - time2)
  insert_news_stock(newsIds, code)
  insert_news(results)
  time4 = time.time()
  print("time4 - time3 : ", time4 - time3)
  content_not_DB = [news[3] for news in results]
  total_content = content_not_DB + content_DB
  # total_content = [result for result in total_content if result is not None]
  return total_content