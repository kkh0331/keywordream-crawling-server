import pymysql as my
import os
from dotenv import load_dotenv

load_dotenv()

def connect_mariaDB():
    try:
        connection = my.connect(host=os.getenv("DB_HOST"),
                                port=int(os.getenv("DB_PORT")),
                                user=os.getenv("DB_USER"),
                                password=os.getenv("DB_PASSWORD"),
                                database=os.getenv("DB_DATABASE"),
                                cursorclass=my.cursors.DictCursor
                                )
        return connection
    except:
        return None
    
def disconnect_mariaDB(connection):
    if connection:
        connection.close()
    # print('DB 연결 종료')