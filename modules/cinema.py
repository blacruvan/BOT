import requests
from bs4 import BeautifulSoup
import resources.cinema_links as links
def getCinemaListings(location):

    URL = links.URL[location]
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup, html = BeautifulSoup(response.content, 'html.parser'), ''

        for noticia in soup.find_all(class_="list-films__content"):
            film = noticia.find(class_="film-title data-link").text
            url = noticia.h3.get('data-link')
            html += f'› <a href="{url}">{film}</a>\n\n'
        return html

    except requests.exceptions.RequestException as e:
        raise Exception('Error when making HTTP request: ', e)

    except Exception as e:
        raise Exception('There is no movie listings for you :( ', e)