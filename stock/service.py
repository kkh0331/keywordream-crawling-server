from flask import abort
from stock.repository import find_stock_by_code

def find_stock(stock_code):
  stock = find_stock_by_code(stock_code)
  if stock is None:
    abort(404, description=f"{stock_code}에 해당하는 주식이 존재하지 않음")
  return stock