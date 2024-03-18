from db.connect import connect_mariaDB, disconnect_mariaDB
import pymysql as my

def getContent(newsCode):
    connection = None
    content = None
    try:
        connection = connect_mariaDB()
        # print("DB 연결 성공")
        cursor = connection.cursor()
        query = "SELECT content from News WHERE newsCode = %s"
        cursor.execute(query, (newsCode, ))
        result = cursor.fetchone()
        if result:
            # print(result)
            content = result['content']
        cursor.close()
    except Exception as e:
        print("접속오류", e)
    finally:
        disconnect_mariaDB(connection)
    return content