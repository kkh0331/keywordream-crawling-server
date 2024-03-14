import requests
from bs4 import BeautifulSoup

def extract_content(url):
  sample_url = url
  response = requests.get(sample_url)
  if(response.status_code == 200):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.select_one('#dic_area')
    # print(content)
    # return content.prettify() # 태그형태로 받은 content을 html 상태로 string화
    return content.get_text()
  else:
    return "none"