from db.connect import get_db

def check_news_id(newsId_list):
    print(newsId_list)
    try:
        cursor = get_db().cursor()
        newsId_list_str = ', '.join(newsId_list)
        print("newsId_list_str : ", newsId_list_str)
        query = f"SELECT newsId, content FROM News WHERE newsId in ({newsId_list_str})"
        cursor.execute(query)
        result = cursor.fetchall()
        print("reuslt : ", result)
        newsId_DB = [str(item['newsId']).zfill(10) for item in result]
        print("newsId : ", newsId_DB)
        content_DB = [item['content'] for item in result]
        # print(content_DB)
        cursor.close()
        return newsId_DB, content_DB
    
    except Exception as e:
        print("check_news_id 접속오류", e)
        return []