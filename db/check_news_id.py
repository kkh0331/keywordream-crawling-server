from db.connect import get_db

def check_news_id(newsId_list):
    try:
        cursor = get_db().cursor()
        newsId_list_str = ', '.join(newsId_list)
        query = f"SELECT newsId, content FROM News WHERE newsId in ({newsId_list_str})"
        cursor.execute(query)
        result = cursor.fetchall()
        newsId_DB = [str(item['newsId']).zfill(10) for item in result]
        content_DB = [item['content'] for item in result]
        cursor.close()
        return newsId_DB, content_DB
    
    except Exception as e:
        print("접속오류", e)
        return []