from db.connect import connect_mariaDB, disconnect_mariaDB

def insertNews(title, press, newsDate, content, imgUrl, originalUrl, newsCode, stockCode):
    values = (title, press, newsDate, content, imgUrl, originalUrl, newsCode, int(stockCode))
    # print(values);
    connection = None
    try:
        connection = connect_mariaDB()
        # print("DB 연결 성공")
        cursor = connection.cursor()
        query = "INSERT INTO News (title, press, newsDate, content, imgUrl, originalUrl, newsCode, stockCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
    except Exception as e:
        print("접속오류", e)
    finally:
        disconnect_mariaDB(connection)