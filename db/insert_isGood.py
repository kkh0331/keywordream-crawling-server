from db.connect import get_db

def insert_isGood(isGood, newsId):
    try:
        cursor = get_db().cursor()
        query = f"UPDATE News SET isGood = {isGood} WHERE newsId = {newsId}"
        cursor.execute(query)
        cursor.close()
        
    except Exception as e:
        print("접속오류", e)