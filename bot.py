import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, Updater
from telegram import InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from dotenv import load_dotenv
import asyncio

from pathlib import Path
import modules as mod
import configuration as conf
import interface.menu as menu
import random

# Authentication to manage the bot
load_dotenv()
TOKEN = os.getenv('TOKEN')
if TOKEN == None:
    print('Lembra indicar a variable TOKEN')
    print('docker run --rm -e TOKEN=xxx')
    exit(1)
          
# Show logs in terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

last_command, main_menu_message_id = None, None

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE, location: str):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getWeather(location), parse_mode='HTML')

async def getNasaImageWithTimeout():
    async def nasaAsync():
        return mod.getNasaImage()
    task = asyncio.create_task(nasaAsync())

    try:
        result = await asyncio.wait_for(task, timeout=5)
        return result
    except asyncio.TimeoutError:
        task.cancel()
        raise TimeoutError("La operación excedió el tiempo de espera")


async def nasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_message(update.effective_chat.id, "Cargando...")

    try:
        image, text = await getNasaImageWithTimeout()
        await context.bot.delete_message(update.effective_chat.id, message.message_id)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=text, parse_mode='HTML')
    except Exception:
        await context.bot.delete_message(update.effective_chat.id, message.message_id)
        await context.bot.send_message(update.effective_chat.id, "Tiempo de espera excedido. Inténtalo de nuevo más tarde.")
    finally:
        conf.clearOutDir()

async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getJokes())

async def processDocs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_command
    global main_menu_message_id

    file = await context.bot.get_file(update.message.document)
    filename = update.message.document.file_name
    path = Path(f'input/{filename}')
    await file.download_to_drive(path)
    if last_command == 'stats':
        try:
            info, stats = mod.getStats(path)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=info)
            await context.bot.send_document(chat_id=update.effective_chat.id, document=stats)
        except Exception as e:
            print(f'Error trying to read the csv: {e}')

    else:
        try:
            newPath = mod.convertFile(path)
            newPath = Path(newPath)
            if newPath.exists():
                with open(newPath, "rb") as answer:
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=answer)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Unsupported file format.')
            print(f'Unsupported file format: {e}')
    

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=main_menu_message_id)
    main_menu_message_id = None
    await show_buttons(update, context)
    conf.clearInDir()
    conf.clearOutDir()

async def ask4Doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envíame el documento 😊")

async def newsletter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/eldiario.jpg'), caption=mod.getHeadlines(), parse_mode='HTML')

async def cinema(update: Update, context: ContextTypes.DEFAULT_TYPE, location: str):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/cinema.png'), caption=mod.getCinemaListings(location), parse_mode='HTML')

async def inferno(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/inferno.jpg'), caption=mod.showDestiny('Vanesa'))

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    message = await context.bot.send_message(update.effective_chat.id, "Cargando...")
    trivial = mod.trivia()
    if trivial:
        pregunta, c, i1, i2, i3 = trivial
        await context.bot.delete_message(update.effective_chat.id, message.message_id)

        triviaButtons = menu.generateTriviaMenu(c, i1, i2, i3)
        reply_markup = InlineKeyboardMarkup(triviaButtons)
        query = update.callback_query
        await query.edit_message_text(pregunta, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="El trivial no está disponible ahora mismo 😟")


async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/cinema.png'), caption=mod.showDestiny('Vanesa'))

async def show_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global main_menu_message_id

    keyboard = menu.main
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if main_menu_message_id:
        query = update.callback_query
        if query:
            await query.edit_message_text('MENU', reply_markup=reply_markup)
    else:
        msg = await context.bot.send_message(update.effective_chat.id, 'MENU', reply_markup=reply_markup)
        main_menu_message_id = msg.message_id

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global main_menu_message_id
    global last_command

    query = update.callback_query
    data = query.data
    
    actions = {
        'nasa': nasa,
        'jokes': jokes,
        'convert': ask4Doc,
        'stats': ask4Doc,
        'newsletter': newsletter,
        'inferno': inferno,
        'trivia': trivia
    }

    action_function = actions.get(data)
    if data == 'weather':
        weatherButtons = menu.weather
        reply_markup = InlineKeyboardMarkup(weatherButtons)
        await query.edit_message_text('¿De dónde?', reply_markup=reply_markup)
 
    elif data == 'cinema':
        cinemaButtons = menu.cinema
        reply_markup = InlineKeyboardMarkup(cinemaButtons)
        await query.edit_message_text('¿Qué cartelera quieres ver?', reply_markup=reply_markup)
    
    elif data in ['convert', 'stats']:
        last_command = data
        await action_function(update, context)
    
    elif data in ['weather_lugo', 'weather_friol', 'weather_ribadeo', 'weather_coruña', 'weather_ferrol', 'weather_santiago', 'weather_pontevedra', 'weather_vigo', 'weather_ourense']:
        await weather(update, context, data[8:])
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=main_menu_message_id)
        main_menu_message_id = None
        await show_buttons(update, context)

    elif data in ['cinema_marineda', 'cinema_cancelas', 'cinema_cantones', 'cinema_lugo', 'cinema_vigo', 'cinema_ourense']:
        await cinema(update, context, data[7:])
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=main_menu_message_id)
        main_menu_message_id = None
        await show_buttons(update, context)

    elif data == 'trivia':
        await trivia(update, context)
    
    elif data in ['correcta', 'incorrecta']:
        game = menu.game
        reply_markup = InlineKeyboardMarkup(game)
        query = update.callback_query
        if data == 'correcta':
            await query.edit_message_text('CORECTO ✅', reply_markup=reply_markup)
        else:
            await query.edit_message_text('INCORRECTO ❌', reply_markup=reply_markup)

    elif data == 'volver':
        await show_buttons(update, context)

    elif action_function:
        await action_function(update, context)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=main_menu_message_id)
        main_menu_message_id = None
        await show_buttons(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', show_buttons))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.Document.ALL, processDocs))

    application.add_handler(CommandHandler("proba", proba))

    application.run_polling()

if __name__ == '__main__':
    main()
    conf.createInOut()