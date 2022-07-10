import os
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import requests
from py_edamam import Edamam
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    CommandHandler,
)

cuisineType = ""
dishType = ""
ROUTES = range(8)
RESULT = range(1)
API_Token = os.getenv("API_TOKEN")
API_ID = os.getenv("API_ID")


async def search(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Settings", callback_data="Set"),
            InlineKeyboardButton("Skip", callback_data="Skip"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please click 'Settings' to configure settings for specific searches or click 'Skip' to skip.",
        reply_markup=reply_markup,
    )
    return ROUTES


async def settings(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Cuisine Type", callback_data="Cuisine"),
            InlineKeyboardButton("Dish Type", callback_data="Dish"),
            InlineKeyboardButton("Proceed", callback_data="Skip"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose how you would like to filter your recipes.",
        reply_markup=reply_markup,
    )
    return ROUTES


async def cuisine(update, context):
    keyboard = [
        [
            InlineKeyboardButton("American", callback_data="American"),
            InlineKeyboardButton("French", callback_data="French"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose your preferred cuisine.",
        reply_markup=reply_markup,
    )
    return ROUTES


async def getCuisine(update, context):
    query = update.callback_query
    await query.answer()
    cuisineType = query.data
    await settings(update, context)


async def dish(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Mains", callback_data="Mains"),
            InlineKeyboardButton("Dessert", callback_data="Dessert"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose the type of dish you would like.",
        reply_markup=reply_markup,
    )
    return ROUTES


async def getDish(update, context):
    query = update.callback_query
    await query.answer()
    dishType = query.data
    await settings(update, context)


async def get(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Enter ingredients (eg. To search for a recipe with chicken skin and onions, type 'chicken skin onion'.)",
    )
    return RESULT


async def getData(update, context):
    query = update.callback_query
    await query.answer()
    q = ""
    for x in query.data:
        if x == " ":
            q += "%20"
        else:
            q += x

    

    if cuisineType == "" and dishType != "":
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&cuisineType={cuisineType}"
    elif cuisineType != "" and dishType == "":
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&dishType={dishType}"
    elif cuisineType == "" and dishType == "":
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}"
    else:
        url = f"https://api.edamam.com/api/recipes/v2?type=public&q={q}&app_id={API_ID}&app_key={API_Token}&cuisineType={cuisineType}&dishType={dishType}"

    
    data = requests.get(url).text()
    

    await update.message.reply_text(data)


search_handler = ConversationHandler(
    entry_points=[CommandHandler("search", search)],
    states={
        ROUTES: [
            CallbackQueryHandler(settings, pattern=str("Set")),
            CallbackQueryHandler(get, pattern=str("Skip")),
            CallbackQueryHandler(cuisine, pattern=str("Cuisine")),
            CallbackQueryHandler(dish, pattern=str("Dish")),
            CallbackQueryHandler(getCuisine, pattern=str("American")),
            CallbackQueryHandler(getCuisine, pattern=str("French")),
            CallbackQueryHandler(getDish, pattern=str("Mains")),
            CallbackQueryHandler(getDish, pattern=str("Dessert")),
        ],
        RESULT: [
            CallbackQueryHandler(getData),
        ],
    },
    fallbacks=[CommandHandler("search", search)],
)