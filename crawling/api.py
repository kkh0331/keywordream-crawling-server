import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

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
  naver_api_url = os.getenv('NAVER_API_URL')
  page_size = 20 
  page = 1 
  url = f"{naver_api_url}/{stock_code}?pageSize={page_size}&page={page}"
  
  try:
    response = requests.get(url)
    if(response.status_code == 200):
      return response.json()
    else:
      return "Error"
  except Exception as ex:
    return "Error"
  
  # request = urllib.request.Request(url)
  # request.add_header("X-Naver-Client-Id", client_id)
  # request.add_header("X-Naver-Client-Secret", client_secret)
  # response = urllib.request.urlopen(request)
  # rescode = response.getcode()
  # if(rescode == 200):
  #   response_body = response.read()
  #   # print(type(response_body))
  #   return json.loads(response_body.decode('utf-8'))['items']
  # else:
  #   print(f"Error Code: ${rescode}")
  #   return "Error"
    
  