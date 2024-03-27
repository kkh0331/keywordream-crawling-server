from db.connect import get_db

def insert_news_stock(data, stockCode):
    values = (data, stockCode)
    try:
        cursor = get_db().cursor()
        query = "SELECT * FROM NewsStock WHERE stockCode = %s"
        cursor.execute(query, (stockCode, ))
        result = cursor.fetchone()
        
        if result is None:
            print("NewsStock 새로 db에 삽입")
            query = "INSERT INTO NewsStock (newsIds, stockCode) VALUES (%s, %s)"
        else:
            print("NewsStock 업데이트")
            query = "UPDATE NewsStock SET newsIds = %s WHERE stockCode = %s"
        cursor.execute(query, values)
        cursor.close()
    
    except Exception as e:
        print("insert_news_stock에서 접속오류 : ", e)