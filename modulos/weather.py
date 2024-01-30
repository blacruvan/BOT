import requests
weatherLugo = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action?idConc=27028&request_locale=gl'

list = []
response = requests.get(weatherLugo)
weather = response.json()
for n in range(3):
    day, sky, date, pRain, maxT, minT = [], None, None, None, None, None
    info = weather['predConcello']['listaPredDiaConcello'][n]
    sky, date, pRain, maxT, minT = info['ceo'], info['dataPredicion'], info['pchoiva'], info['tMax'], info['tMin']
    print(sky, date, pRain, maxT, minT, '\n')
