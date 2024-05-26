import requests
from bs4 import BeautifulSoup

def get_latest_article():
    url = 'https://ccc.technews.tw/'
    response = requests.get(url)
    if response.status_code != 200:
        return "無法存取該網址。"
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        latest_article = soup.find('div', class_='content')
        if latest_article:
            title = latest_article.find('h1', class_='entry-title').text.strip()
            link = latest_article.find('a')['href']
            return f"{title}\n{link}"
        else:
            return "找不到最新文章。"
        
