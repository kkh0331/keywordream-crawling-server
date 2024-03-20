from flask import Flask, request, jsonify
from konlpy.tag import Mecab
from collections import Counter
from crawling.crawling import each_crawling
from db.connect import get_db
from db.check_insert_stock import check_insert_stock
from db.insert_keywords import insert_keywords
import json

app = Flask(__name__)
db = get_db()
# print(db)

@app.route('/api/news', methods=['POST'])
def crawling_keyword():
    # request body : {"name" : "삼성전자", "code" : "005930"}
    name = request.json['name'] # [code]
    code = request.json['code']
    tags = None
    if check_insert_stock(name, code):
        news_text = each_crawling(code) # code에 대한 뉴스 가져옴

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
    result = json.dumps([{"word":tag[0], "cnt":tag[1]} for tag in tags], ensure_ascii=False)
    if insert_keywords(result, code):
        response_data = {"message": "요청이 성공적으로 처리되었습니다."}
        return jsonify(response_data), 200
    
    response_data = {"message": "요청이 실패했습니다."}
    return jsonify(response_data), 404
    
if __name__ == '__main__':
    app.run(debug=True)