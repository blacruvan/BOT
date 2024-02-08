import requests
from bs4 import BeautifulSoup

def getHeadlines():
    #generar try
    url = 'https://www.eldiario.es'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    html = ''

    headers = soup.find_all(class_="ni-subtitle")[:3]
    for new in headers:
        headLine, link = new.a.text, new.a.get('href')
        html += f'- <a href="{link}">{headLine}</a>\n\n'

    headers = soup.find_all(class_="ni-title")[:3]
    for new in headers:
        headLine, link = new.a.text.strip(), new.a.get('href')
        html += f'- <a href="https://www.eldiario.es{link}">{headLine}</a>\n\n'

    print(len(html))
    return html

getHeadlines()