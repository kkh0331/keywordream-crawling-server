from db.connect import connect_mariaDB, disconnect_mariaDB

def checkInsertStock(name, code):
    connection = None
    try:
        connection = connect_mariaDB()
        # print("DB 연결 성공")
        cursor = connection.cursor()
        query = "SELECT * FROM Stock WHERE stockCode = %s"
        cursor.execute(query, (code,))
        result = cursor.fetchone()
        
        if result is None:
            query = "INSERT INTO stock (stockCode, name) VALUES (%s, %s)"
            cursor.execute(query, (code, name))
            print(f"stockCode {code} Stock Table에 추가 완료")
        else:
            print(f"stockCode {code} 이미 존재함")
        connection.commit()
        cursor.close()
    except Exception as e:
        print("접속오류", e)
    finally:
        disconnect_mariaDB(connection)