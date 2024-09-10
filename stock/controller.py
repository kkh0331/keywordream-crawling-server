from flask import Blueprint
from stock.service import find_stock, update_recent_news_count, extract_stopwords_at_stock
from utils.api_result import success_response
from crawling.service import news_list_crawling_by_code
from keywords.service import extract_keywords_in_news

stock = Blueprint("stock", __name__, template_folder="templates")

@stock.route('/<stock_code>/news/crawling')
def crawl_stock_news_and_extract_keyword(stock_code):
  stock = find_stock(stock_code)
  news_list, recent_news_count = news_list_crawling_by_code(stock['code'])
  update_recent_news_count(stock_code, recent_news_count)
  stopwords_at_stock = extract_stopwords_at_stock(stock)
  for news in news_list:
    extract_keywords_in_news(news, stopwords_at_stock)
  return success_response(200, "News crawling and keyword extraction is successful")