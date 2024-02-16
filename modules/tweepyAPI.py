import requests
from bs4 import BeautifulSoup

def getHeadlines():
    url = 'https://www.edreams.es'
    page = requests.get(url,
                     headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
    soup = BeautifulSoup(page.content,'html.parser')

    clase = soup.find_all(class_="css-1xi4blx e17fzqxg0")
    print(clase)

getHeadlines()