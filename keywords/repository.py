from database.connect import get_database
from flask import abort

def save_news_keywords(tags, news_id):
  # tags : [(word, cnt), ...]
  try:
    cursor = get_database().cursor()
    query = "INSERT INTO news_keywords (keyword, count, news_id) VALUES (%s, %s, %s)"
    tags_news_id = [(word, cnt, news_id) for word, cnt in tags]
    cursor.executemany(query, tags_news_id)
    get_database().commit()
  except:
    print(f"save_news_keywords(tags)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()