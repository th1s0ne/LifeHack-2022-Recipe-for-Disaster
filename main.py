import os
from dotenv import load_dotenv
from telegram import Update

from py_edamam import Edamam


from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
)



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
    application.add_handler(unknown_handler)
    
    application.run_polling()
