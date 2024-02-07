import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

from pathlib import Path

import modules as mod
import configuration as conf

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


    

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#weather
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getWeather(), parse_mode='HTML')

#NASA
async def nasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image, text = mod.getNasaImage()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=text, parse_mode='HTML')
    conf.clearOutDir()

#jokes
async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getJokes())

#files
async def processDocs(update, context):
    global last_command

    file = await context.bot.get_file(update.message.document)
    filename = update.message.document.file_name
    path = Path(f'input/{filename}')
    await file.download_to_drive(path)

    if last_command == '/stats':
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

    conf.clearInDir()
    conf.clearOutDir()

async def ask4Doc(update, context):
    global last_command
    last_command = update.message.text
    print(last_command)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envíame el documento")

async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<u>Some text</u>", parse_mode='HTML') 

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    conf.createInOut()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CommandHandler('nasa', nasa))
    application.add_handler(CommandHandler('jokes', jokes))
    application.add_handler(CommandHandler("convert", ask4Doc))
    application.add_handler(CommandHandler("stats", ask4Doc))
    application.add_handler(CommandHandler("proba", proba))
    application.add_handler(MessageHandler(filters.Document.ALL, processDocs))
    
    # Keeps the application running
    application.run_polling()