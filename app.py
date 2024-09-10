from flask import Flask
import json
import os
import time

from stocks.controller import stock
from news.controller import news
from utils.json_app import JsonApp

app = JsonApp(Flask(__name__))
app.register_blueprint(stock, url_prefix="/api/stocks")
app.register_blueprint(news, url_prefix="/api/news")
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')