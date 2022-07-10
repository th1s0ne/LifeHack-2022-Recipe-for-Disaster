import os
from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests
import pprint
from py_edamam import Edamam
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler
)

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="",
    )


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

cuisineType = ''
dishType = ''

async def messagehandler(update, context):
    text = update.message.text
    if text == "Settings":
        await settings(update, context)
    elif text == "Skip":
        await get(update, context)
    elif text == "Cuisine Type":
        await cuisine(update, context)
    elif text == "Dish Type":
        await dish(update, context)
    elif text == "American" or "French":
        cuisineType = text
        await get(update, context)
    elif text == "Mains" or "Dessert":
        dishType = text
        await get(update, context)
    else:
        await geturl(update, context)

       
async def search(update, context):
    buttons = [[KeyboardButton("Settings")], [KeyboardButton("Skip")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Please click 'Settings' to configure settings and click 'Skip' to skip.", reply_markup = reply_markup)


async def settings(update, context):
    buttons = [[KeyboardButton("Cuisine Type")], [KeyboardButton("Dish Type")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Choose how you would like to filter your recipes.", reply_markup = reply_markup)


async def cuisine(update, context):
    buttons = [[KeyboardButton("American")], [KeyboardButton("French")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Choose your preferred cuisine.", reply_markup = reply_markup)


async def dish(update, context):
    buttons = [[KeyboardButton("Mains")], [KeyboardButton("Dessert")]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text("Choose the type of dish you would like.", reply_markup = reply_markup)
 

async def get(update, context):
    reply_markup = ForceReply()
    await update.message.reply_text("Enter ingredients (eg. To search for a recipe with chicken skin and onions, type 'chicken skin onion'.)", reply_markup = reply_markup) 
    
async def geturl(update, context):
    q = ''
    for x in update.message.text:
        if x == ' ':
            q += '%20'
        else: q += x
    
    print(q)
    
    if cuisineType == '' and dishType != '':
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&cuisineType={cuisineType}'
    elif cuisineType != '' and dishType == '':
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&dishType={dishType}'
    elif cuisineType == '' and dishType == '':
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}'
    else:
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&cuisineType={cuisineType}&dishType={dishType}'

    print(url)
    data =  requests.get(url)
    print(data)

    """await update.message.reply_text(data)"""
    
async def learn(update, context):
    pass


async def donate(update, context):
    pass

async def unknown(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Please type /start to start",
    )

if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_Token = os.getenv("API_TOKEN")
    API_ID = os.getenv("API_ID")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    e = Edamam(recipes_appid=API_ID, recipes_appkey=API_Token)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    search_handler = CommandHandler("search", search)
    learn_handler = CommandHandler("learn", learn)
    donate_handler = CommandHandler("donate", donate)
    message_handler = MessageHandler(filters.TEXT, messagehandler)
    
    
    application.add_handler(search_handler)
    application.add_handler(message_handler)
    application.add_handler(learn_handler)
    application.add_handler(donate_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
