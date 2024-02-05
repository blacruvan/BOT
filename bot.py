import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

from modulos.weather import *
from modulos.nasa import *
from modulos.jokes import *
from modulos.converter import *
from configuration import *

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
last_command = None
def createInOut():
    import os
    
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('input'):
        os.makedirs('input')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

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
        print(f'Error when trying to delete the image: {e}')

#jokes
async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getJokes())

#files
async def convert(update, context):
    global last_command
    if last_command == '/convert':
        print('SUUUUUUUUUU')
        file = await context.bot.get_file(update.message.document)
        filename = update.message.document.file_name
        path = f'input/{filename}'
        await file.download_to_drive(path)

        try:
            newPath = convertFile(path)
            if os.path.exists(newPath):
                answer = open(newPath, "rb")
                await context.bot.send_document(chat_id=update.effective_chat.id, document=answer)
                os.remove(path)
                os.remove(newPath)
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Unsupported file format.')
            os.remove(path)
            print(f'Unsupported file format{e}')

async def ask4Doc(update, context):
    global last_command
    last_command = update.message.text
    print(last_command)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envíame el documento")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    createInOut()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    #weather
    application.add_handler(CommandHandler('weather', weather))

    #nasa
    application.add_handler(CommandHandler('nasa', nasa))

    #jokes
    application.add_handler(CommandHandler('jokes', jokes))

    application.add_handler(CommandHandler("convert", ask4Doc))
    application.add_handler(CommandHandler("stats", ask4Doc))

    #files
    application.add_handler(MessageHandler(filters.Document.ALL, convert))
    
    # Keeps the application running
    application.run_polling()