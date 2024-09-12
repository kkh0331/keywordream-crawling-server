from flask import Blueprint
from utils.api_result import success_response
from news.service import analyze_news_sentiment_by_krFinbert

news = Blueprint("news", __name__, template_folder="templates")

@news.route('/<news_id>/sentiment-analysis')
def analyze_news_sentiment(news_id):
  is_good = analyze_news_sentiment_by_krFinbert(news_id)
  result = {
    "news_id" : news_id,
    "is_good" : is_good
  }
  return success_response(200, result)