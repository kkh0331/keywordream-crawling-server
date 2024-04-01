from flask import Flask, request, jsonify
#from konlpy.tag import Mecab
from konlpy.tag import Okt
from collections import Counter
from db.connect import get_db
from db.check_insert_stock import check_insert_stock
from db.insert_keywords import insert_keywords
from flask_cors import CORS
import json

import matplotlib.pyplot as plt
import requests
from wordcloud import WordCloud

app = Flask(__name__)
CORS(app, resources={r'*':{'origins':'http://localhost:3000'}})
db = get_db()

# BigKinds API 키 및 기본 설정
API_KEY = 'koba-M3CMSHQ-ZRBUUNI-WHTY2KI-NUYJDCY'
BASE_URL = 'https://www.bigkinds.or.kr/api/news/search.do'  # BigKinds API 검색 URL (예시)
headers = {'Content-Type': 'application/json'}

# 검색 조건 설정
payload = {
    "access_key": API_KEY,
    "argument": {
        "query": "삼성전자",
        "published_at": {
            "from": "2024-03-25",
            "until": "2024-03-24"
        },
        "provider": [],
        "category": [],
        "category_incident": [],
        "byline": "",
        "provider_subject": [],
        "subject_info": [],
        "sort": {"date": "desc"},
        "hilight": 200,
        "return_from": 0,
        "return_size": 10,
        "fields": [
            "byline",
            "category",
            "category_incident",
            "provider_news_id",
            "hilight"
        ]
    }
}

# BigKinds API를 통해 뉴스 데이터 검색
resp = requests.post(BASE_URL, json=payload, headers=headers)
print(resp)
news_data = resp.json()

# 뉴스 데이터에서 본문 추출 및 형태소 분석
okt = Okt()
nouns = []
for news in news_data.get('return_object', {}).get('documents', []):
    content = news.get('content', '')  # 뉴스 본문 필드
    nouns += okt.nouns(content)

# 형태소 분석 결과를 바탕으로 키워드 추출 및 워드클라우드 생성
count = Counter(nouns)
wordcloud = WordCloud(font_path='나눔고딕 경로', background_color='white').generate_from_frequencies(count)

plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


if __name__ == '__main__':
    app.run(debug=True)