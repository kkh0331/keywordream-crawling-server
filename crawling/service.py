from client.naver_api import naver_news_crawling_by_code, naver_news_content_crawling
from crawling.repository import find_news_ids_by_news_ids_in, save_news_list, find_news_ids_by_code_and_news_ids_in, save_news_stocks
from datetime import datetime

def news_list_crawling_by_code(code): # 주식 코드로 뉴스 크롤링
  crawled_news_list = naver_news_crawling_by_code(code)
  news_list = [item for news in crawled_news_list for item in news['items']]
  news_ids = [news["articleId"] for news in news_list]
  news_ids_in_news_db = find_news_ids_by_news_ids_in(news_ids)
  news_list_not_in_news_db = [news for news in news_list if news['articleId'] not in news_ids_in_news_db]
  preprocessed_news_list_not_in_news_db = preprocess_news_list(news_list_not_in_news_db)
  save_news_list(preprocessed_news_list_not_in_news_db)
  # news_stock 저장하게 되는데...
  # news_ids_in_news_db와 preprocessed_news_ids_not_in_news_db(preprocessed_news_list_not_in_news_db에서 추출)
  # => news_ids 추출
  # => news_ids와 code을 이용해서 news_stock에 저장한다
  preprocessed_news_ids_not_in_news_db = [preprocessed_news_not_in_news_db["news_id"] for preprocessed_news_not_in_news_db in preprocessed_news_list_not_in_news_db]
  final_news_ids = news_ids_in_news_db + preprocessed_news_ids_not_in_news_db
  news_ids_in_news_stocks_db = find_news_ids_by_code_and_news_ids_in(code, final_news_ids)
  news_ids_not_in_news_stocks_db = [news_id for news_id in final_news_ids if news_id not in news_ids_in_news_stocks_db]
  save_news_stocks(code, news_ids_not_in_news_stocks_db)
  return preprocessed_news_list_not_in_news_db, len(final_news_ids)

def preprocess_news_list(news_list):
  preprecessed_news_list = []
  for news in news_list:
    preprocessed_news = preprocess_news(news)
    if preprocessed_news is not None:
      preprecessed_news_list.append(preprocessed_news)
      print("[크롤링 완료] ", preprocessed_news["title"])
  return preprecessed_news_list

def preprocess_news(news):
  try:
    news_id = news['articleId']
    title = news["titleFull"]
    press = news["officeName"]
    news_date = datetime.strptime(news["datetime"], '%Y%m%d%H%M')
    img_url = news["imageOriginLink"]
    original_url = extract_url(news['officeId'], news['articleId'])
    content = naver_news_content_crawling(original_url)
    if content is None:
      return None
    return {
      "title" : title,
      "press" : press,
      "news_date" : news_date,
      "content" : content,
      "img_url" : img_url,
      "original_url" : original_url,
      "news_id" : news_id
    }
  except Exception as e:
    print("데이터 크롤링 오류 : ", e)
    return None
  
def extract_url(officeId, articleId):
  return f"https://n.news.naver.com/article/{officeId}/{articleId}"