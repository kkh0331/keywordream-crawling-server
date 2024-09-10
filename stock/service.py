from flask import abort
from stock.repository import find_stock_by_code, update_recent_news_count_by_code

def find_stock(stock_code):
  stock = find_stock_by_code(stock_code)
  if stock is None:
    abort(404, description=f"{stock_code}에 해당하는 주식이 존재하지 않음")
  return stock

def update_recent_news_count(stock_code, recent_news_count):
  update_recent_news_count_by_code(stock_code, recent_news_count)
  
def extract_stopwords_at_stock(stock):
  stopwords_at_stock = []
  stock_name = stock['name']
  for i in range(len(stock_name)):
    part_of_name = stock_name[:i+1]
    if len(part_of_name) > 1:
      stopwords_at_stock.append(part_of_name)
  return stopwords_at_stock