def getNasaImage():
    from PIL import Image
    import requests
    import os

    KEY = 'TTAcbwe4sDbn2ZMc1pNY4XdxPUmC1hc5gpSDkCOL'
    URL = f'https://api.nasa.gov/planetary/apod?api_key={KEY}'

    try:
        response = requests.get(URL)
        image, title, description = None, None, None
        info = response.json()
        image, title, description = info['url'], info['title'], info['explanation']
        path = f'output/nasa.{image.split(".")[-1]}'
        getImage(image, path)
        return (path,f'{title}\n{description}')
    except Exception as e:
        print(f'Error getting data from API: {e}')

    
def getImage(url, ruta):
    import requests
    from io import BytesIO
    from PIL import Image
    try:
        response = requests.get(url)
        if response.status_code == 200:
            imagen = Image.open(BytesIO(response.content))
            imagen.save(ruta)
    except Exception as e:
        print(f'Error downloading image: {e}')