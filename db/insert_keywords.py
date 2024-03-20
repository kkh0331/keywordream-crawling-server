from db.connect import get_db

def insert_keywords(data, stockCode):
    values = (data, stockCode)
    try:
        cursor = get_db().cursor()
        query = "SELECT * FROM Keyword WHERE stockCode = %s"
        cursor.execute(query, (stockCode, ))
        result = cursor.fetchone()
        
        if result is None:
            print("keyword 새로 db에 삽입")
            query = "INSERT INTO Keyword (data, stockCode) VALUES (%s, %s)"
        else:
            print("keyword 업데이트")
            query = "UPDATE Keyword SET data = %s WHERE stockCode = %s"
        cursor.execute(query, values)
        cursor.close()
        return True
    
    except Exception as e:
        print("접속오류", e)
        return False