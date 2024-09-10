from flask import abort
from database.connect import get_database

def find_title_content_by_news_id(news_id):
  try:
    cursor = get_database().cursor()
    query = "SELECT title, content, is_good FROM news WHERE id = %s"
    cursor.execute(query, (news_id,))
    result = cursor.fetchone()
    return result
  except:
    print("find_title_content_by_news_id(news_id)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()
    
def update_is_good_by_news_id(is_good, news_id):
  try:
    cursor = get_database().cursor()
    query = "UPDATE news SET is_good = %s WHERE id = %s"
    cursor.execute(query, (is_good, news_id,))
    cursor.close()
  except:
    print("update_is_good_by_news_id(is_good, news_id)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()