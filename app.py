from flask import Flask, request
from konlpy.tag import Mecab
from collections import Counter
from crawling.crawling import each_crawling
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "test"

@app.route('/api/news', methods=['POST'])
def crawling_keyword():
    # request body : {"name" : "삼성전자", "code" : "005930"}
    name = request.json['name'] # [code]
    code = request.json['code']
    # stock_contents = total_crawling(stockList)
    news_text = each_crawling(name, code) or []; # code에 대한 뉴스 가져옴
    #return news_text

    # KoNLpy + Mecab : 형태소 분석
    # 형태소 분석기로 명사만 추출,1글자는 의미없다고 보고 삭제
    path = "/opt/homebrew/lib/mecab/dic/mecab-ko-dic"
    try:
        mecab = Mecab() 
    except: 
        mecab = Mecab(path)
    nouns = mecab.nouns(' '.join(news_text))
    nouns = [n for n in nouns if len(n) > 1]

    # 단어 개수 세기, 가장 많이 등장한 N개 구하기(Counter.most_common())
    count = Counter(nouns)
    tags = count.most_common(40)
    return tags

if __name__ == '__main__':
    app.run(debug=True)