from db.connect import get_db

def insert_news(title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode):
    values = (title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode)
    
    try:
        # print("DB 연결 성공")
        cursor = get_db().cursor()
        query = "INSERT INTO News (title, press, newsDate, content, imgUrl, originalUrl, newsId, stockCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        cursor.close()
        
    except Exception as e:
        print("접속오류", e)