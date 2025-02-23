from flask import abort
from database.connect import get_database

def find_stock_by_code(code):
  try:
    cursor = get_database().cursor()
    query = "SELECT code, name FROM stocks WHERE code = %s"
    cursor.execute(query, (code,))
    result = cursor.fetchone()
    return result
  except Exception as e:
    print("find_stock_by_code(code)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()
    
def update_recent_news_count_by_code(code, recent_news_count):
  try:
    cursor = get_database().cursor()
    query = f"UPDATE stocks SET recent_news_count = %s WHERE code = %s"
    cursor.execute(query, (recent_news_count, code))
  except Exception as e:
    print("update_recent_news_count_by_code(code, recent_news_count)에서 데이터베이스 서버 에러")
    abort(500, description="데이터베이스 서버 에러")
  finally:
    cursor.close()