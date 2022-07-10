import os
from dotenv import load_dotenv
from telegram import CallbackQuery, Update
from DonationLocation import donate, areaRetriever
from learn import learn_handler
from search import search_handler
from py_edamam import Edamam


from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)


async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Welcome to NommNommBot!\n"
            "Feel free to press the following commands:\n"
            "/search - find new recipes for your leftover ingredient!\n"
            "/learn - find out more about food wastage in Singapore and actions you can take to allievate this problem!\n"
            "/donate - find out the nearest Food Bank donation boxes to your house today!"
        ),
    )

async def location(update, context):
    user = update.effective_user
    message = None

    global prev_message

    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    current_pos = (message.location.latitude, message.location.longitude)
    print(current_pos)

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

    start_handler = CommandHandler("start", start)
    donate_handler = CommandHandler("donate", donate)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(search_handler)
    application.add_handler(learn_handler)
    application.add_handler(donate_handler)
    application.add_handler(CallbackQueryHandler(areaRetriever))
    application.add_handler(unknown_handler)

    application.run_polling()