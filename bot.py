import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, Updater
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from pathlib import Path

import requests
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
msgId = None

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getWeather(), parse_mode='HTML')

async def nasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image, text = mod.getNasaImage()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=text, parse_mode='HTML')
    conf.clearOutDir()

async def jokes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mod.getJokes())

async def processDocs(update, context):
    global last_command

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

    await show_buttons(update, context)
    conf.clearInDir()
    conf.clearOutDir()

async def ask4Doc(update, context):
    #global last_command
    #last_command = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envíame el documento 😊")

async def newsletter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/eldiario.jpg'), caption=mod.getHeadlines(), parse_mode='HTML')

async def cinema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/cinema.png'), caption=mod.getCinemaListings(), parse_mode='HTML')


async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=Path('resources/cinema.png'), caption='😊')

async def button_click(update, context):
    global msgId
    global last_command
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msgId)
    query = update.callback_query
    data = query.data
    
    if data == 'weather':
        await weather(update, context)
        await show_buttons(update, context)
    elif data == 'nasa':
        await nasa(update, context)
        await show_buttons(update, context)
    elif data == 'jokes':
        await jokes(update, context)
        await show_buttons(update, context)
    elif data == 'convert':
        last_command = data
        await ask4Doc(update, context)
    elif data == 'stats':
        last_command = data
        await ask4Doc(update, context)
    elif data == 'newsletter':
        await newsletter(update, context)
        await show_buttons(update, context)
    elif data == 'cinema':
        await cinema(update, context)
        await show_buttons(update, context)

async def show_buttons(update, context):
    global msgId
    keyboard = [
        [InlineKeyboardButton("Weather", callback_data='weather'),
         InlineKeyboardButton("NASA", callback_data='nasa')],
        [InlineKeyboardButton("Jokes", callback_data='jokes'),
         InlineKeyboardButton("Proposta", callback_data='convert')],
        [InlineKeyboardButton("Convert", callback_data='convert'),
         InlineKeyboardButton("Stats", callback_data='stats')],
        [InlineKeyboardButton("Newsletter", callback_data='newsletter'),
         InlineKeyboardButton("Cinema", callback_data='cinema')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = await context.bot.send_message(update.effective_chat.id, 'MENU', reply_markup=reply_markup)
    msgId = msg.message_id

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    conf.createInOut()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CommandHandler('nasa', nasa))
    application.add_handler(CommandHandler('jokes', jokes))
    application.add_handler(CommandHandler("convert", ask4Doc))
    application.add_handler(CommandHandler("stats", ask4Doc))
    application.add_handler(CommandHandler("newsletter", newsletter))
    application.add_handler(CommandHandler("cinema", cinema))

    application.add_handler(CommandHandler("proba", proba))

    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(CommandHandler('menu', show_buttons))

    application.add_handler(MessageHandler(filters.Document.ALL, processDocs))

    application.run_polling()

if __name__ == '__main__':
    main()