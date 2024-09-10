from database.connect import get_database
from flask import abort

def find_news_ids_by_news_ids_in(news_ids):
  try:
    cursor = get_database().cursor()
    query = "SELECT id FROM news WHERE id IN %s"
    cursor.execute(query, (tuple(news_ids),))
    result = cursor.fetchall()
    return [str(item['id']).zfill(10) for item in result]
  except:
    print(f"find_by_news_ids_not_in(news_ids)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()

def save_news_list(news_list):
  try:
    cursor = get_database().cursor()
    query = "INSERT INTO news (id, title, press, created_at, content, img_url, origin_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    formatted_news_list = [
      (
        news["news_id"],
        news["title"],
        news["press"],
        news["news_date"],
        news["content"],
        news["img_url"],
        news["original_url"]
      )
      for news in news_list
    ]
    cursor.executemany(query, formatted_news_list)
    get_database().commit()
  except Exception as e:
    print(f"save_news_list(news_list)에서 데이터베이스 서버 에러 - ", e)
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()
    
def find_news_ids_by_code_and_news_ids_in(code, news_ids):
  try:
    cursor = get_database().cursor()
    news_ids_codes = [(news_id, code) for news_id in news_ids]
    query = "SELECT news_id FROM news_stocks WHERE (news_id, stock_code) IN %s"
    cursor.execute(query, (news_ids_codes,))
    result = cursor.fetchall()
    return [str(item['news_id']).zfill(10) for item in result]
  except:
    print(f"find_news_ids_by_code_and_news_ids_in(code, news_ids)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()
    
def save_news_stocks(code, news_ids):
  try:
    cursor = get_database().cursor()
    news_ids_codes = [(news_id, code) for news_id in news_ids]
    query = "INSERT INTO news_stocks (news_id, stock_code) VALUES (%s, %s)"
    cursor.executemany(query, news_ids_codes)
    get_database().commit()
  except:
    print(f"save_news_stocks(code, news_ids)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()