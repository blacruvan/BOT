def getWeather():
    import requests
    weatherLugo = 'https://servizos.meteogalicia.gal/mgrss/predicion/jsonPredConcellos.action?idConc=27028&request_locale=gl'

    clima = {
        -9999: "Non dispoñible",
        101: "Despexado",
        102: "Nubes altas",
        103: "Nubes e claros",
        104: "Anubrado 75%",
        105: "Cuberto",
        106: "Néboas",
        107: "Chuvasco",
        108: "Chuvasco (75%)",
        109: "Chuvasco neve",
        110: "Orballo",
        111: "Choiva",
        112: "Neve",
        113: "Treboada",
        114: "Brétema",
        115: "Bancos de néboa",
        116: "Nubes medias",
        117: "Choiva débil",
        118: "Chuvascos débiles",
        119: "Treboada con poucas nubes",
        120: "Auga neve",
        121: "Sarabia",
        122: "Non dispoñible",
        201: "Despexado",
        202: "Nubes altas",
        203: "Nubes e claros",
        204: "Anubrado 75%",
        205: "Cuberto",
        206: "Néboas",
        207: "Chuvasco",
        208: "Chuvasco (75%)",
        209: "Chuvasco nieve",
        210: "Orballo",
        211: "Choiva",
        212: "Neve",
        213: "Treboada",
        214: "Brétema",
        215: "Bancos de néboa",
        216: "Nubes medias",
        217: "Choiva débil",
        218: "Chuvascos débiles",
        219: "Treboada con poucas nubes",
        220: "Auga neve",
        221: "Sarabia"
    }

    list = []
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
        for clave, valor in pRain.wsitems():
            string = ''
            if clave == 'manha':
                clave = 'mañá'
            string += f'{clave}: {valor}% de probabilidade'
            rainList.append(string)
        imprimir += f'{dia[n]} ({date[:10]}): \n\tTemperatura mínima: {minT}°C\n\tTemperatura máxima: {maxT}°C,\nCeos:\n\t{skyList[0]}\n\t{skyList[1]}\n\t{skyList[2]}\nChoiva:\n\t{rainList[0]}\n\t{rainList[1]}\n\t{rainList[2]}\n\n'
    return imprimir
