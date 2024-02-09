def getWeather():
    import requests
    import resources.weather_codes as weather
    weatherLugo = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action?idConc=27028&request_locale=gl'

    clima = weather.emojis

    response = requests.get(weatherLugo)
    weather = response.json()
    dia = ['Hoxe', 'Maña', 'Pasado']
    imprimir = ''
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

        printDay = f'<u>{dia[n]} ({date[:10]})</u>:'
        printTemp = f'\n    <b>Mínima:</b> {minT}°C\n    <b>Máxima:</b> {maxT}°C'
        printSky = f'\n<b>Ceos:</b>\n    {skyList[0]}\n    {skyList[1]}\n    {skyList[2]}'
        printRain = f'\n<b>Choiva:</b>\n    {rainList[0]}\n    {rainList[1]}\n    {rainList[2]}\n\n'
        
        imprimir += printDay + printTemp + printSky + printRain
        #imprimir += f'{dia[n]} ({date[:10]}): \n\tTemperatura mínima: {minT}°C\n\tTemperatura máxima: {maxT}°C,\nCeos:\n\t{skyList[0]}\n\t{skyList[1]}\n\t{skyList[2]}\nChoiva:\n\t{rainList[0]}\n\t{rainList[1]}\n\t{rainList[2]}\n\n'
    return imprimir
