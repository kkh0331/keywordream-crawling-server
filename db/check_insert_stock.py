from db.connect import get_db

def check_insert_stock(name, code):
    try:
        cursor = get_db().cursor()
        query = "SELECT * FROM Stock WHERE stockCode = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        
        if result is None:
            query = "INSERT INTO Stock (stockCode, name) VALUES (%s, %s)"
            cursor.execute(query, (code, name))
            print(f"stockCode {code} Stock Table에 추가 완료")
        else:
            print(f"stockCode {code} 이미 존재함")
        cursor.close()
        return True
    
    except Exception as e:
        print("접속오류", e)
        return False