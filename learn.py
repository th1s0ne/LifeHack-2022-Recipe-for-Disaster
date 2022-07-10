from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
import random

ROUTES = range(2)

RfDict = {
    "https://www.towardszerowaste.gov.sg/foodwaste/": [
        "Food waste makes up about half of the total household waste in Singapore daily!",
        "Food waste generated in Singapore has grown by around 20% over the last 10 years!",
        "When food is wasted, so are all of the resources used to grow and deliver the food to our tables, as well as to dispose of it. This increases our carbon footprint, contributing to global warming and climate change!",
        "Food wastage is unsustainable in land-scarce Singapore as more land will be used to build waste disposal facilities like waste-to-energy plants and landfills!",
        "In 2019, Singapore generated around 744 million kg of food waste. That is equivalent to 2 bowls of rice per person per day, or around 51,000 double decker buses!",
        f"Food wastage meant that more food has to be sourced to meet local demand. This can compromise our food security as Singapore imports over 90% of our food supply!",
        f"24% of households often threw away spoilt or rotten food because they either bought too much food or did not realise that they had food hidden at the back of their fridge.",
    ],
}
TipsDict = {
    "https://www.towardszerowaste.gov.sg/foodwaste/": [
        "Buy, order and cook only what you can finish! Ask for less rice/noodles if you can't finish them and say 'No' to side dishes you won't eat.",
        "Before going grocery shopping, make a shopping list of things you need so you won't overbuy.",
        "Check your fridge and cabinet before shopping to avoid buying things you already have.",
        "When preparing meals, find out the number of people eating in order to plan how much food to cook.",
        "Downsize the portions to avoid wasting food when a lot of dishes are prepared.",
        "Turn leftovers into new dishes instead of binning them! You can type /search to look up new recipes for the leftover ingredients now!",
        "Donate your excess food to avoid food wastage! You can type /donate to look up for nearest food bank donation boxes now!",
    ]
}
VidsList = [
    "https://www.youtube.com/watch?v=6RlxySFrkIM",
    "https://www.youtube.com/watch?v=ishA6kry8nc",
    "https://www.youtube.com/watch?v=c2hMNg6dlPY",
]


async def chooseLearn(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Random Fact", callback_data="Rf"),
            InlineKeyboardButton("Tip", callback_data="Tip"),
            InlineKeyboardButton("Video", callback_data="Vid"),
            InlineKeyboardButton("Back", callback_data="End"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What do you want to find out about food wastage?",
        reply_markup=reply_markup,
    )
    return ROUTES


async def getRf(update, context):
    Source, Factslist = random.choice(list(RfDict.items()))
    Fact = random.choice(Factslist)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="{}\nSource: {}".format(Fact, Source),
    )
    await chooseLearn(update, context)


async def getTip(update, context):
    Source, Tipslist = random.choice(list(TipsDict.items()))
    Tip = random.choice(Tipslist)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="{}\nSource: {}".format(Tip, Source),
    )
    await chooseLearn(update, context)


async def getVid(update, context):
    Vid = random.choice(VidsList)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Video: " + Vid,
    )
    await chooseLearn(update, context)


async def end(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Thank you for using /learn! To find out more about functions, press /start!",
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("learn", chooseLearn)],
    states={
        ROUTES: [
            CallbackQueryHandler(getRf, pattern=str("Rf")),
            CallbackQueryHandler(getTip, pattern=str("Tip")),
            CallbackQueryHandler(getVid, pattern=str("Vid")),
            CallbackQueryHandler(end, pattern=str("End")),
        ],
    },
    fallbacks=[CommandHandler("learn", chooseLearn)],
)
