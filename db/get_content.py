from db.connect import get_db

def get_content(newsId):
    content = None
    
    try:
        cursor = get_db().cursor()
        query = "SELECT content from News WHERE newsId = %s"
        cursor.execute(query, (newsId, ))
        result = cursor.fetchone()
        if result:
            content = result['content']
        cursor.close()
        
    except Exception as e:
        print("접속오류 getContent", e)
        
    return content