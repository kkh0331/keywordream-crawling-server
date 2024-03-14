from flask import Flask, request
from crawling.crawling import total_crawling
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "test"

@app.route('/api/news', methods=['POST'])
def crawling_keyword():
    stockList = request.json['stockList'] # [{name, code}]
    news_list = total_crawling(stockList)
    return news_list

if __name__ == '__main__':
    app.run(debug=True)