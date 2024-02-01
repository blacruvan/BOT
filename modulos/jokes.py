def getJokes():
    import requests
    URL = 'https://v2.jokeapi.dev/joke/Dark'
    try:
        response = requests.get(URL)
        info = response.json()
        return f"{info['setup']}\n\n{info['delivery']}"

    except Exception as e:
        return f"Error al obtener el chiste: {e}"

print(getJokes())