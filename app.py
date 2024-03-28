from flask import Flask, request, jsonify
from konlpy.tag import Mecab
from collections import Counter
from crawling.crawling import each_crawling
from db.connect import get_db
from db.check_insert_stock import check_insert_stock
from db.insert_keywords import insert_keywords
from db.get_title_content import get_title_content
from db.insert_isGood import insert_isGood
from flask_cors import CORS
from bs4 import BeautifulSoup
from transformers import pipeline
import json
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = Flask(__name__)
CORS(app, resources={r'*':{'origins':'http://localhost:3003'}})
db = get_db()
kor_clf_sentiment = pipeline("sentiment-analysis", "snunlp/KR-FinBert-SC")

stopwords = ['최근', '요즘', '지난달', '이달', '지난해', '올해', '이날', '지난해', '전날', '이전', '이후',
             '극내','빈면','기준', '관련','상황','대비','이상','이하','장중','이후','개인','기관','포인트',
             '주가','거래일','지수','기록','활용','요소']

@app.route('/api/news', methods=['POST'])
def crawling_keyword():
    # request body : {"name" : "삼성전자", "code" : "005930"}
    # name = request.json['name'] # [code]
    code = request.json['code']
    tags = None
    if check_insert_stock("임시", code):
        news_text = each_crawling(code) # code에 대한 뉴스 가져옴
    # return news_text
    # KoNLpy + Mecab : 형태소 분석
    # 형태소 분석기로 명사만 추출,1글자는 의미없다고 보고 삭제
    path = "/opt/homebrew/lib/mecab/dic/mecab-ko-dic"
    try:
        mecab = Mecab() 
    except: 
        mecab = Mecab(path)
    nouns = mecab.nouns(' '.join(news_text))
    nouns = [n for n in nouns if len(n) > 1]

     # 종목 이름과 일부를 불용어로 추가
    stopwords_exp = stopwords + get_stopwords_for_stock(code)
    print(stopwords_exp)

    # 단어 개수 세기, 가장 많이 등장한 N개 구하기(Counter.most_common())
    count = Counter(nouns)
    tags = count.most_common(40)
    # 불용어 제거
    tags = [(word, cnt) for word, cnt in tags if word not in stopwords_exp]
    
    result = json.dumps([{"word":tag[0], "cnt":tag[1]} for tag in tags], ensure_ascii=False)
    if insert_keywords(result, code):
        response_data = {"message": "요청이 성공적으로 처리되었습니다."}
        return jsonify(response_data), 200
    
    response_data = {"message": "요청이 실패했습니다."}
    return jsonify(response_data), 404


def get_stopwords_for_stock(code):
    # 여기에서 데이터베이스 또는 다른 소스로부터 종목 이름과 일부를 가져와서 불용어로 처리합니다.
    stopwords_for_stock = []
    cursor = db.cursor()
    query = "SELECT name FROM Stock WHERE stockCode = %s"
    cursor.execute(query, (code, ))
    stock_name = cursor.fetchone()

    if stock_name:
        stock_name = stock_name['name']  # dict에서 종목 이름 문자열로 변환
        
        # 종목 이름의 일부도 불용어로 처리
        for i in range(len(stock_name)):
            part_of_name = stock_name[:i+1]  # 종목 이름의 처음부터 i+1까지의 부분
            if len(part_of_name) > 1:  # 한 글자 이상인 경우에만 추가
                stopwords_for_stock.append(part_of_name)

    print(stopwords_for_stock)

    return stopwords_for_stock


@app.route('/api/krFinBert', methods=['POST'])
def content_sentiment():
    newsId = request.json['newsId']
    text = get_title_content(newsId)
    if text['isGood'] is not None:
        return str(text['isGood'])
    text["content"] = [text for text in BeautifulSoup(text["content"], 'html.parser').stripped_strings]
    score = 0 # positive
    res_title = 2 * kor_clf_sentiment(text['title'])
    score += calculate_score(res_title)
    for text in text["content"]:
        res_content = kor_clf_sentiment(text)
        score += calculate_score(res_content)
    isGood = 1 if score >= 0 else 0
    insert_isGood(isGood, newsId)
    return str(isGood)

def calculate_score(result):
    if(result[0]['label'] == 'neutral'): return 0
    elif(result[0]['label'] == 'positive') : return 1
    else: return -1
    
if __name__ == '__main__':
    app.run(debug=True)