from news.repository import find_title_content_by_news_id, update_is_good_by_news_id
from bs4 import BeautifulSoup
from transformers import pipeline
from flask import abort

kor_clf_sentiment = pipeline("sentiment-analysis", "snunlp/KR-FinBert-SC")

def analyze_news_sentiment_by_krFinbert(news_id):
  news = find_title_content_by_news_id(news_id)
  if news is None:
    abort(404, description=f"{news_id}에 해당하는 뉴스가 존재하지 않음")
  if news['is_good'] is not None:
    return str(news['is_good'])
  news['content'] = [text for text in BeautifulSoup(news["content"], 'html.parser').stripped_strings]
  score = 0
  title_score = 2 * kor_clf_sentiment(news['title'])
  score += calculate_score(title_score)
  for content in news['content']:
    content_score = kor_clf_sentiment(content)
    score += calculate_score(content_score)
  is_good = 1 if score >= 0 else 0
  update_is_good_by_news_id(is_good, news_id)
  return str(is_good)
  
def calculate_score(result):
  if(result[0]['label'] == 'neutral'): return 0
  elif(result[0]['label'] == 'positive') : return 1
  else: return -1