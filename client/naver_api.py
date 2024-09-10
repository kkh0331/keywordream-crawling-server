import requests
from flask import abort
from bs4 import BeautifulSoup

def naver_news_crawling_by_code(code):
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
  url = f"https://m.stock.naver.com/api/news/stock/{code}?pageSize={page_size}&page={page}"
  
  try:
    response = requests.get(url)
    if(response.status_code == 200):
      return response.json()
    else:
      print(f"naver_news_crawling_by_code({code})에서 네이버 뉴스 크롤링 실패")
      abort(response.status_code, description="네이버 뉴스 리스트 크롤링 실패")
  except Exception as e:
    print(f"naver_news_crawling_by_code({code})에서 네이버 뉴스 리스트 크롤링 에러")
    abort(500, description="네이버 뉴스 리스트 크롤링 에러")

def naver_news_content_crawling(url):
  try:
    response = requests.get(url, timeout=0.5)
    if(response.status_code == 200):
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      content = soup.select_one('#dic_area')
      if content is None:
        return None
      for img_tag in content.find_all('img'):
        if img_tag.has_attr('data-src'):
          img_tag['src'] = img_tag['data-src']
          del img_tag['data-src']
      for element in content.find_all(class_='img_desc'):
        element.decompose()
      return content.prettify()
    else:
      return None
  except:
    return None