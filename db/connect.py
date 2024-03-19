import pymysql
import os
from dotenv import load_dotenv
from dbutils.persistent_db import PersistentDB
from flask import globals

load_dotenv()

def connect_db():
    
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
    
def get_db():
    if not hasattr(globals, 'db'):
        print("없어서 새로 발급")
        globals.db = connect_db()
    return globals.db.connection()