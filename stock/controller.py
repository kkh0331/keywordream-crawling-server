from flask import Blueprint
from stock.service import find_stock
from utils.api_result import success_response
from crawling.service import news_list_crawling_by_code

stock = Blueprint("stock", __name__, template_folder="templates")

@stock.route('/<stock_code>/news/crawling')
def crawl_stock_news_and_extract_keyword(stock_code):
  stock = find_stock(stock_code)
  news_list, recent_news_count = news_list_crawling_by_code(stock['code'])
  return success_response(200, news_list)