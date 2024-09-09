from flask import Blueprint, abort, jsonify
from stock.service import find_stock
from utils.api_result import success_response

stock = Blueprint("stock", __name__, template_folder="templates")

@stock.route('/<stock_code>/news/crawling')
def crawl_stock_news_and_extract_keyword(stock_code):
  stock = find_stock(stock_code)
  return success_response(200, stock)