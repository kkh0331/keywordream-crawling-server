import requests

def naver_news_api(stock_code):
  '''
  네이버 뉴스 api을 통해서 관련 종목에 대한 종목을 가져온다.
  다음과 같은 사항이 존재한다.
  - articleId
  - body(요약)
  - id
  - imageOriginLink
  - officeId
  - officeName
  - photoType
  - title
  - titleFull
  '''

  page_size = 20 
  page = 1 
  url = f"https://m.stock.naver.com/api/news/stock/{stock_code}?pageSize={page_size}&page={page}"
  
  try:
    response = requests.get(url)
    if(response.status_code == 200):
      return response.json()
    else:
      return "Error"
  except Exception as ex:
    return "Error"  