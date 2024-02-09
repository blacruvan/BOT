import requests
from bs4 import BeautifulSoup

def getCinemaListings():
    URL = 'https://www.taquilla.com/lugo/yelmo-as-termas-lugo'
    paxina = requests.get(URL)
    soup = BeautifulSoup(paxina.content,'html.parser')
    html = ''

    for noticia in soup.find_all(class_="list-films__content"):
        film = noticia.find(class_="film-title data-link").text
        url = noticia.h3.get('data-link')
        html += f'- <a href="{url}">{film}</a>\n\n'
    return html