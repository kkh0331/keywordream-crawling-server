import pymysql
import os
from dotenv import load_dotenv
from dbutils.persistent_db import PersistentDB
from flask import globals

load_dotenv()

def connect_database():
    return PersistentDB(
        creator=pymysql,
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    
def get_database():
    if not hasattr(globals, 'db'):
        print("database와 연결 시작")
        globals.db = connect_database()
    return globals.db.connection()