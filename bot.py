import threading
import time
import requests
from telegram import Bot
from flask import Flask
import os

# Токен Telegram-бота (использовать через переменные окружения для безопасности)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Прямо указанный канал (если публичный)
TELEGRAM_CHAT_ID = "@alexbinancebotcrypto"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Список монет с целями
coins = {
    "fetch-ai": {"symbol": "FET", "target_buy": 1.00, "stop_loss": 0.70},
    "chainlink": {"symbol": "LINK", "target_buy": 20.00, "stop_loss": 15.00},
    "secret": {"symbol": "SCRT", "target_buy": 0.30, "stop_loss": 0.21},
    "avalanche-2": {"symbol": "AVAX", "target_buy": 30.00, "stop_loss": 22.00}
}

# Получение цены
def get_coin_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin_id]["usd"]

# Отправка в Telegram
def send_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

# Цикл отслеживания
def track_prices():
    # Стартовое сообщение
    msg = "✅ Бот запущен. Монеты и цели:\n"
    for coin_id, info in coins.items():
        try:
            price = get_coin_price(coin_id)
            msg += f"• {info['symbol']}: {price} USD (🎯 {info['target_buy']} / ⛔ {info['stop_loss']})\n"
        except:
            msg += f"• {info['symbol']}: ❌ не удалось получить цену\n"
    send_message(msg)

    while True:
        for coin_id, info in coins.items():
            try:
                price = get_coin_price(coin_id)
                if price >= info["target_buy"]:
                    send_message(f"🟢 {info['symbol']} достиг цели! Цена: {price} USD.")
                elif price <= info["stop_loss"]:
                    send_message(f"🔴 Стоп-лосс по {info['symbol']}! Цена: {price} USD.")
            except Exception as e:
                print(f"Ошибка {coin_id}: {e}")
        time.sleep(300)

# Flask-сервер для Render
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Crypto bot is running."

if __name__ == "__main__":
    t = threading.Thread(target=track_prices)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
