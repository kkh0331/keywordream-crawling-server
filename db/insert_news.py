from db.connect import get_db

def insert_news(news_list):
    
    try:
        cursor = get_db().cursor()
        query = "INSERT INTO News (title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(query, news_list)
        cursor.close()
        
    except Exception as e:
        print("접속오류", e)