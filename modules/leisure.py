import requests
from bs4 import BeautifulSoup

def getActivities(location):

    url = f'https://ocioengalicia.com/{location}/'
    try:
        page = requests.get(url,
                        headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
        soup, html = BeautifulSoup(page.content,'html.parser'), ''

        for container in soup.find_all(class_='grid-container')[:5]:
            url, title, date, place = container.find('h3').find('a').get('href'), container.find('h3').find('a').text, container.find('div', class_='fecha').text.strip(), container.find(id='venue').find('a').text if container.find(id='venue') is not None and container.find(id='venue').find('a') is not None else None
            html += f'› <a href="{url}">{title}</a>\nFecha: {date}\nLugar: {place}\n\n' if place else f'› <a href="{url}">{title}</a>\nFecha: {date}\n\n'
        return html
    
    except requests.exceptions.RequestException as e:
        raise Exception('Error when making HTTP request: ', e)

    except Exception as e:
        raise Exception('There is no movie leisure for you :( ', e)