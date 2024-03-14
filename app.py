from flask import Flask, request
from crawling.crawling import total_crawling
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "test"

@app.route('/api/news', methods=['POST'])
def crawling_keyword():
    stockList = request.json['stockList'] # [code]
    stock_news = total_crawling(stockList)
    return stock_news

if __name__ == '__main__':
    app.run(debug=True)