
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup



async def donate(update, context):
    keyboard = [
        [
            InlineKeyboardButton("North-North East", callback_data="NorthNE"),
            InlineKeyboardButton("Central & South", callback_data="CentralSouth"),
        ],
        [
            InlineKeyboardButton("East", callback_data="East"),
            InlineKeyboardButton("West", callback_data="West"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose the area of your location:", reply_markup=reply_markup)

async def areaRetriever(update, context):
    query = update.callback_query
    await query.answer()

    area = query.data
    locations = ""
    with open ("{}.txt".format(area),"r") as locationFile:
        locations += "Here are the food bank donation boxes in your area:\n\n" 
        for location in locationFile:
            locations += (location + "\n")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=locations,
    )


