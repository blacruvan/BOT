def getNasaImage():
    import requests
    KEY = 'TTAcbwe4sDbn2ZMc1pNY4XdxPUmC1hc5gpSDkCOL'
    URL = f'https://api.nasa.gov/planetary/apod?api_key={KEY}'
    response = requests.get(URL)
    image, title, description = None, None, None
    info = response.json()
    image = info['url']
    title = info['title']
    description = info['explanation']
    image = getImage(image)
    print(image, title, description)

    
def getImage(url):
    import requests
    from PIL import Image
    from io import BytesIO
    import os
    try:
        response = requests.get(url)
        response.raise_for_status() 

        image = Image.open(BytesIO(response.content))

        if not os.path.exists('/output'):
            os.makedirs('/output')

        # Construir la ruta completa para guardar la imagen
        nombre_archivo = os.path.join('/output', "NASA.jpg")

        # Guardar la imagen en el directorio destino
        image.save(nombre_archivo)

        return nombre_archivo

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la imagen desde la URL: {e}")
        return None
    
getNasaImage()