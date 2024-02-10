from typing import Tuple
from pathlib import Path
from io import BytesIO
from PIL import Image
import requests
from .translator import *

def getNasaImage() -> Tuple[Path, str]:
    KEY = 'TTAcbwe4sDbn2ZMc1pNY4XdxPUmC1hc5gpSDkCOL'
    URL = f'https://api.nasa.gov/planetary/apod?api_key={KEY}'

    try:
        response = requests.get(URL)
        image, title, description = None, None, None
        info = response.json()
        image, title, description = info['url'], info['title'], info['explanation']
        path = Path(f'output/nasa.{image.split(".")[-1]}')
        getImage(image, path)
        title = translate(title)
        caption = f'<u><strong>{title}</strong></u>\n{description}'
        return (path,caption if len(caption)<1024 else caption[:1024])
        
    except Exception as e:
        print(f'Error getting data from API: {e}')

    
def getImage(url, ruta):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            imagen = Image.open(BytesIO(response.content))
            imagen.save(ruta)
    except Exception as e:
        print(f'Error downloading image: {e}')