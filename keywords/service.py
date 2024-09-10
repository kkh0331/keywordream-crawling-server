from konlpy.tag import Mecab
from collections import Counter
from keywords.repository import save_news_keywords

base_stopwords = ['최근', '요즘', '지난달', '이달', '지난해', '올해', '이날', '지난해', '전날', '이전', '이후',
             '극내','반면','기준', '관련','상황','대비','이상','이하','장중','이후','개인','기관','포인트',
             '주가','거래일','지수','기록','활용','요소']

path = "/opt/homebrew/lib/mecab/dic/mecab-ko-dic"
try:
    mecab = Mecab()
except:
    mecab = Mecab(path)

def extract_keywords_in_news(news, stopwords_at_stock):
  nouns = mecab.nouns(news['content'])
  nouns = [n for n in nouns if len(n) > 1]
  stopwords = base_stopwords + stopwords_at_stock
  count = Counter(nouns)
  tags = [(word, cnt) for word, cnt in count.items() if word not in stopwords]
  save_news_keywords(tags, news["news_id"])