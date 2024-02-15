import requests
from .translator import *

def getJokes():
    URL = 'https://v2.jokeapi.dev/joke/Any'
    try:
        response = requests.get(URL)
        info = response.json()
        setup, delivery = translate(info['setup']), translate(info['delivery'])
        return f"{setup}\n\n{delivery}"

    except Exception as e:
        return None
    

    