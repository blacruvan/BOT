from telegram import InlineKeyboardButton

main = [
        [InlineKeyboardButton("Weather", callback_data='weather'),
         InlineKeyboardButton("NASA", callback_data='nasa'),
         InlineKeyboardButton("Jokes", callback_data='jokes')],
        
        [InlineKeyboardButton("Convert", callback_data='convert'),
         InlineKeyboardButton("Stats", callback_data='stats')],

        [InlineKeyboardButton("Newsletter", callback_data='newsletter'),
         InlineKeyboardButton("Cinema", callback_data='cinema')],

        [InlineKeyboardButton("Trivia", callback_data='trivia'),
         InlineKeyboardButton("Proposta2", callback_data='convert')],

        [InlineKeyboardButton("💀 INFERNO 💀", callback_data='inferno')]
    ]

weather = [
            [InlineKeyboardButton('Lugo', callback_data='weather_lugo'),
            InlineKeyboardButton('Friol', callback_data='weather_friol'),
            InlineKeyboardButton('Ribadeo', callback_data='weather_ribadeo')],

            [InlineKeyboardButton('A Coruña', callback_data='weather_coruña'),
            InlineKeyboardButton('Ferrol', callback_data='weather_ferrol'),
            InlineKeyboardButton('Santiago', callback_data='weather_santiago')],

            [InlineKeyboardButton('Pontevedra', callback_data='weather_pontevedra'),
            InlineKeyboardButton('Vigo', callback_data='weather_vigo'),
            InlineKeyboardButton('Ourense', callback_data='weather_ourense')],

            [InlineKeyboardButton('« Volver', callback_data='volver')]
        ]

cinema = [
            [InlineKeyboardButton('Marineda', callback_data='cinema_marineda'),
            InlineKeyboardButton('Cancelas', callback_data='cinema_cancelas'),
            InlineKeyboardButton('Cantones', callback_data='cinema_cantones')],
            
            [InlineKeyboardButton('Lugo', callback_data='cinema_lugo'),
            InlineKeyboardButton('Vigo', callback_data='cinema_vigo'),
            InlineKeyboardButton('Ourense', callback_data='cinema_ourense')],

            [InlineKeyboardButton('« Volver', callback_data='volver')]
        ]

game = [
            [InlineKeyboardButton('« Volver', callback_data='volver'),
            InlineKeyboardButton('Seguir jugando', callback_data='trivia')]
        ]

def generateTriviaMenu(c, i1, i2, i3):
    import random
    menu = [
            [InlineKeyboardButton(c, callback_data='correcta'),
            InlineKeyboardButton(i1, callback_data='incorrecta')],
            
            [InlineKeyboardButton(i2, callback_data='incorrecta'),
            InlineKeyboardButton(i3, callback_data='incorrecta')],
        ]
    random.shuffle(menu)
    menu.append([InlineKeyboardButton('« Volver', callback_data='volver')])
    return menu