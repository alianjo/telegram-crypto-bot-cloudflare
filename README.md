# Telegram Crypto Price Bot

A Telegram bot on Cloudflare Workers that fetches real-time cryptocurrency prices using CoinGecko API.

## Features
- Get crypto prices with `/price <crypto>` (e.g., `/price bitcoin`).
- Serverless deployment on Cloudflare Workers.


# Telegram Crypto Price Bot 📈🤖

A simple Telegram bot that provides real-time prices of popular cryptocurrencies like Bitcoin, Ethereum, and Toncoin.

## Technologies Used 🛠️
- Python 3.12
- `python-telegram-bot` library
- CoinGecko API for real-time crypto prices
- Railway for deployment and hosting

## Project Architecture 🏗️
- Users interact with the bot through Telegram buttons.
- Upon selection, the bot fetches the real-time price from the CoinGecko API.
- The bot then sends the current price back to the user.
- The project is deployed and hosted using Railway.

## Setup Guide 🚀

### 1. Preparing the Code
- The project includes a main Python script that manages the bot and handles user interactions.
- Handlers are used to manage button clicks and API responses.

### 2. Deploying on Railway
- Push your project to a GitHub repository.
- Sign in to [Railway](https://railway.app/) and create a new project.
- Choose **Deploy from GitHub** and select your repository.
- Add an environment variable:
  - `BOT_TOKEN`: Your Telegram bot token.
- Railway automatically detects and runs the Python project without the need for a Dockerfile.

✅ Note:  
**No Dockerfile or docker-compose.yml is required for this deployment.**

## Bot Workflow 📲
- The bot displays a menu with crypto options.
- When a user selects an option, the bot fetches and sends the real-time price.
- If the "All" option is selected, it sends the prices of all supported cryptocurrencies.

## Example of the Main Bot Logic
```python
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    crypto_map = {
        "bitcoin": "Bitcoin",
        "ethereum": "Ethereum",
        "the-open-network": "Toncoin"
    }

    try:
        if data == "all":
            prices = []
            for coin_id, name in crypto_map.items():
                coin_data = cg.get_price(ids=coin_id, vs_currencies='usd')
                price = coin_data[coin_id]['usd']
                prices.append(f"{name}: ${price:.2f}")
            await context.bot.send_message(chat_id=query.message.chat_id, text="💸 Current Prices:\n" + "\n".join(prices))
        else:
            name = crypto_map[data]
            coin_data = cg.get_price(ids=data, vs_currencies='usd')
            price = coin_data[data]['usd']
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"💲 {name} Price: ${price:.2f}")
    except Exception as e:
        logger.error(f"Error fetching price: {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text="Sorry! Something went wrong.")
```

## Final Result ✅
A lightweight and fast Telegram bot to fetch real-time cryptocurrency prices without the need for a complex server setup.

---

