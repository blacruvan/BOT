import requests

def getWeather(city):
    import resources.weather_codes as weather

    locations, clima = weather.locations, weather.emojis
    weatherLugo = f'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action?idConc={locations[city]}&request_locale=gl'

    try:
        response = requests.get(weatherLugo)
        weather = response.json()
        moment = ['Hoxe', 'Maña', 'Pasado']
        html = ''
        for n in range(3):
            day, sky, date, pRain, maxT, minT = [], None, None, None, None, None
            info = weather['predConcello']['listaPredDiaConcello'][n]
            sky, date, pRain, maxT, minT = info['ceo'], info['dataPredicion'], info['pchoiva'], info['tMax'], info['tMin']
            skyList = []
            for clave, valor in sky.items():
                string = ''
                if clave == 'manha':
                    clave = 'mañá'
                string += f'{clave}: {clima[valor]}'
                skyList.append(string)
            
            rainList = []
            for clave, valor in pRain.items():
                string = ''
                if clave == 'manha':
                    clave = 'mañá'
                string += f'{clave}: {valor}% de probabilidade'
                rainList.append(string)

            printDay = f'<u>{moment[n]} ({date[:10]})</u>:'
            printTemp = f'\n    <b>Mínima:</b> {minT}°C\n    <b>Máxima:</b> {maxT}°C'
            printSky = f'\n<b>Ceos:</b>\n    {skyList[0]}\n    {skyList[1]}\n    {skyList[2]}'
            printRain = f'\n<b>Choiva:</b>\n    {rainList[0]}\n    {rainList[1]}\n    {rainList[2]}\n\n'
            
            html += printDay + printTemp + printSky + printRain
        return html

    except Exception as e:
        print(f'You\'ll have to guess the weather, cause the API cannot be accessed: {e}')
        return 'No hay información 😭'