import requests
from bs4 import BeautifulSoup

def extract_content(url):
  sample_url = url
  response = requests.get(sample_url)
  if(response.status_code == 200):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.select_one('#dic_area')
    
    for img_tag in content.find_all('img'):
      if img_tag.has_attr('data-src'):
        img_tag['src'] = img_tag['data-src']
        del img_tag['data-src']
    
    for element in content.find_all(class_='img_desc'):
      element.decompose()
      
    return content.prettify()
  else:
    return "none"