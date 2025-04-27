import logging
from telegram import Update, ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters ,CallbackQueryHandler
from pycoingecko import CoinGeckoAPI

# Activation of the logging system
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Robot token
token = 'Your_Robot_Token'

# Prototyping of CoinGeckoAPI
cg = CoinGeckoAPI()

# Function for starting robot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("💰 بیت‌کوین", callback_data='bitcoin')],
        [InlineKeyboardButton("⚡ اتریوم", callback_data='ethereum')],
        [InlineKeyboardButton("🚀 تون‌کوین", callback_data='the-open-network')],
        [InlineKeyboardButton("📊 همه قیمت‌ها", callback_data='all')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"سلام {user.first_name}! 👋\nرمزارز مورد نظر رو انتخاب کن:",
        reply_markup=reply_markup
    )

# Function to hadle button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    try:
        await query.answer(text="در حال دریافت اطلاعات...")  

        data = query.data
        crypto_map = {
            "bitcoin": "بیت‌کوین",
            "ethereum": "اتریوم",
            "the-open-network": "تون‌کوین"
        }
        if data == "all":
            prices = []
            for coin_id, name in crypto_map.items():
                coin_data = cg.get_price(ids=coin_id, vs_currencies='usd')
                price = coin_data[coin_id]['usd']
                prices.append(f"{name}: ${price:.2f}")
            await context.bot.send_message(chat_id=query.message.chat_id, text="💸 قیمت لحظه‌ای:\n" + "\n".join(prices))
        else:
            name = crypto_map[data]
            coin_data = cg.get_price(ids=data, vs_currencies='usd')
            price = coin_data[data]['usd']
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"💲 قیمت {name}: ${price:.2f}")
    
    except Exception as e:
        logger.error(f"خطا در دریافت قیمت: {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text="متاسفم! مشکلی پیش آمده است.")


# Function to get single crypto price
async def get_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    crypto_map = {
        "بیت‌کوین": "bitcoin",
        "اتریوم": "ethereum",
        "تون‌کوین": "the-open-network"
    }

    # Define the keyboard layout
    reply_keyboard = [["بیت‌کوین", "اتریوم"], ["تون‌کوین", "همه قیمت‌ها"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    try:
        if text == "همه قیمت‌ها":
            prices = []
            for name, coin_id in crypto_map.items():
                coin_data = cg.get_price(ids=coin_id, vs_currencies='usd')
                price = coin_data[coin_id]['usd']
                prices.append(f"{name}: ${price:.2f}")
            await update.message.reply_text(
                "💸 قیمت لحظه‌ای:\n" + "\n".join(prices),
                reply_markup=markup
            )
        elif text in crypto_map:
            coin_id = crypto_map[text]
            coin_data = cg.get_price(ids=coin_id, vs_currencies='usd')
            price = coin_data[coin_id]['usd']
            await update.message.reply_text(
                f"💲 قیمت {text}: ${price:.2f}",
                reply_markup=markup
            )
        else:
            await update.message.reply_text(
                "دستور نامعتبر است. لطفاً یکی از گزینه‌ها را انتخاب کن.",
                reply_markup=markup
            )
    except Exception as e:
        logger.error(f"خطا در دریافت قیمت: {e}")
        await update.message.reply_text(
            "متاسفم! مشکلی در دریافت قیمت پیش آمده است.",
            reply_markup=markup
        )


# Unknown Message Management Function
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("دستور نامعتبر است. لطفاً یکی از گزینه‌های موجود را انتخاب کن.")

# The main settings of the robot
def main() -> None:
    # Build an app
    application = ApplicationBuilder().token(token).build()

    # Order Management
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Text(["بیت‌کوین", "اتریوم", "تون‌کوین", "همه قیمت‌ها"]), get_crypto_price))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Running the bot
    application.run_polling()

if __name__ == "__main__":
    main()
