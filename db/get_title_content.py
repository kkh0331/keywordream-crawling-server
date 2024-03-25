from db.connect import get_db

def get_title_content(newsId):
    try:
        cursor = get_db().cursor()
        query = f"SELECT title, content, isGood FROM News WHERE newsId = {newsId}"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    except Exception as e:
        print("접속오류", e)
        return []