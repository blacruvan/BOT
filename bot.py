import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

from modulos.taboas import *
from modulos.weather import *
from modulos.nasa import *
from modulos.jokes import *
from modulos.converter import *

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

# This function responds to echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# This function responds to start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Son un bot, dime algo!")

# function
async def afirmador(update, context):
    file = await context.bot.get_file(update.message.document)
    filename = update.message.document.file_name
    await file.download_to_drive(filename)
  
   # envía ficheiro de resposta
    answer = open('docs/resposta.txt', "rb")
    await context.bot.send_document(chat_id=update.effective_chat.id, document=answer)

#weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getWeather())

#NASA
async def nasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image, text = getNasaImage()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=text)
    try:
        if os.path.exists(image): os.remove(image)
    except Exception as e:
        print(f'Error al intentar borrar la imagen: {e}')

#jokes
async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getJokes())

# archivos
async def convert(update, context):
    file = await context.bot.get_file(update.message.document)
    filename = update.message.document.file_name
    await file.download_to_drive(f"input/{filename}")

if __name__ == '__main__':
    # Start the application to operate the bot
    application = ApplicationBuilder().token(TOKEN).build()

    # Handler to manage the start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handler to manage text messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    #weather
    weather_handler = CommandHandler('weather', weather)
    application.add_handler(weather_handler)

    #nasa
    nasa_handler = CommandHandler('nasa', nasa)
    application.add_handler(nasa_handler)

    #chistes
    jokes_handler = CommandHandler('jokes', jokes)
    application.add_handler(jokes_handler)

    #archivos
    application.add_handler(MessageHandler(filters.Document.ALL, convert))

    #handler documentos
    application.add_handler(MessageHandler(filters.Document.ALL, afirmador))
    
    # Keeps the application running
    application.run_polling()